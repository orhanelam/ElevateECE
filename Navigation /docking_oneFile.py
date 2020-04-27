import math
import time

from H7Camera import H7Camera
from motorController import motorController

X_OFFSET_MAX = 80
CM_PER_MOVE = 20


ACCEPTABLE_TURN_ERROR_DEGREES = 2
ACCEPTABLE_TURN_ERROR = math.radians(ACCEPTABLE_TURN_ERROR_DEGREES)
MAX_NUM_TURN_ADJUSTMENTS = 20

TURN_SPEED = 80
MOVE_SPEED = -80


fov_degrees = 70
fov_rad = math.radians(fov_degrees)
search_turn_mag_degrees = fov_degrees/2


def dock_one_file():
    print('Dock_v3')
    time.sleep(0.5)

    v = H7Camera(port_name="/dev/ttyACM0")
    motors = motorController()

    print("cam ready")
    # This runs
    #     iii = 0
    #     while iii < 6:
    #         while v.get_tag_present() and v.get_z() > 20:
    #             if v.get_tag_present():
    #                 print(v.get_test())
    #                 print(v.get_z())
    #                 print(v.get_x_offset())
    #         iii += 1
    # -------------------------------
    L = 0
    T = math.pi / 6
    while not v.get_tag_present():
        print('looking for tag')

    print("proceeding")
    #     if v.get_tag_present():
    #         while not v.get_trust_reading():
    #             print("trust check")
    #             tug.move(10)

    offset = v.get_x_offset()
    print("offset :" + str(offset))
    # turn 15 degrees towards tag
    print("turning")
    time.sleep(3)
    if offset < 0:
        motors.turnLeft(math.degrees(T), TURN_SPEED)
        L = 1
    else:
        motors.turnRight(math.degrees(T), TURN_SPEED)

    tag_dist = v.get_z()
    time.sleep(0.5)
    distance_to_tag = tag_dist
    print('z to tag: ', distance_to_tag)
    #         offset = v.get_x_offset()
    print('Internal offset' + str(offset))

    theta_1 = (offset / X_OFFSET_MAX) * (fov_rad / 2)
    psi_2 = math.pi/6
    distance_1 = distance_to_tag * math.cos(theta_1)
    print('distance_1: ', distance_1)
    if psi_2 < math.pi / 2:
        distance_2 = -(distance_to_tag * math.sin(theta_1) * math.tan((math.pi / 2) - psi_2))
        print('distance_2.1: ', distance_2)
    else:
        psi_1 = math.pi - psi_2
        distance_2 = (distance_to_tag * math.sin(theta_1) * math.tan((math.pi / 2) - psi_1))
        print('distance_2.2: ', distance_2)

    distance = distance_1 + distance_2

    print('distance: ' + str(distance))
    time.sleep(3)
    if (distance > 80):
        print("bad distance: " + str(distance))
        return

    dist_m = distance / 100
    motors.move(dist_m, MOVE_SPEED)

    if L:
        motors.turnRight(math.degrees(T), TURN_SPEED)
    else:
        motors.turnLeft(math.degrees(T), TURN_SPEED)

    # tug.turn_to_heading(0)
    #     tag_dist = v.get_z()
    #     print("final approach:"+str(tag_dist))
    #
    time.sleep(3)
    offset2 = v.get_x_offset()
    print("offset2: " + str(offset2))
    rads_off_by = (offset2 / X_OFFSET_MAX) * (fov_rad / 2)
    print('Delta for initial spin: ', math.degrees(rads_off_by))

    if abs(rads_off_by) < 4:
        rads_off_by *= 2
    if rads_off_by < 0:
        motors.turnLeft(math.degrees(abs(rads_off_by)), TURN_SPEED)
    else:
        motors.turnRight(math.degrees(abs(rads_off_by)), TURN_SPEED)

    while (tag_dist > 20):
        dist_m = 10 / 100
        motors.move(dist_m, MOVE_SPEED)
        tag_dist = v.get_z()
        print(tag_dist)

    print(tag_dist)


dock_one_file()
