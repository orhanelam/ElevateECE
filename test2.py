import time
from motorController import motorController

power = -100
x = motorController()

while(True):
    x.turnRight(90,power)
    time.sleep(1)
    #print("here")
    x.move(3, power)
    time.sleep(5)
