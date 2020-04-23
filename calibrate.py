import time
from motorController import motorController

x = motorController()

x.turnRight(360, 100)
time.sleep(1)
x.turn(False, 360, 100)
time.sleep(1)
x.turnLeft(360, 100)
time.sleep(1)
x.turn(True, 360, 100)
time.sleep(1)
x.move(200, 100)
