# main.py
from camera_module import SmartCamera
camera = SmartCamera(save_dir="images")
try:
    while True:
        cmd = input("Press 'c' to capture or 'q' to quit: ")
        if cmd.lower() == 'c':
            camera.capture_image()
        elif cmd.lower() == 'q':
            break
finally:
    camera.stop()
