import SerialMotor as S
import time

sm = S.SerialMotor("/dev/ttyACM0")
x = 100

while x > 0: 
    sm.set_motor(4,.7) # right motor to full forward
    time.sleep(3)
    sm.set_motor(4,0)
    print('F')
    sm.set_motor(3, .7)
    time.sleep(3)
    sm.set_motor(3,0)
    time.sleep(3)
    
    x = x - 1
    print(x)

# first arg is port number (3 for left, 4 for right)
# second arg is power, a float in range -1 .. +1
# FYI, "/dev/ttyUSB0" is the device for the first (and in our case, only) USB-connected serial port