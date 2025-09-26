import time
from mqtt_pubsub import MQTTPublisher
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "socket")))

import client


pub = MQTTPublisher(topic="temperature")
pub.connect()

"""
while True :
    temp = random.randint(-40,80)
    pub.publish(temp)
    time.sleep(1)
"""
while True:
    temp_humid = client.send(client.RETURN_VALUE,client.GET_TEMP)
    desiredfloors = client.send([client.RETURN_VALUE,client.GET_FLOORS])
    pub.publish(f"Curret Floor : {desiredfloors[0]}, Next Floors : {desiredfloors[1:]}")
    pub.publish(f"Temperature : {temp_humid[0]}, Humidity : {temp_humid[1]}")
    time.sleep(1)
    
