import math
import time

from eTaxi_Lucas import eTaxi_Lucas

X_OFFSET_MAX = 80
CM_PER_MOVE = 3


fov_degrees = 10
fov_rad = math.radians(fov_degrees)
search_turn_mag_degrees = fov_degrees/6


def dock_v2():
    print('Dock_v1')
    tug = eTaxi_Lucas()
    time.sleep(0.5)

    while not tug.cameras[0].get_tag_present():
       x = 3
    if tug.cameras[0].get_tag_present():
        print("Tag is present")
        offset = tug.cameras[0].get_x_offset()
        print('offset: ', offset)
        degrees_off_from_tag_heading = (offset / X_OFFSET_MAX) * (fov_rad / 2)
        print('degree turn: ', degrees_off_from_tag_heading)
        # turn bot so tag is symmetrically in opposite side of FOV
        if offset < 0:
            tug.turnLeft(2*abs(degrees_off_from_tag_heading))
        else:
            tug.turnRight(2*abs(degrees_off_from_tag_heading))

        while not tug.cameras[0].get_trust_reading():
            if tug.cameras[0].get_tag_present():
                print("CM1")
                tug.move(CM_PER_MOVE)
                offset_current = tug.cameras[0].get_x_offset()
                offset_delta = -offset - offset_current
                degrees_off_from_tag_heading = (offset_delta / X_OFFSET_MAX) * (fov_rad / 2)
                if offset_delta > 0:
                    tug.turnRight(abs(degrees_off_from_tag_heading))
                else:
                    tug.turnLeft(abs(degrees_off_from_tag_heading))
                time.sleep(1)
            else:
                if offset < 0:
                    tug.turnRight(search_turn_mag_degrees)
                else:
                    tug.turnLeft(search_turn_mag_degrees)
                time.sleep(3)
        time.sleep(1)
        distance = distance_to_travel_for_perp_intercept(tug)
        print("m1")
        print('alignment to perp move dist: ', distance)
        tug.move(distance)
        tug.turn_to_heading(0)
        tag_z_distance = tug.cameras[0].get_z()
        # print("m2")
        # tug.move(-tag_z_distance*2/3)


# all angles should be in radians
def distance_to_travel_for_perp_intercept(eTaxi):
    time.sleep(3)
    if eTaxi.cameras[0].get_tag_present():
        distance_to_tag = eTaxi.cameras[0].get_z()
        print('z to tag: ', distance_to_tag)
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

