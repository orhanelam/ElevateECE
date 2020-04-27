import math
from DWMTag import DWMTag
from eTaxiBase import eTaxiBase
from imu_integrated_movement import args, getYaw
from MotorControllerUSB import MotorControllerUSB
import threading
import time


class eTaxi_Dima(eTaxiBase):
    # Error Vars
    MAX_POS_ERROR = 6
    MAX_IMU_ERROR_DEG = 3.5
    MAX_IMU_ERROR = (MAX_IMU_ERROR_DEG / 360) * 2 * math.pi

    ACCEPTABLE_TURN_ERROR = 3
    TURN_SPEED = 80
    MOVE_SPEED = 40
    MAX_NUM_TURN_ADJUSTMENTS = 20

    def __init__(self):
        print('initalizing dima bot')
        self.motors = MotorControllerUSB()
        print('motors initalized')
        self.myTag = DWMTag()
        print('DWM tag initialized')
        self.pos_thread = threading.Thread(target=self.update_positioning)
        print('thread created')
        self.pos_thread.start()
        print('eTaxi_Dima Initialized')

    # position is returned in cm
    def get_position(self):
        position = self.myTag.get_pos()
        pos_copy = position.copy()

        return (100*pos_copy[0]), (100*pos_copy[1])

    # distance is in cm
    def move(self, dist_cm):
        self.motors.setSpeed(self.MOVE_SPEED)
        dist_meters = dist_cm/100
        self.motors.move(dist_meters)

    # rads is in radians
    def turn_to_heading(self, rads):
        self.motors.setSpeed(self.TURN_SPEED)
        time.sleep(0.2)
        current_heading = getYaw(args)
        delta = math.degrees(self.angle_between_headings(math.radians(current_heading), rads))
        print('Current heading: ', current_heading)
        print('Delta for initial spin: ', delta)
        count = 0
        while abs(delta) > self.ACCEPTABLE_TURN_ERROR and count < self.MAX_NUM_TURN_ADJUSTMENTS:
            self.motors.turn(-delta)
            time.sleep(2)
            current_heading = getYaw(args)
            delta = math.degrees(self.angle_between_headings(math.radians(current_heading), rads))
            print('Current heading: ', current_heading)
            print('Delta for correction ', count, ' is: ', delta)
            count += 1

    # get heading is returned in radians
    def get_heading(self):
        return math.radians(getYaw(args))

    def update_positioning(self):
        while True:
            self.myTag.update_position()

    def shut_down(self):
        self.myTag.close_serial()
        self.pos_thread.exit()
