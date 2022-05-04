from time import sleep
import subprocess

sleep(2)
subprocess.run("python3 socketServer.py", shell=True)