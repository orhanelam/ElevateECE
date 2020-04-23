# This example shows how to use the USB VCP class to send an image to PC on demand.
# Host Code
#
#!/usr/bin/env python2.7
import sys, serial, struct
import time

port = '/dev/ttyACM1'



def cam_mand(serialcmd):
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
    return cam_mand("getz")

def get_x():
    return cam_mand("getx")

def tag_present():
    return cam_mand("findtag")

def trust_reading():
    return cam_mand("trust")


tag_present()


