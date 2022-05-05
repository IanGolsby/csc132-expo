from time import sleep
import subprocess

try:
    sleep(2)
    subprocess.run("python3 socketServer.py", shell=True)
except:
    print("startSocket.py interrupted by keyboard")
