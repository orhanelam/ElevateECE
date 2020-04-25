import random
import math


# eVTOL Position
from numpy.core.umath import sign

from integration_layer import turn_to_heading

plane_x = 10.0
plane_y = -10.0
plane_heading = 0.0
tag_size = 1 #cm

# bot position, these are true values, no error
x_pos = 0.0
y_pos = 0.0
heading = -math.pi/4
fov_degrees = 10
fov = math.radians(fov_degrees)


# sensor variables
MAX_ACCURATE_DETECT_RANGE = 350
ERROR_MAG = 3
X_OFFSET_MAX = 100


def dock():
    turn_to_heading(plane_heading + math.pi)
    if tag_present():
        print('tag acquired!!!!!')


# standardized form -100 as far right, 0 is center, and 100 far left
def tag_x_offset():
    if tag_present():
        delta_x = plane_x - x_pos
        delta_y = plane_y - y_pos
        plane_angle_from_xaxis = math.atan(delta_y / delta_x)
        angle_delta = angle_between_headings(heading, plane_angle_from_xaxis)
        if angle_delta <= fov/2:
            percent_offset = angle_delta/(fov/2)
            return percent_offset * X_OFFSET_MAX * sign(angle_delta)
        else:
            print("something went wrong")
    else:
        print('Error: Tag not found, no offset data available')


def tag_z_distance():
    delta_x = plane_x - x_pos
    delta_y = plane_y - y_pos
    dist = math.sqrt(delta_x**2 + delta_y**2)
    if dist < MAX_ACCURATE_DETECT_RANGE:
        error = (random.randrange(0, 2*ERROR_MAG) - ERROR_MAG)
        return dist + error
    else:
        return random.randrange(100, 400)


def trust_reading():
    delta_x = plane_x - x_pos
    delta_y = plane_y - y_pos
    dist = math.sqrt(delta_x ** 2 + delta_y ** 2)
    return dist <= MAX_ACCURATE_DETECT_RANGE


# this needs to be fixed
def tag_present():
    delta_x = (plane_x - x_pos) + tag_size/2
    delta_y = plane_y - y_pos
    plane_angle_from_xaxis = math.atan(delta_y/delta_x)
    return angle_between_headings(heading, plane_angle_from_xaxis) <= fov/2


def angle_between_headings(angle_1, angle_2):
    wrapped_delta = abs(angle_1- angle_2) % 360
    shortest_delta = 2*math.pi - wrapped_delta if wrapped_delta > math.pi else wrapped_delta
    sign = 1 if (angle_1 - angle_2 >= 0 and angle_1 - angle_2 <= 180) \
                or (angle_1 - angle_2 <= -180 and angle_1 - angle_2 >= -360) else -1
    shortest_delta *= sign
    print('Angle Delta: ', math.degrees(shortest_delta))
    return  shortest_delta