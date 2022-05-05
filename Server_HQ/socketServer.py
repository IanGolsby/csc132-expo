import socket
from time import sleep

#f = open("detected.txt", "w+")

HOST = "192.168.0.158" # Standard loopback interface address (localhost)
PORT = 1024 # Port to listen on (non-privliged ports are > 1023)

# boilerplate socket code
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn: 
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(PORT) # receives data from client
                conn.sendall(data)
                if data.decode().strip() != "":
                    print(data.decode())
                    with open("detected.txt", "w+") as f: 
                        f.write(data.decode()) # write data to file
        except KeyboardInterrupt:
            print("socketServer.py interrupted by keyboard")
            s.close()
