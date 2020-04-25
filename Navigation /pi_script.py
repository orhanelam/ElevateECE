# This example shows how to use the USB VCP class to send an image to PC on demand.
# Host Code
#
#!/usr/bin/env python2.7
import sys, serial, struct
import time

port = '/dev/ttyACM0'
portB = '/dev/ttyACM1'

TAG_PRESENT = False
TAG_X_OFFSET = 0.0
TAG_Z = 0.0
TRUST_READING = False

def cam_mand(serialcmd, port='/dev/ttyACM0'):
    sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
            xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=5000, dsrdtr=True)
    sp.setDTR(True) # dsrdtr is ignored on Windows.
    sp.write(serialcmd.encode())
    sp.flush()
    result = struct.unpack('<L', sp.read(4))[0]
    #result = sp.read(size)
    sp.close()
    return result

def get_photo():
    serialcmd="snap"
    sp = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
            xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)
    sp.setDTR(True) # dsrdtr is ignored on Windows.
    sp.write(serialcmd.encode())
    sp.flush()
    size = struct.unpack('<L', sp.read(4))[0]
    img = sp.read(size)
    sp.close()
    
    with open("img.jpg", "wb") as f:
        f.write(img)

def get_z():
    global TAG_Z
    TAG_Z = cam_mand("getz")

def get_x():
    global TAG_X_OFFSET
    TAG_X_OFFSET = cam_mand("getx")

def tag_present():
    global TAG_PRESENT
    TAG_PRESENT = cam_mand("find")

def trust_reading():
    global TRUST_READING
    TRUST_READING = cam_mand("trst")

def test():
    return cam_mand("test")



