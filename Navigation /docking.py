import math
from motorController import motorController


X_OFFSET_MAX = 80
CM_PER_MOVE = 20
motors = motorController()


TURN_SPEED = 100
MOVE_SPEED = 100

fov_degrees = 10
fov_rad = math.radians(fov_degrees)


def dock_v1():
    if tag_present(): # change this to real tag_present
        offset = tag_x_offset() # change this to real tag_x_offset
        degrees_off_from_tag_heading = (offset/X_OFFSET_MAX)*fov_degrees
        if offset < 0:
            motors.turn_left(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turn_right(degrees_off_from_tag_heading, TURN_SPEED)
        while not trust_reading(): # change this to real trust_reading()
            motors.move(CM_PER_MOVE, MOVE_SPEED)

        if offset < 0:
            motors.turn_right(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turn_left(degrees_off_from_tag_heading, TURN_SPEED)