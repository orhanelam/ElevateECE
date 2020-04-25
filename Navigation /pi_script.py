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
TEST = 0.0
THREAD_TEST = 0

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

def update_get_z():
    global TAG_Z
    TAG_Z = cam_mand("getz")

def update_get_x():
    global TAG_X_OFFSET
    TAG_X_OFFSET = cam_mand("getx")

def update_tag_present():
    global TAG_PRESENT
    TAG_PRESENT = cam_mand("find")

def update_trust_reading():
    global TRUST_READING
    TRUST_READING = cam_mand("trst")

def update_test():
    global TEST
    TEST = cam_mand("test")


def test_threading():
    global THREAD_TEST
    THREAD_TEST += 1

def get_THREAD_TEST():
    return THREAD_TEST

def tag_present():
    return TAG_PRESENT

def tag_x_offset():
    return TAG_X_OFFSET

def trust_reading():
    return TRUST_READING

def get_test():
    return TEST



