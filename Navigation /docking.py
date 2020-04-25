import math
import threading
import time
from motorController import motorController
from pi_script import tag_present, trust_reading, get_x, TAG_PRESENT, TAG_X_OFFSET, TRUST_READING

X_OFFSET_MAX = 80
CM_PER_MOVE = 20
motors = motorController()


TURN_SPEED = 100
MOVE_SPEED = 100

fov_degrees = 10
fov_rad = math.radians(fov_degrees)


def dock_v1():
    initalize_openMV()
    time.sleep(0.3)
    if TAG_PRESENT:
        offset = TAG_X_OFFSET
        degrees_off_from_tag_heading = (offset/X_OFFSET_MAX)*fov_degrees
        if offset < 0:
            motors.turn_left(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turn_right(degrees_off_from_tag_heading, TURN_SPEED)
        while not TRUST_READING:
            motors.move(CM_PER_MOVE, MOVE_SPEED)

        if offset < 0:
            motors.turn_right(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turn_left(degrees_off_from_tag_heading, TURN_SPEED)


def initalize_openMV():
    MV_update_thread = threading.Thread(target=update_openMV)
    MV_update_thread.start()


def update_openMV():
    while True:
        tag_present()
        trust_reading()
        get_x()