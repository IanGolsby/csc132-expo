from time import sleep
import subprocess

sleep(2)

try:
    subprocess.run("python3 sensor_testing.py", shell=True)
except KeyboardInterrupt:
    print("Exited startSensor.py from Interrupt")