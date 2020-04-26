# This example shows how to use the USB VCP class to send an image to PC on demand.
# Host Code
#
#!/usr/bin/env python2.7
import sys, serial, struct
import time


class H7Camera():
    def __init__(self, port_name="/dev/ttyACM0"):
        #Exact port name may vary
        self.port = port_name
        
        self.tag_present = False
        self.x_offset = 0.0
        self.z = 0.0
        self.trust_reading = False
        self.test = 0.0
        self.thread_test = 0

    def cam_mand(serialcmd):
        sp = serial.Serial(self.port_name, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=5000, dsrdtr=True)
        sp.setDTR(True) # dsrdtr is ignored on Windows.
        sp.write(serialcmd.encode())
        sp.flush()
        result = struct.unpack('<L', sp.read(4))[0]
        sp.close()
        return result

    def get_photo():
        serialcmd="snap"
        sp = serial.Serial(self.port_name, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=None, dsrdtr=True)
        sp.setDTR(True) # dsrdtr is ignored on Windows.
        sp.write(serialcmd.encode())
        sp.flush()
        size = struct.unpack('<L', sp.read(4))[0]
        img = sp.read(size)
        sp.close()
        
        with open("img.jpg", "wb") as f:
            f.write(img)


# update calls used by eTaxi_Lucas

    def update_z():
        self.z = cam_mand("getz")

    def update_x_offset():
        self.tag_x_offset = cam_mand("getx")

    def update_tag_present():
        self.tag_present = cam_mand("find")

    def update_trust_reading():
        self.trust_reading = cam_mand("trst")

    def update_test():
        self.test = cam_mand("test")

    def update_thread_test():
        self.thread_test += 1
        
    def update(self):
        update_z()
        update_x_offset()
        update_tag_present()
        update_trust_reading()
        update_test()
        update_thread_test()
        
# get methods will be used by docking script

    def get_z(self):
        return self.tag_z
    
    def get_x_offset(self):
        return self.tag_x_offset

    def get_tag_present(self):
        return self.tag_present

    def get_trust_reading(self):
        return self.trust_reading

    def get_test(self):
        return self.test
    
    def get_thread_test(self):
        return self.thread_test



