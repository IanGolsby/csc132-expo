import socket

HOST = "192.168.0.158" # the server's hostname or IP address
PORT = 1024

def sendData(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            try: s.sendall(data)
            except: print("Sending Error")
        except: print("Connection Error")
        
        s.close()