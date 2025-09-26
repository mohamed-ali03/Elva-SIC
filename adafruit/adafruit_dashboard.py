from Adafruit_IO import Client

class ElevatorDashboard:
    def __init__(self,username,key):
        self.username = username
        self.key = key
        self.aio = Client(self.username, self.key)

    def send_temp_humid(self, temperature, humidity):
        self.aio.send("temperature", round(temperature, 2))
        self.aio.send("humidity", round(humidity, 2))
        print(f"Sent Temp={temperature}, Humid={humidity}")

    def send_door_number(self, doornumber):
        self.aio.send("door-number", int(doornumber))
        print(f"Sent Door={doornumber}")

    def send_Next_Floors(self, nextfloors):
        nextfloors = ", ".join(nextfloors)
        self.aio.send("desireddoorsarray", int(nextfloors))
        print(f"Sent Door={nextfloors}")

    def send_image(self, image_url):
        self.aio.send("image", image_url)
        print(f"Sent Image URL={image_url}")



