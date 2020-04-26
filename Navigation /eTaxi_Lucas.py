import math
from DWMTag import DWMTag
from eTaxiBase import eTaxiBase
from motorController import motorController
import threading

from pi_script import update_tag_present, update_trust_reading, update_get_x, update_test, test_threading


class eTaxi_Lucas(eTaxiBase):
    # Error Vars
    MAX_POS_ERROR = 10
    MAX_IMU_ERROR_DEG = 0.05
    MAX_IMU_ERROR = (MAX_IMU_ERROR_DEG / 360) * 2 * math.pi

    TURN_SPEED = 100
    MOVE_SPEED = 100

    heading = 0.0

    def __init__(self):
        self.motors = motorController()
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

    def get_heading(self):
        return self.heading

    def update_openMV(self):
        while True:
            update_tag_present()
            update_trust_reading()
            update_get_x()
            update_test()
            test_threading()





