import time
import board
import adafruit_dht


class DHT11:
    def __init__(self,pin):
        self.dht = adafruit_dht.DHT11(pin)
    
    def get_data(self):
        temperature = self.dht.temperature
        humidity = self.dht.humidity
        return temperature,humidity
