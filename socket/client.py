import socket
import json

PORT = 5051
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
HEADER = 64
FORMAT = "utf-8"


RETURN_VALUE = 1
RETURN_NANE  = 0

DISCONNECT    = 0
UPDATE_FLOORS = 1
GET_FLOORS    = 2
UPDATE_TEMP   = 3
GET_TEMP      = 4


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)


"""
parameter : msg
                msg[0] --> need return or not
                msg[1] --> operation id
                msg[2:]--> data

"""
def send(msg):
    msg_s = json.dumps(msg[1:]).encode(FORMAT)
    client.send(msg_s)

    if msg[0] == 1:
        msg_r = client.recv(2048).decode(FORMAT)
        msg_r = json.loads(msg_r)
        return msg_r
    return None


while True:
    msg = list(map(int,input().split(',')))
    msg = send(msg)
    if msg :
        print(msg)

    

