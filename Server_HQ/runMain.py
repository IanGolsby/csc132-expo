import subprocess
import threading

def threadProcess():
    subprocess.run("python3 startSocket.py", shell=True)

x = threading.Thread(target=threadProcess, daemon=True)
x.start()
subprocess.run("python3 startServer.py", shell=True)


