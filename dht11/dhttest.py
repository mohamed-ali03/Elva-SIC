from dht import DHT11 ,board
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "socket")))

import client

dhtSensor = DHT11(board.D6)


def get_env_data():
    while True:
        temperature , humidity = dhtSensor.get_data()
        client.send(client.RETURN_NANE,client.UPDATE_TEMP,temperature,humidity)
        time.sleep(1)

