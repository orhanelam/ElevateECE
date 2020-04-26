import random
import math


# eVTOL Position

from eTaxi_Lucas import get_true_position, get_imu_heading, angle_between_headings, MOVE_SPEED, TURN_SPEED
from motorController import motorController
from navigation_control import turn_to_heading

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


