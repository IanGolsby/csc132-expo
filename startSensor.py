from time import sleep
import subprocess

sleep(2)
subprocess.run("python3 sensor_testing.py", shell=True)
