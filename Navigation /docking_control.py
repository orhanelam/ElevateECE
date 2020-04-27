import math
import time

from eTaxi_Lucas import eTaxi_Lucas
from H7Camera import H7Camera

X_OFFSET_MAX = 80
CM_PER_MOVE = 20


fov_degrees = 10
fov_rad = math.radians(fov_degrees)
search_turn_mag_degrees = fov_degrees/2


def dock_v2():
    print('Dock_v1')
    tug = eTaxi_Lucas()
    time.sleep(0.5)
    
    v = H7Camera(port_name="/dev/ttyACM0")


# This runs
    iii = 0
    while iii < 6:
        while v.get_tag_present() and v.get_z() > 20:
            if v.get_tag_present():
                print(v.get_test())
                print(v.get_z())

                print(v.get_x_offset())
        iii += 1
# -------------------------------



# This does not run

    while not (v.get_trust_reading() and v.get_z() < 150):
        if v.get_tag_present():
            #print("CM1")
            #tug.move(CM_PER_MOVE)
            offset_current = v.get_x_offset()
            print(offset_current)

        else:
            print('attempting to find tag')

# ------------------------------------------

## you cannot run 2 heavy computations in a single while loop

    while not v.get_tag_present():
       print("No tag")
       
    if v.get_tag_present():
        print("Tag is present")
        offset = v.get_x_offset()
        print('offset: ', offset)
        rads_off_from_tag_heading = (offset / X_OFFSET_MAX) * (fov_rad / 2)
        #print('degree turn: ', math.degrees(rads_off_from_tag_heading))
        # turn bot so tag is symmetrically in opposite side of FOV
        if rads_off_from_tag_heading < 1000:
            if offset < 0:
                tug.turnLeft(2*abs(rads_off_from_tag_heading))
            else:
                tug.turnRight(2*abs(rads_off_from_tag_heading))
        else:
            print('crazy turn requested')

    while not (v.get_trust_reading() and v.get_z() < 150):
        time.sleep(3)
        if v.get_tag_present():
            print("CM1")
            #tug.move(CM_PER_MOVE)
            offset_current = v.get_x_offset()
            print(offset_current)
            offset_delta = -offset - offset_current
            #rads_off_from_tag_heading = (offset_delta / X_OFFSET_MAX) * (fov_rad / 2)
            #print('offset-delta: ', offset_delta)
            if rads_off_from_tag_heading < 1000:
                if offset_delta > 0:
                    tug.turnRight(abs(rads_off_from_tag_heading))
                else:
                    tug.turnLeft(abs(rads_off_from_tag_heading))
            else:
                print('crazy turn requested')
            time.sleep(1)
        else:
            print('attempting to find tag')
            if offset < 0:
                tug.turnRight(search_turn_mag_degrees)
            else:
                tug.turnLeft(search_turn_mag_degrees)
    
    time.sleep(5)
    final_z = v.get_z()
    distance = distance_to_travel_for_perp_intercept(tug, v, final_z)
    while distance > 500:
        print('bad z: ', distance)
        time.sleep(3)
        distance = distance_to_travel_for_perp_intercept(tug, v, final_z)

    print("m1")
    print('alignment to perp move dist: ', distance)
    time.sleep(5)
    #tug.move(distance)
    #tug.turn_to_heading(0)
    # tag_z_distance = tug.cameras[0].get_z()
    # print("m2")
    # tug.move(-tag_z_distance*2/3)


# all angles should be in radians
def distance_to_travel_for_perp_intercept(tug, v, z_dist):
    time.sleep(3)
    if v.get_tag_present():
        time.sleep(0.5)
        distance_to_tag = z_dist
        print('z to tag: ', distance_to_tag)
        offset = v.get_x_offset()
        theta_1 = (offset / X_OFFSET_MAX) * (fov_rad / 2)
        psi_2 = abs(tug.angle_between_headings(0, tug.get_heading()))
        distance_1 = distance_to_tag * math.cos(theta_1)
        print('distance_1: ', distance_1)
        if psi_2 < math.pi/2:
            distance_2 = -(distance_to_tag * math.sin(theta_1) * math.tan((math.pi/2) - psi_2))
            print('distance_2.1: ', distance_2)
        else:
            psi_1 = math.pi - psi_2
            distance_2 = (distance_to_tag * math.sin(theta_1) * math.tan((math.pi/2) - psi_1))
            print('distance_2.2: ', distance_2)

        return distance_1 + distance_2
    return 0


dock_v2()

