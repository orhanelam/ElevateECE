import time
from MotorControllerUSB import MotorControllerUSB

x = MotorControllerUSB()


x.setSpeed(100)
time.sleep(5)
x.turn(90)

x.setSpeed(90)
time.sleep(5)
x.turn(90)

x.setSpeed(80)
time.sleep(5)
x.turn(90)

# x.setSpeed(100)
# time.sleep(15)
# x.move(1.5)
# 
# x.setSpeed(90)
# time.sleep(15)
# x.move(1.5)
# 
# x.setSpeed(80)
# time.sleep(15)
# x.move(1.5)