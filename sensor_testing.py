""" MODULE IMPORTS """
import RPi.GPIO as GPIO
import time
""" GLOBAL VARIABLES """
# When enabled, it will never do anything to do with actual sensors and only deal with button
button_only = True
pin_mq4_heater = 1
pin_mq4_alarm = 2
pin_mq7_heater = 3
pin_mq7_alarm = 4
pin_button = 13
pin_buzzer = 12
mq7_mode = ""
state = "Nothing"
last_state = ""

""" USER FUNCTIONS """
def main_loop():
    # Track when we started the loop
    loop_start_time = time.time()

    # Activate MQ4 heater
    if not button_only:
        GPIO.output(pin_mq4_heater, 1)

    # MQ7 is in purge phase for one minute
    mq7_mode = "PURGE"
    while time.time() - loop_start_time < 60:
        # Activate the heater
        if not button_only:
            GPIO.output(pin_mq7_heater, 0)
        
        # Check all sensors
        read_sensors()

        # Wait so we aren't constantly refreshing stuff
        time.sleep(0.1)

    # MQ7 is in sense phase for next 90 sec
    mq7_mode = "SENSE"
    while time.time() - loop_start_time < 150:

        # Cycle heater 7ms on 18ms off -- 1.4V PWM
        if not button_only:
            GPIO.output(pin_mq7_heater, 0)
        time.sleep(0.007)
        if not button_only:
            GPIO.output(pin_mq7_heater, 1)
        time.sleep(0.018)

        #Check all sensors
        read_sensors()

def read_sensors():
    global state

    btn_alarm = GPIO.input(pin_button)
    if not button_only:
        mq4_alarm = GPIO.input(pin_mq4_alarm)
        mq7_alarm = 0 if mq7_mode == "PURGE" else GPIO.input(pin_mq7_alarm)
    else:
        mq4_alarm, mq7_alarm = 0, 0

    # Hold previous state information
    last_state = state
    
    # Tells if we've written to the state this round
    state_flag = 0

    # Append information for each alarm
    state = ""
    if btn_alarm:
        state += "Button Pressed, "
        state_flag = 1
    if mq4_alarm:
        state += "Flammable Gas, "
        state_flag = 1
    if mq7_alarm:
        state += "Carbon Monoxide, "
        state_flag = 1

    if not state_flag:
        state = "Nothing"

    # If the state isn't Nothing,
    if state != "Nothing":
        # Remove the comma at the end
        state = state[:-2]
    
    # If the state has changed
    if state != last_state:
        # Update the text file
        with open("detected.txt", "w+") as detected:
            detected.write(state)
    
    # Activate the buzzer
    if state != "Nothing":
        play_sound(pin_buzzer, 220, 5)

def play_sound(pin, freq, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        GPIO.output(pin, 1)
        time.sleep(0.5 / freq)
        GPIO.output(pin, 0)
        time.sleep(0.5 / freq)



""" CURRENTLY DEPRECATED FUNCTIONS """

def deprecated_mq7_purge():
    """ Purges sensor by activating heater at full power for one minute """
    # Activate heater (active low) for one minute
    if not button_only:
        GPIO.output(pin_mq4_heater, 0)
    for i in range(60):
        time.sleep(1)
        if not button_only:
            mq4_sense()
        button_sense()
    # Deactivate heater
    if not button_only:
        GPIO.output(pin_mq4_heater, 1)

def deprecated_mq7_sense():
    """ Runs heater at ~1.4V for 90 sec to sense, calibrate, or check sensor """
    # Tracks how long we've been sensing
    start_time = time.time()
    while(1):
        # 7ms on, 18ms off -- makes 1.4V
        # Cycle heater
        if not button_only:
            GPIO.output(pin_mq4_heater, 0)
        time.sleep(0.007)
        if not button_only:
            GPIO.output(pin_mq4_heater, 1)
        time.sleep(0.018)

        # Sense while we're in sense phase
        if not button_only:
            mq7_alarm = GPIO.input(pin_mq7_alarm)
        else:
            mq7_alarm = 0
        if mq7_alarm:
            print("MQ7 DETECTED CO LEVELS OVER THRESHOLD")
            detected.write("CO")
        if not button_only:
            mq4_sense()
        button_sense()

        # Check elapsed time
        if time.time() - start_time >= 90:
            # We hit 90 seconds, so exit loop
            break

def deprecated_mq7_sense():
    alarm = GPIO.input(pin_mq7_alarm)
    if alarm:
        print("MQ7 DETECTED CO LEVELS ABOVE THRESHOLD")
        detected.write("Flammable Gas")

def deprecated_mq4_sense():
    alarm = GPIO.input(pin_mq4_alarm)
    if alarm:
        print("MQ4 DETECTED FLAMMABLE GAS LEVELS ABOVE THRESHOLD")
        detected.write("Flammable Gas")

def deprecated_button_sense():
    alarm = GPIO.input(pin_button)
    if alarm:
        print("BUTTON PRESSED")
        detected.write("Button")



""" MAIN CODE """
# Set up GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_buzzer, GPIO.OUT)

if not button_only:
    GPIO.setup(pin_mq4_heater, GPIO.OUT)
    GPIO.setup(pin_mq4_alarm, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pin_mq7_heater, GPIO.OUT)
    GPIO.setup(pin_mq7_alarm, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Always check for keyboard interrupt
try:
    while True:
        main_loop()
# Halt execution when interrupt is pressed
except KeyboardInterrupt:
    GPIO.cleanup()
