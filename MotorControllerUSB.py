import RPi.GPIO as GPIO
import time
import SerialMotor as S

sm = S.SerialMotor("/dev/ttyUSB0")

class MotorControllerUSB:
        
    def setSpeed(self, speed):
        #speed is a percentage ---> 50 is 50% speed, 100 is 100% speed
        self.speed = speed/100
        
    
    def turn(self, degrees):
        consistentError = 0.15
        turnConstant = 0.18 + consistentError*(1-self.speed)
        degreesToTime = turnConstant * (abs(degrees)/90) / (self.speed)       
        if (degrees < 0):
            time.sleep(degreesToTime)
            sm.set_motor(3, -self.speed)
            sm.set_motor(4, self.speed)
            time.sleep(degreesToTime)
        else:
            time.sleep(degreesToTime)
            sm.set_motor(3, self.speed)
            sm.set_motor(4, -self.speed)
            time.sleep(degreesToTime)
        sm.set_motor(3, 0)
        sm.set_motor(4, 0)
        
    def move(self, meters):
        moveConstant=0.75
        metersToTime = meters*moveConstant/self.speed
        time.sleep(metersToTime)
        sm.set_motor(3, self.speed)
        sm.set_motor(4, self.speed)
        time.sleep(metersToTime)
        sm.set_motor(3, 0)
        sm.set_motor(4, 0)

            

