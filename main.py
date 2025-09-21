""" Import Section """
from adafruit.adafruit_dashboard import ElevatorDashboard
from mqtt.mqtt_pubsub import MQTTPublisher ,MQTTSubscriber
from camera.camera_module import SmartCamera

from dcmotor.dcmotor import DCMotor
from servo.servo import Servo

from ultrasonic.ultrasonic import Ultrasonic
import Adafruit_DHT

import threading
import time

""" Global Varaible Section """
""" Variable related to the motion of elevator """
ultra = Ultrasonic(2,3)
dcmotor = DCMotor(4,5)
servomotor = Servo(13)
READING_TIME = 10                        # constant reading time to ensure that is not a wrong reading
DURATION_BETWEEN_DOORS = 15              # time taken to move from one door to the next one
NOT_A_READING = -1                       # constant for wrong reading status
ultradistance = 0                        # Iintial value of distance = 0
currentfloor = 0                         # Start in the ground floor
readingfloor = 0                         # Initiat the readingfloor by 0
bufferreadingfloor = 0                   # to have access to the previous value of the reading floor number
desiredfloors = [currentfloor]           # Set of the doors to reach
desiredfloorsLock = threading.Lock()

""" Supperted Functions Section """
def getDesiredDoorNumber(distance):
    if distance >=0 and distance < 12 :
            return 1
    elif distance  >=12 and distance < 20 :
            return 2 
    elif distance >= 20 and distance < 32 :
            return 3
    elif distance >= 32 and distance < 40 :
            return  4
    return None

""" SubTasks Section """
def getDoors():
    global desiredfloors
    while True:
        ultradistance = ultra.get_distance()

        if ultradistance is not None and ultradistance <= 40 :
            starttime = time.time()
            readingfloor = getDesiredDoorNumber(ultradistance)
            while time.time() < starttime + READING_TIME:
                  ultradistance = ultra.get_distance()
                  bufferreadingfloor = getDesiredDoorNumber(ultradistance)
                  if readingfloor != bufferreadingfloor:
                        readingfloor = NOT_A_READING
                        break
                  
            
                                                # to avoid redundent floor number
            if readingfloor != NOT_A_READING and readingfloor not in desiredfloors:
                with desiredfloorsLock:
                    desiredfloors.append(readingfloor)
                    desiredfloors.sort()
                    
                    idx = desiredfloors.index(currentfloor)

                    part1 = sorted(desiredfloors[idx:])
                    part2 = sorted(desiredfloors[:idx], reverse=True)
                    
                    desiredfloors[:] = part1 + part2
        time.sleep(0.1)


def moveElevator():
    global currentfloor, desiredfloors
    while True :
        with desiredfloorsLock:
            if len(desiredfloors) <= 1:
                time.sleep(0.1)
                continue
            nextfloor = desiredfloors[1]
        
        step = 1 if nextfloor > currentfloor else -1
        starttime = time.time()
        if step == 1 :
            dcmotor.moveForward()
        else:
            dcmotor.moveBackward()

        duration = DURATION_BETWEEN_DOORS * abs(nextfloor - currentfloor)
        while time.time() < (starttime + duration):
            time.sleep(0.01)

        dcmotor.stop()

        time.sleep(5)
        servomotor.setServoAngle(90)              # Open the door
        time.sleep(15)
        servomotor.setServoAngle(0)               # Close the door
        time.sleep(5)

        with desiredfloorsLock :
            if desiredfloors[0] == currentfloor:
                del desiredfloors[0]                      # shift list one step to the lift 
            currentfloor = desiredfloors[0] if desiredfloors else currentfloor
              




def getTempHumid():
    pass



""" main Section """
if __name__ == "__main__":
    ultraThread = threading.Thread(target=getDoors)
    ultraThread.start()

    elevMoveThread = threading.Thread(target=moveElevator)
    elevMoveThread.start()

    dhtThread = threading.Thread(target=getTempHumid)
    dhtThread.start()




    ultraThread.join()
    dhtThread.join()
    elevMoveThread.join()
