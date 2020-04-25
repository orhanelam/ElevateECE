import random
import math

# eTaxi Variables
from imu_integrated_movement import args, getYaw
from motorController import motorController

x_pos = 0.0
y_pos = 1000.0
adj_target_x_pos = 0.0
adj_target_y_pos = 0.0
heading = 0.0
IMU_heading = 0.0

# Error Vars
MAX_POS_ERROR = 10
MAX_IMU_ERROR_DEG = 0.05
MAX_IMU_ERROR = (MAX_IMU_ERROR_DEG/360) * 2*math.pi
ACCEPTABLE_TURN_ERROR_DEG = 3
ACCEPTABLE_TURN_ERROR = math.radians(ACCEPTABLE_TURN_ERROR_DEG)

motors = motorController()

TURN_SPEED = 100
MOVE_SPEED = 100


def get_position():
    rad_error = (random.randint(0, 100)/100) * 2*math.pi
    dist_error = random.randint(0, MAX_POS_ERROR)
    x_error = dist_error * math.cos(rad_error)
    y_error = dist_error * math.sin(rad_error)
    # print('x_pos_error: ', x_error, ' y_pos_error: ', y_error)
    return (x_pos + x_error), (y_pos + y_error)


def move(dist):
    global x_pos, y_pos
    x_diff = dist * math.cos(heading)
    y_diff = dist * math.sin(heading)
    x_pos += x_diff
    y_pos += y_diff
    # print("x_pos: ", x_pos, " y_pos: ", y_pos)


def turn_to_heading(rads, real=False):
    if real:
        turn_to_heading_real(rads)
    else:
        turn_to_heading_sim(rads)


def turn_to_heading_real(rads):
    current_heading = getYaw(args)
    delta = angle_between_headings(math.radians(current_heading), rads)
    count = 0
    while delta > ACCEPTABLE_TURN_ERROR and count < 10:
        if delta < 0:
            motors.turnRight(math.degrees(abs(delta)), TURN_SPEED)
        else:
            motors.turnLeft(math.degrees(abs(delta)), TURN_SPEED)
        current_heading = getYaw(args)
        delta = angle_between_headings(math.radians(current_heading), rads)
        count += 1


def turn_to_heading_sim(rads):
    global heading, IMU_heading
    IMU_heading = rads if rads < 2 * math.pi else rads - (2 * math.pi)
    error = ((random.randint(0, 200) - 100) / 100) * MAX_IMU_ERROR
    heading = rads + error if rads + error < 2 * math.pi else rads + error - (2 * math.pi)

    print('bot heading: ', math.degrees(heading))
    print('IMU_heading: ', math.degrees(IMU_heading))
    # print('IMU skew is: ', error)
    # print('Heading: ', heading)


def get_imu_heading():
    print('apparent heading is: ', math.degrees(IMU_heading))
    return IMU_heading


def set_true_position(new_x, new_y):
    global x_pos, y_pos
    x_pos = new_x
    y_pos = new_y


def set_true_heading(new_heading):
    global heading
    heading = new_heading


def get_true_position():
    return x_pos, y_pos


def get_true_heading():
    return heading


def angle_between_headings(angle_1, angle_2):
    wrapped_delta = abs(angle_1 - angle_2) % 2*math.pi
    shortest_delta = 2*math.pi - wrapped_delta if wrapped_delta > math.pi else wrapped_delta
    sign = 1 if (angle_1 - angle_2 >= 0 and angle_1 - angle_2 <= math.pi) \
                or (angle_1 - angle_2 <= -math.pi and angle_1 - angle_2 >= -2*math.pi) else -1
    shortest_delta *= sign
    return shortest_delta