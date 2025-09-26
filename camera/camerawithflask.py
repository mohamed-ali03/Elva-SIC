from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "socket")))

import client


app = Flask(__name__)

camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

def generate_frames():
    while True:
        frame = camera.capture_array()
        temp_humid = client.send(client.RETURN_VALUE,client.GET_TEMP)
        desiredfloors = client.send([client.RETURN_VALUE,client.GET_FLOORS])
        
        # Overlay text on the frame
        text1 = f"Temp: {temp_humid[0]} C"
        text2 = f"Hum: {temp_humid[1]} %"
        text3 = f"Current Floor: {desiredfloors[0]}"
        text4 = f"Next Floors: {desiredfloors[1:]}"

        cv2.putText(frame, text1, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, text2, (10,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.putText(frame, text3, (10,110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        cv2.putText(frame, text4, (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)


        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# use this code to run the camera from another file
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""


