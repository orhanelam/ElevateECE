import math
import time

from eTaxi_Lucas import eTaxi_Lucas
from pi_script import get_THREAD_TEST, tag_present, tag_x_offset, trust_reading

X_OFFSET_MAX = 80
CM_PER_MOVE = 20


TURN_SPEED = 50
MOVE_SPEED = 100


fov_degrees = 10
fov_rad = math.radians(fov_degrees)


def dock_v1():
    print('Dock_v1')
    tug = eTaxi_Lucas()
    time.sleep(0.5)
    while not tag_present():
        print('looking for tag')
        print('THREAD_TEST through getter: ', get_THREAD_TEST())
    if tag_present():
        print("Tag is present")
        offset = tag_x_offset()
        print('offset: ', offset)
        degrees_off_from_tag_heading = (offset/X_OFFSET_MAX)*(fov_degrees/2)
        print('degree turn: ', degrees_off_from_tag_heading)
        if offset < 0:
            tug.get_motors().turnLeft(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            tug.get_motors().turnRight(degrees_off_from_tag_heading, TURN_SPEED)
        print('Bot just turned hopefully')
        while not trust_reading():
            tug.get_motors().move(CM_PER_MOVE, MOVE_SPEED)
        print('bot just moved')
        if offset < 0:
            tug.get_motors().turnRight(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            tug.get_motors().turnLeft(degrees_off_from_tag_heading, TURN_SPEED)
        print('done')


dock_v1()

