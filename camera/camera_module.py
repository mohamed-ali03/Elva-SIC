# camera_module.py
from picamera2 import Picamera2
from datetime import datetime
from io import BytesIO
import os
import time

class SmartCamera:
    def __init__(self, save_dir="images"):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())
        self.picam2.start()
        time.sleep(2)
        os.makedirs(save_dir, exist_ok=True)
        self.save_dir = save_dir

    def capture_image(self):
        filename = os.path.join(
            self.save_dir,
            f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        self.picam2.capture_file(filename)
        print("Saved image:", filename)
        return filename

    def get_image_bytes(self):
        stream = BytesIO()
        self.picam2.capture_file(stream, format='jpeg')
        stream.seek(0)
        return stream.read()

    def stop(self):
        self.picam2.stop()
