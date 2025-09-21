import time
from mqtt_pubsub import MQTTPublisher

pub = MQTTPublisher(topic="elevator/floor")
pub.connect()

for i in range(1, 5):
    msg = f"Elevator at floor {i}"
    pub.publish(msg)
    time.sleep(2)
