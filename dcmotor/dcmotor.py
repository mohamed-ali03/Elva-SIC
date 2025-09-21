import RPi.GPIO as GPIO
from time import sleep


# just controll the direction not the speed 
class DCMotor:
    def __init__(self,IN1,IN2):
        self.IN1 = IN1
        self.IN2 = IN2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)

    def moveForward(self):
        GPIO.output(self.IN1,GPIO.HIGH)
        GPIO.output(self.IN2,GPIO.LOW)
    
    def moveBackward(self):
        GPIO.output(self.IN1,GPIO.LOW)
        GPIO.output(self.IN2,GPIO.HIGH)

    def stop(self):
        GPIO.output(self.IN1,GPIO.LOW)
        GPIO.output(self.IN2,GPIO.LOW)