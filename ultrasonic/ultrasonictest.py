from ultrasonic import Ultrasonic


ultra = Ultrasonic(4,5)

while True:
    distance = ultra.get_distance()
    print(f"Distance = {distance}")