""" MODULE IMPORTS """
import RPi.GPIO as GPIO
import time, values

""" GLOBAL VARIABLES """
# When enabled, it will never do anything to do with actual sensors and only deal with button
button_only = True
pin_mq4_heater = 1
pin_mq4_alarm = 2
pin_mq7_heater = 3
pin_mq7_alarm = 4
pin_button = 18
detected = open("detected.txt", "w+")

""" USER FUNCTIONS """
def mq7_purge():
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

def mq7_sense():
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

def mq4_sense():
    alarm = GPIO.input(pin_mq4_alarm)
    if alarm:
        print("MQ4 DETECTED FLAMMABLE GAS LEVELS ABOVE THRESHOLD")
        detected.write("Flammable Gas")

def button_sense():
    alarm = GPIO.input(pin_button)
    if alarm:
        print("BUTTON PRESSED")
        detected.write("Button")



""" MAIN CODE """
# Set up GPIO
GPIO.setmode(GPIO.BCM)

if not button_only:
    GPIO.setup(pin_mq4_heater, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pin_mq4_alarm, GPIO.IN)
    GPIO.setup(pin_mq7_heater, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pin_mq7_alarm, GPIO.IN)

GPIO.setup(pin_button, GPIO.IN)

# Always check for keyboard interrupt
try:
    while True:
        # Begin PURGE phase
        mq7_purge()
        # Begin SENSE phase
        mq7_sense()
# Halt execution when interrupt is pressed
except KeyboardInterrupt:
    GPIO.cleanup()