import math
import time

from eTaxi_Lucas import eTaxi_Lucas

X_OFFSET_MAX = 80
CM_PER_MOVE = 3

TURN_SPEED = 80

fov_degrees = 10
fov_rad = math.radians(fov_degrees)
search_turn_mag_degrees = fov_degrees/6


def dock_v2():
    print('Dock_v1')
    tug = eTaxi_Lucas()
    time.sleep(0.5)

    while not tug.cameras[0].get_tag_present():
        print('looking for tag')
        print('THREAD_TEST through getter: ', tug.cameras[0].get_thread_test())
    if tug.cameras[0].get_tag_present():
        print("Tag is present")
        offset = tug.cameras[0].get_x_offset()
        print('offset: ', offset)
        degrees_off_from_tag_heading = (offset / X_OFFSET_MAX) * (fov_degrees / 2)
        print('degree turn: ', degrees_off_from_tag_heading)
        # turn bot so tag is symmetrically in opposite side of FOV
        if offset < 0:
            tug.get_motors().turnLeft(2*degrees_off_from_tag_heading, TURN_SPEED)
        else:
            tug.get_motors().turnRight(2*degrees_off_from_tag_heading, TURN_SPEED)

        while not tug.cameras[0].get_trust_reading() and not distance_to_travel_for_perp_intercept(tug):
            if tug.cameras[0].get_tag_present():
                print("CM1")
                tug.move(CM_PER_MOVE)
                offset_current = tug.cameras[0].get_x_offset()
                offset_delta = -offset - offset_current
                degrees_off_from_tag_heading = (offset_delta / X_OFFSET_MAX) * (fov_degrees / 2)
                if offset_delta > 0:
                    tug.get_motors().turnLeft(degrees_off_from_tag_heading, TURN_SPEED)
                else:
                    tug.get_motors().turnRight(degrees_off_from_tag_heading, TURN_SPEED)
                time.sleep(1)
            else:
                if offset < 0:
                    tug.get_motors().turnRight(search_turn_mag_degrees, TURN_SPEED)
                else:
                    tug.get_motors().turnLeft(search_turn_mag_degrees, TURN_SPEED)
                time.sleep(3)
        distance = distance_to_travel_for_perp_intercept(tug)
        print("m1")
        tug.move(-1*distance)
        tug.turn_to_heading(0)
        tag_z_distance = tug.cameras[0].get_z()
        # print("m2")
        # tug.move(-tag_z_distance*2/3)



# all angles should be in radians
def distance_to_travel_for_perp_intercept(eTaxi):
    time.sleep(3)
    if eTaxi.cameras[0].get_tag_present():
        distance_to_tag = eTaxi.cameras[0].get_z()
        offset = eTaxi.cameras[0].get_x_offset()
        theta = (offset / X_OFFSET_MAX) * (fov_rad / 2)
        psi = abs(eTaxi.angle_between_headings(0, eTaxi.get_heading()))
        distance_1 = distance_to_tag * math.cos(theta)
        if psi < math.pi/2:
            distance_2 = (distance_to_tag * math.sin(theta) * math.tan(psi-(math.pi/2)))
        else:
            distance_2 = -(distance_to_tag * math.sin(theta) * math.tan((math.pi/2)- psi))
        return distance_1 + distance_2
    return 0
                


dock_v2()

