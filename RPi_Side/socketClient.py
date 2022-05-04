import socket

HOST = "192.168.0.158" # the server's hostname or IP address
PORT = 1024

def sendData(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data)
        stuff = s.recv(1024)
        print(f"Received {stuff!r}")
