import serial
import time
import datetime
import pandas as pd

class DWMTag():
    def __init__(self, port_name="/dev/cu.usbmodem0007600981201"):
        #defualt port name from my computer. Different on differnt devices.
        '''
        Opens the serial connection at the given port and writes commands
        to read position from the tag.
        Waits until one position reading is successful before deeming connection successful
        '''
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
        '''
        Returns a dict in the form:
        {'Timestamp': '14:44:14',
        'X': '1.57',
        'Y': '1.18',
        'Z': '0.95'}
        where timestamp is the time at which the position is read from the tag,
        adnd each of X, Y, and Z are the position in meters of the tag.
        '''
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
        '''
        Closes the serial connection.
        '''
        self.DWM.write("\r".encode())
        self.DWM.close()
        print('Serial connection closed')
        return
