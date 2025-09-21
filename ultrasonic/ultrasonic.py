import RPi.GPIO as GPIO
import time


class Ultrasonic:
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(2)

    def get_distance(self):
        # Send trigger pulse
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        # Wait for echo start
        while GPIO.input(self.echo) == 0:
            pulse_start = time.time()

        # Wait for echo end
        while GPIO.input(self.echo) == 1:
            pulse_end = time.time()

        # Calculate distance
        duration = pulse_end - pulse_start
        distance = round(duration * 17150, 2)  
        return distance
