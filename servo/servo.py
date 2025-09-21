import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self,pin):         # pin must be a PWM pin
        self.sevoPin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sevoPin, GPIO.OUT)

        self.servoPWM= GPIO.PWM(self.sevoPin, 50)
        self.servoPWM.start(0)
        time.sleep(0.5)


    def setServoAngle(self,angle):
        duty = 2 + (angle / 18)
        self.servoPWM.ChangeDutyCycle(duty)
        time.sleep(0.5)  
        self.servoPWM.ChangeDutyCycle(0)
    
    def cleanup(self):
        self.servoPWM.stop()
        GPIO.cleanup()


