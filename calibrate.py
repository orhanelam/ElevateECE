import time


x = motorController()

x.turnRight(90, 100)
time.sleep(1000)
x.turn(False, 90, 100)
time.sleep(1000)
x.turnLeft(90, 100)
time.sleep(1000)
x.turn(True, 90, 100)
time.sleep(1000)
x.move(2, 100)