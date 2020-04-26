# This example shows how to use the USB VCP class to send an image to PC on demand.
# Host Code
#
#!/usr/bin/env python2.7
import sys, serial, struct
import time


class H7Camera():
    def __init__(self, port_name="/dev/ttyACM0"):
        #Exact port name may vary
        self.port_name = port_name
        
        self.tag_present = False
        self.x_offset = 0.0
        self.z = 0.0
        self.trust_reading = False
        self.test = 0.0
        self.thread_test = 0

    def cam_mand(self, serialcmd):
        print("c1")
        sp = serial.Serial(self.port_name, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE, timeout=5000, dsrdtr=True)
        print("c2")
        sp.setDTR(True) # dsrdtr is ignored on Windows.
        sp.write(serialcmd.encode())
        print("c3")
        sp.flush()
        print("c4")
        result = struct.unpack('<L', sp.read(4))[0]
        print("c5")
        sp.close()
        print("c6")
        return result

    def get_photo(self):
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

    def update_z(self):
        self.z = self.cam_mand("getz")

    def update_x_offset(self):
        self.tag_x_offset = self.cam_mand("getx")

    def update_tag_present(self):
        self.tag_present = self.cam_mand("find")

    def update_trust_reading(self):
        self.trust_reading = self.cam_mand("trst")

    def increment(self, num):
        bigger = num+2
        return bigger
    
    def update_test(self):
        self.test = self.cam_mand("test")

    def update_thread_test(self):
        self.thread_test += 1 #only this works, arithmetic. nested function fails
        
    def update(self):
        self.update_z()
        self.update_x_offset()
        self.update_tag_present()
        self.update_trust_reading()
        self.update_test()
        self.update_thread_test()
        
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


# v = H7Camera(port_name="/dev/ttyACM1")
# v.update_test()
# print(v.get_test())

