import time
from motorController import motorController

power = 90
x = motorController()

while(True):
    x.turnRight(90,90)
    time.sleep(1)
    #print("here")
    x.move(1, -90)
    time.sleep(5)
