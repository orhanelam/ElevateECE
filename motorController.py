import RPi.GPIO as GPIO
import time

class motorController:
    def __init__(self):

        self.turnRatio = 1 #ratio of seconds per degree
        self.moveRation = 1 #ratio of seconds per meter

        # These are the pins for a 2B rasbperry pi, may differ for other models. 
        # https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=105044 to get 
        # pins.

        leftPin = 12
        rightPin = 18

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(leftPin, GPIO.OUT)
        GPIO.setup(rightPin, GPIO.OUT)
        #self.leftMotor
        self.leftMotor = GPIO.PWM(leftPin,250)
        self.leftMotor.start(0)

        #self.rightMotor
        self.rightMotor = GPIO.PWM(rightPin, 250)
        self.rightMotor.start(0)

        

    #left: if true, set left motor, otherwise set right.
    # speedPercentage: -100 to 100, sets direction of motor and percent of max motor    # rotation speed to turn at.
    def turnMotor(self, left, speedPercentage):
        if (speedPercentage > 100):
            speedPercentage = 100
        elif (speedPercentage < -100):
            speedPercentage = -100
        speed = 37.5 + 0.125 * speedPercentage
        if (left):
            self.leftMotor.ChangeDutyCycle(speed)
        else:
            self.rightMotor.ChangeDutyCycle(speed)

    def turn(self, left, degrees, speed):
        self.turnMotor(left, -speed)
        self.turnMotor(not left, speed)
        time.sleep(degrees * self.turnRatio * 100 / speed)
        self.turnMotor(left, 0)
        self.turnMotor(not left, 0)
    
    def turnLeft(self, degrees, speed):
        self.turn(True, degrees, speed)

    def turnRight(self, degrees, speed):
        self.turn(self, False, degrees, speed)

    def move(self, meters, speed):
        self.turnMotor(True, speed)
        self.turnMotor(False, speed)
        time.sleep(meters * self.moveRatio * 100 / speed)
        self.turnMotor(left, 0)
        self.turnMotor(not left, 0)


            