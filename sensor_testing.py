""" MODULE IMPORTS """
import RPi.GPIO as GPIO
import time



""" GLOBAL VARIABLES """
# When enabled, it will never do anything to do with actual sensors and only deal with button
button_only = True
pin_mq4_alarm = 25
pin_mq7_heater = 3
pin_mq7_alarm = 4
pin_button = 13
pin_buzzer = 22
mq7_mode = ""
state = "Nothing"
last_state = ""

""" USER FUNCTIONS """
def main_loop():
    # Track when we started the loop
    loop_start_time = time.time()

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
        play_sound(pin_buzzer, 220, 3)

def play_sound(pin, freq, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        GPIO.output(pin, 1)
        time.sleep(0.5 / freq)
        GPIO.output(pin, 0)
        time.sleep(0.5 / freq)



""" MAIN CODE """
# Set up GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_buzzer, GPIO.OUT)

if not button_only:
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
