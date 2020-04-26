import math
from DWMTag import DWMTag
from eTaxiBase import eTaxiBase
from motorController import motorController
import threading

from H7Camera import H7Camera


class eTaxi_Lucas(eTaxiBase):
    # Error Vars
    MAX_POS_ERROR = 10
    MAX_IMU_ERROR_DEG = 0.05
    MAX_IMU_ERROR = (MAX_IMU_ERROR_DEG / 360) * 2 * math.pi

    TURN_SPEED = 100
    MOVE_SPEED = 100

    heading = 0.0

    motors = None

    def __init__(self):
        self.motors = motorController()
        self.cameras = []
        self.cameras.append(H7Camera(port_name="/dev/ttyACM1"))
        #self.cameras.append(H7Camera(port_name="/dev/ttyACM1"))
        
        MV_thread = threading.Thread(target=self.update_openMV)
        MV_thread.start()
        print('eTaxi_Lucas Initialized')

    def get_position(self):
        position = self.myTag.get_pos()
        return position[0], position[1]

    def move(self, dist):
        self.motors.move(dist, self.MOVE_SPEED)

    def turn_to_heading(self, rads):
        delta = self.angle_between_headings(math.radians(self.heading), rads)
        if delta < 0:
            self.motors.turnRight(math.degrees(abs(delta)), self.TURN_SPEED)
        else:
            self.motors.turnLeft(math.degrees(abs(delta)), self.TURN_SPEED)
        self.heading = rads

    def get_motors(self):
        return self.motors

    def get_heading(self):
        return self.heading

    def update_openMV(self):
        x = 0
        while x < 10:
            for camera in self.cameras:
                print("update start")
                camera.update()
                x += 1







