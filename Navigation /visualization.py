import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import math
import time


X_OFFSET_MAX = 80
CM_PER_MOVE = 20

ACCEPTABLE_TURN_ERROR = 2
MAX_NUM_TURN_ADJUSTMENTS = 20

fov_degrees = 10
fov_rad = math.radians(fov_degrees)
search_turn_mag_degrees = fov_degrees/2

def make_plot(x_pos, y_pos, adj_x, adj_y, measured_x, measured_y, target_x, target_y, start_x, start_y, plane_x=None, plane_y=None):
    plt.clf()

    plt.plot(x_pos, y_pos, 'b-')
    plt.plot(adj_x, adj_y, 'go')

    plt.plot(measured_x, measured_y, 'c--')

    plt.plot([target_x], [target_y], 'ro')
    plt.plot([start_x], [start_y], 'mo')
    if plane_x is not None and plane_y is not None:
        plt.plot([plane_x], [plane_y], 'ko')

    plt.show()



def turn_to_center_on_tag(tug, v):
    time.sleep(0.2)
    offset = v.get_x_offset()
    rads_off_by = (offset / X_OFFSET_MAX) * (fov_rad / 2)
    print('Delta for initial spin: ', math.degrees(rads_off_by))
    count = 0
    while abs(rads_off_by) > ACCEPTABLE_TURN_ERROR and count < MAX_NUM_TURN_ADJUSTMENTS:
        if abs(rads_off_by) < 4:
            rads_off_by *= 2
        if rads_off_by < 0:
            tug.turnLeft(rads_off_by)
        else:
            tug.turnRight(rads_off_by)
        time.sleep(0.2)
        offset = v.get_x_offset()
        rads_off_by = (offset / X_OFFSET_MAX) * (fov_rad / 2)
        print('Delta for correction ', count, ' is: ', rads_off_by)
        count += 1
    if count == MAX_NUM_TURN_ADJUSTMENTS:
        print('HIT MAX NUMBER OF TURN ADJUSTMENTS')