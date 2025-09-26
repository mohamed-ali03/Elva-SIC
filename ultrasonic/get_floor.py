from ultrasonic import Ultrasonic
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "socket")))

import client

NOT_A_READING = -1
READING_TIME = 5



TRIG = 2
ECHO = 3

ultra = Ultrasonic(TRIG,ECHO)

def _getDesiredDoorNumber(distance):
    if distance >=0 and distance < 12 :
            return 1
    elif distance  >=12 and distance < 20 :
            return 2 
    elif distance >= 20 and distance < 32 :
            return 3
    elif distance >= 32 and distance < 42 :
            return  4
    return None

def getDoors():
    while True:
        ultradistance = ultra.get_distance()

        if ultradistance is not None and ultradistance <= 42 :
            starttime = time.time()
            readingfloor = _getDesiredDoorNumber(ultradistance)
            while time.time() < starttime + READING_TIME:
                  ultradistance = ultra.get_distance()
                  bufferreadingfloor = _getDesiredDoorNumber(ultradistance)
                  
                  if readingfloor != bufferreadingfloor:
                        readingfloor = NOT_A_READING
                        break
                  

            desiredfloors = client.send([client.RETURN_VALUE,client.GET_FLOORS])
            currentfloor = desiredfloors[0]
                                                # to avoid redundent floor number
            if readingfloor != NOT_A_READING and readingfloor not in desiredfloors:
                print(f"[ADDING FLOOR] {readingfloor}.")
                desiredfloors.append(readingfloor)
                desiredfloors.sort()
                
                idx = desiredfloors.index(currentfloor)

                part1 = sorted(desiredfloors[idx:])
                part2 = sorted(desiredfloors[:idx], reverse=True)
                
                desiredfloors[:] = part1 + part2
                client.send([client.RETURN_NANE,client.UPDATE_FLOORS] + desiredfloors)
                print(f"[NEXT FLOORS] [{' ,'.join(desiredfloors)}]")
        time.sleep(0.1)
