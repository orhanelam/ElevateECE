import SerialMotor as S


sm = S.SerialMotor("/dev/ttyUSB0")
sm.set_motor(4,1) # right motor to full forward
# first arg is port number (3 for left, 4 for right)
# second arg is power, a float in range -1 .. +1
# FYI, "/dev/ttyUSB0" is the device for the first (and in our case, only) USB-connected serial port