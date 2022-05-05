import socket
from time import sleep

HOST = "192.168.0.158" # Standard loopback interface address (localhost)
PORT = 1024 # Port to listen on (non-privliged ports are > 1023)

while(True):
    # boilerplate socket code
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn: 
            print(f"Connected by {addr}")
            try:
                while True:
                    data = conn.recv(PORT) # receives data from client
                    #conn.sendall(data)
                    if data.decode().strip() != "":
                        print(data.decode())
                        with open("detected.txt", "w+") as f: 
                            f.write(data.decode()) # write data to file
                        break
            except KeyboardInterrupt:
                print("socketServer.py interrupted by keyboard")
                s.close()
