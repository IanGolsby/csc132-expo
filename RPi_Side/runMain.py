import subprocess
import threading

def threadProcess():
    subprocess.run("python3 startSensor.py", shell=True)

x = threading.Thread(target=threadProcess, daemon=True)
x.start()

try:
    subprocess.run("python3 startServer.py", shell=True)
except KeyboardInterrupt:
    print("Exited runMain.py from Interrupt")
