import math
from DWMTag import DWMTag
from eTaxiBase import eTaxiBase
from imu_integrated_movement import args, getYaw
from MotorControllerUSB import MotorControllerUSB
import threading


class eTaxi_Dima(eTaxiBase):
    # Error Vars
    MAX_POS_ERROR = 10
    MAX_IMU_ERROR_DEG = 0.05
    MAX_IMU_ERROR = (MAX_IMU_ERROR_DEG / 360) * 2 * math.pi

    TURN_SPEED = 100
    MOVE_SPEED = 100

    def __init__(self):
        self.motors = MotorControllerUSB()
        self.myTag = DWMTag()
        pos_thread = threading.Thread(target=self.update_positioning)
        pos_thread.start()
        print('eTaxi_Dima Initialized')

    def get_position(self):
        position = self.myTag.get_pos()
        return position[0], position[1]

    def move(self, dist):
        self.motors.move(dist)

    def turn_to_heading(self, rads):
        current_heading = getYaw(args)
        delta = self.angle_between_headings(math.radians(current_heading), rads)
        count = 0
        while abs(delta) > self.ACCEPTABLE_TURN_ERROR and count < 10:
            self.motors.turn(-math.degrees(delta))
            current_heading = getYaw(args)
            delta = self.angle_between_headings(math.radians(current_heading), rads)
            count += 1

    def get_heading(self):
        return getYaw(args)

    def update_positioning(self):
        while True:
            self.myTag.update_position()




