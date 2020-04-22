#DWM Serial Parser

import serial
import time
import datetime
import pandas as pd

class DWMTag():
    def __init__(self, port_name="/dev/cu.usbmodem0007600981201"):
        #self.DWM = serial.Serial(port="/dev/cu.usbmodem0007600981201", baudrate=115200)
        #determine port name using this command in terminal: python -m serial.tools.list_ports -v
        self.DWM = serial.Serial(port=port_name, baudrate=115200)
        self.DWM.write("\r\r".encode())
        time.sleep(1)
        self.DWM.write("lec\r".encode())
        time.sleep(1)
        is_not_available = True
        while is_not_available:
            line=self.DWM.readline()
            if(line):
                if len(line)>=5:
                    parse=line.decode().split(",")
                    try:
                        pos_ind = parse.index("POS")
                        if pos_ind is not None:
                            is_not_available = False
                    except Exception as ex:
                        print('connecting...')
        print("Connected to " +self.DWM.name)

    def get_pos(self):
        try:
            line=self.DWM.readline()
            if(line):
                if len(line)>=5:
                    parse=line.decode().split(",")
                    pos_ind = parse.index("POS")
                    tag_pos = {"Timestamp":datetime.datetime.now().strftime("%H:%M:%S"),"X":parse[pos_ind+1], "Y":parse[pos_ind+2], "Z":parse[pos_ind+3]}

                    return tag_pos

                else:
                    print("Distance not calculated: ",line.decode())
                    return
        except Exception as ex:
            print('position unavailable')

    def close_serial(self):
        self.DWM.write("\r".encode())
        self.DWM.close()
        print('Serial connection closed')
        return
