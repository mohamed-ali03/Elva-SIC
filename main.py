""" Import Section """
from adafruit.adafruit_dashboard import ElevatorDashboard
from mqtt.mqtt_pubsub import MQTTPublisher
from camera.camera_module import SmartCamera
from camera import camerawithflask

from dcmotor.dcmotor import DCMotor
from servo.servo import Servo

from ultrasonic.ultrasonic import Ultrasonic
import Adafruit_DHT

import threading
import time

""" Global Varaible Section """
""" PINS """
ULTRASONIC_TRIG_PIN = 2
ULTRASONIC_ECHO_PIN = 3
DCMOTOR_IN1_PIN = 4
DCMOTOR_IN2_PIN = 5
SERVO_MOTOR_PIN = 13
DHT_PIN = 6
""" Threading Locks """
desiredfloorsLock = threading.Lock()
humidityTemperatureLock = threading.Lock()
doorStatusLock = threading.Lock()
""" Variable related to the motion of elevator """
ultra = Ultrasonic(ULTRASONIC_TRIG_PIN,ULTRASONIC_ECHO_PIN)
dcmotor = DCMotor(DCMOTOR_IN1_PIN,DCMOTOR_IN2_PIN)
servomotor = Servo(SERVO_MOTOR_PIN)
READING_TIME = 10                        # constant reading time to ensure that is not a wrong reading
DURATION_BETWEEN_DOORS = 15              # time taken to move from one door to the next one
NOT_A_READING = -1                       # constant for wrong reading status
currentfloor = 0                         # Start in the ground floor
desiredfloors = [currentfloor]           # Set of the doors to reach
doorstatus = "Closed"

""" DHT Varaibles """
dht = Adafruit_DHT.DHT22
humidity = 0                             # Initial value of humidity
temperature = 0                          # Initial value of temperature

""" MQTT Variables"""
mqttPUB = MQTTPublisher(topic="Elva-Status")
mqttPUB.connect()

""" Adafruit Varaibles """
dashboard = ElevatorDashboard()

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

""" Thread Funcations Section """
def getDoors():
    global desiredfloors , currentfloor
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
    global currentfloor, desiredfloors,doorstatus
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
        with doorStatusLock:
            doorstatus = "Opened"
        time.sleep(15)
        servomotor.setServoAngle(0)               # Close the door
        with doorStatusLock:
            doorstatus = "Closed"
        time.sleep(5)

        with desiredfloorsLock :
            if desiredfloors[0] == currentfloor:
                del desiredfloors[0]                      # shift list one step to the lift 
            currentfloor = desiredfloors[0] if desiredfloors else currentfloor


def getTempHumid():
    global humidity , temperature
    while True:
        with humidityTemperatureLock:
            humidity,temperature = Adafruit_DHT.read_retry(dht, dhtThread)
        time.sleep(1)


def pubMQTTMasseg():
    while True :
        msg = f"Current Floor = {currentfloor}, Next Floor = {desiredfloors[1]} ,Temperature = {temperature} , Humidity = {humidity} , Door Status = {doorstatus}"
        mqttPUB.publish(msg)
        time.sleep(1)

def pubAdafruitDashboard():
    while True:
        dashboard.send_temp_humid(temperature,humidity)
        dashboard.send_door_number(currentfloor)
        time.sleep(1)

""" main Section """
if __name__ == "__main__":
    ultraThread = threading.Thread(target=getDoors)
    ultraThread.start()

    elevMoveThread = threading.Thread(target=moveElevator)
    elevMoveThread.start()

    dhtThread = threading.Thread(target=getTempHumid)
    dhtThread.start()

    mqttThread = threading.Thread(target=pubMQTTMasseg)
    mqttThread.start()

    dashboardThread = threading.Thread(target=pubAdafruitDashboard)
    dashboardThread.start()

    # run camera
    camerawithflask.app.run(host='0.0.0.0', port=5000)


    ultraThread.join()
    dhtThread.join()
    elevMoveThread.join()
    mqttThread.join()
    dashboardThread.join()
