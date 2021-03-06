import random
import math
import pi_script as ps
# eVTOL Position

from eTaxi import get_true_position, get_imu_heading
from motorController import motorController
from navigation_control import turn_to_heading

# Cam H7 imports
import sys, serial, struct
import time

port = '/dev/ttyACM0'
portB = '/dev/ttyACM1'

print(ps.test())
print(ps.cam_mand("test", portB))

plane_x = 0.0
plane_y = 0.0
plane_heading = 0.0
tag_size = 1 #cm

# bot position, these are true values, no error

fov_degrees = 10
fov = math.radians(fov_degrees)


# sensor variables
MAX_ACCURATE_DETECT_RANGE = 350
ERROR_MAG = 3
X_OFFSET_MAX = 80

CM_PER_MOVE = 20
TURN_SPEED = 100
MOVE_SPEED = 100

motors = motorController()


def dock_v1():
    if tag_present():
        offset = tag_x_offset()
        degrees_off_from_tag_heading = (offset/X_OFFSET_MAX)*fov
        if offset < 0:
            motors.turn_left(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turn_right(degrees_off_from_tag_heading, TURN_SPEED)
        while not trust_reading():
            motors.move(CM_PER_MOVE, MOVE_SPEED)

        if offset < 0:
            motors.turn_right(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turn_left(degrees_off_from_tag_heading, TURN_SPEED)



def dock(plane_x_in, plane_y_in, plane_heading_in):
    global plane_x, plane_y, plane_heading
    plane_x = plane_x_in
    plane_y = plane_y_in
    plane_heading = plane_heading_in
    print('plane_heading: ', math.degrees(plane_heading_in))
    turn_to_heading(plane_heading + math.pi)
    if tag_present():
        offset = tag_x_offset()
        print('x_offset: ', offset)
    else:
        print('failed to aquire tag')


#
# All  methods below are simulations of real camera mv commands
#

# standardized form -100 as far right, 0 is center, and 100 far left
def tag_x_offset():
    if tag_present():
        x_pos, y_pos = get_true_position()
        delta_x = plane_x - x_pos
        delta_y = plane_y - y_pos
        plane_angle_from_xaxis = math.atan(delta_y / delta_x)
        angle_delta = angle_between_headings(get_imu_heading(), plane_angle_from_xaxis)
        if angle_delta <= fov/2:
            percent_offset = angle_delta/(fov/2)
            return percent_offset * X_OFFSET_MAX
        else:
            print("something went wrong")
    else:
        print('Error: Tag not found, no offset data available')


def tag_z_distance():
    x_pos, y_pos = get_true_position()
    delta_x = plane_x - x_pos
    delta_y = plane_y - y_pos
    dist = math.sqrt(delta_x**2 + delta_y**2)
    if dist < MAX_ACCURATE_DETECT_RANGE:
        error = (random.randrange(0, 2*ERROR_MAG) - ERROR_MAG)
        return dist + error
    else:
        return random.randrange(100, 400)


def trust_reading():
    x_pos, y_pos = get_true_position()
    delta_x = plane_x - x_pos
    delta_y = plane_y - y_pos
    dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
    return dist <= MAX_ACCURATE_DETECT_RANGE


# this needs to be fixed
def tag_present():
    x_pos, y_pos = get_true_position()
    delta_x = (plane_x - x_pos) + tag_size/2
    delta_y = plane_y - y_pos
    plane_angle_from_xaxis = math.atan(delta_y/delta_x)
    print('plane angle from x axis: ', math.degrees(plane_angle_from_xaxis))
    angle_diff = angle_between_headings(get_imu_heading(), plane_angle_from_xaxis)
    print('angle_diff: ', math.degrees(angle_diff))
    return abs(angle_diff) <= fov/2


def angle_between_headings(angle_1, angle_2):
    wrapped_delta = abs(angle_1 - angle_2) % 2*math.pi
    shortest_delta = 2*math.pi - wrapped_delta if wrapped_delta > math.pi else wrapped_delta
    sign = 1 if (angle_1 - angle_2 >= 0 and angle_1 - angle_2 <= math.pi) \
                or (angle_1 - angle_2 <= -math.pi and angle_1 - angle_2 >= -2*math.pi) else -1
    shortest_delta *= sign
    return shortest_delta