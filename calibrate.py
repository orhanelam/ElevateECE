import time
from motorController import motorController

x = motorController()

x.turnRight(360, 100)
time.sleep(1000)
x.turn(False, 360, 100)
time.sleep(1000)
x.turnLeft(360, 100)
time.sleep(1000)
x.turn(True, 360, 100)
time.sleep(1000)
x.move(200, 100)
