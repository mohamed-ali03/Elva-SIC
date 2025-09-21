from dcmotor import DCMotor
import time


motor = DCMotor(2,3)


while True :
    print("f --> Forward\nb --> Backword\ns --> Stop")
    command = input("Which direction do you need to move (f,b,s) : ")

    if command == 'f':
        motor.moveForward()
    elif command == 'b':
        motor.moveBackward()
    elif command == 's':
        motor.stop()
    else:
        print("Invaild Input! Please try again")

