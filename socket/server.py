import socket
import threading
import json

PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
HEADER = 64
FORMAT = "utf-8"

DISCONNECT    = 0
UPDATE_FLOORS = 1
GET_FLOORS    = 2
UPDATE_TEMP   = 3
GET_TEMP      = 4


desiredfloors = [0]
temp  = 0
humid = 0

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn,addr):
    global desiredfloors
    print(f"[NEW CONNECTION] {addr}")

    connected = True
    while connected:
        received = conn.recv(2048).decode(FORMAT)
        data_r = json.loads(received)
        if len(data_r) >= 1:
            if data_r[0]   == UPDATE_FLOORS:
                desiredfloors = data_r[1:]
                print(f"Desired Floors {desiredfloors}")
            elif data_r[0] == GET_FLOORS:
                data_s = json.dumps(desiredfloors).encode(FORMAT)
                conn.send(data_s)
            elif data_r[0] == UPDATE_TEMP:
                temp  = data_r[1]
                humid = data_r[2]
                print(f"Temperature = {temp}, Humidity = {humid}")
            elif data_r[0] == GET_TEMP :
                data_s = [temp,humid]
                data_s = json.dumps(data_s).encode(FORMAT)
                conn.send(data_s)
            elif data_r[0] == DISCONNECT:
                print(f'[DISCONNECTED] {addr}')
                connected = False
                conn.send(json.dumps([-1]).encode(FORMAT))
            else:
                conn.send(json.dumps([-1]).decode(FORMAT))
    conn.close()

            

def start():
    server.listen()
    print(f"[LISTENING] server is listening on {ADDR}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")



print("[STARTING] server is starting .......")
start()






