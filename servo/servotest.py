from servo import Servo

servomotor = Servo(13)


while True:
    command = input("Input your desired angle [0,180] : ")
    
    if command >= 0 and command <= 180 :
        servomotor.setServoAngle(command)
    else:
        print("Invaild Angle! Please Try again")