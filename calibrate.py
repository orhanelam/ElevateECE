import time
from motorController import motorController

power = 100
x = motorController()


x.turnRight(360, power)
time.sleep(1)
x.turn(False, 360, power)
time.sleep(1)
x.turnLeft(360, power)
time.sleep(1)
x.turn(True, 360, power)
time.sleep(1)
x.move(200, power)

