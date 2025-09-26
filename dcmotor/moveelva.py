from dcmotor import DCMotor
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".." )))

from socket import client
from servo.servo import Servo

DURATION_BETWEEN_DOORS = 20
IN1 = 4
IN2 = 5
SERVO_PIN = 13
motor = DCMotor(IN1,IN2)
servomotor = Servo(SERVO_PIN)

def moveElevator():
    global doorstatus
    desiredfloors = client.send([client.RETURN_VALUE,client.GET_FLOORS])
    currentfloor = desiredfloors[0]
    nextfloor = desiredfloors[1]
        
    step = 1 if nextfloor > currentfloor else -1
    starttime = time.time()
    if step == 1 :
        motor.moveForward()
    else:
        motor.moveBackward()

    duration = DURATION_BETWEEN_DOORS * abs(nextfloor - currentfloor)
    while time.time() < (starttime + duration):
        time.sleep(0.01)

    motor.stop()


    time.sleep(5)
    servomotor.setServoAngle(90)              # Open the door
    doorstatus = "Opened"
    time.sleep(15)
    servomotor.setServoAngle(0)               # Close the door
    doorstatus = "Closed"
    time.sleep(5)

    desiredfloors = client.send([client.RETURN_VALUE,client.GET_FLOORS])
    client.send([client.RETURN_NANE,client.UPDATE_FLOORS] + desiredfloors[1:])
