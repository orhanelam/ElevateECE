import math
import time
# Target
from eTaxi_Simulated import eTaxi_Simulated
from visualization import make_plot


target_x_pos = 2500.2
target_y_pos = 10.2
start_x_pos = 0.0
start_y_pos = 0.0
PLANE_HEADING = 0.0

# Config vars
TARGET_TOLERANCE = 20
ANGLE_ADJUST_CONSTANT = 1 # multiplier, 1 has no effect
MAX_NUM_STEPS = 90000
METERS_PER_MOVE = .4
CM_PER_MOVE = METERS_PER_MOVE * 100
MIN_MOVE_SIZE = 0.1
TARGET_DIST_FROM_PLANE = 0

# Logging Vars
STEPS_PER_DATAPOINT = 5


def navigate_bot(eTaxi, way_points, plot=False):
    global target_x_pos, target_y_pos

    full_rec_x = []
    full_rec_y = []
    full_adj_x = []
    full_adj_y = []
    target_point_x = []
    target_point_y = []

    count = 1
    for point in way_points:
        target_x_pos = point[0]
        target_y_pos = point[1]
        step_count, rec_x, rec_y, adj_x, adj_y, measured_x, measured_y, defined_start_x, defined_start_y = drive_to_target(eTaxi, step_limit=MAX_NUM_STEPS, bulk_test=True)
        if step_count >= MAX_NUM_STEPS:
            print('FAILURE!')
        full_rec_x += rec_x
        full_rec_y += rec_y
        full_adj_x += adj_x
        full_adj_y += adj_y
        target_point_x += [defined_start_x]
        target_point_y += [defined_start_y]
        print('REACHED POSITION: ', count)
        print('position: ', eTaxi.get_position(), 'heading: ', math.degrees(eTaxi.get_heading()))
        count += 1
    if plot:
        make_plot(full_rec_x, full_rec_y, full_adj_x, full_adj_y, target_point_x, target_point_y, target_x_pos, target_y_pos, start_x_pos, start_y_pos)


# grid is quad I, 0 degree is parrallel to x axis
def drive_to_target(eTaxi, step_limit=float('inf'), bulk_test=False):
    global start_x_pos, start_y_pos

    # variables used for plotting
    recorded_x_pos = []
    recorded_y_pos = []
    angle_adjust_x_pos = []
    angle_adjust_y_pos = []
    measured_x_pos = []
    measured_y_pos = []

    # get current heading and adjust to point to target
    set_start_position(eTaxi)
    adjust_heading(eTaxi, start_x_pos, start_y_pos)
    print('pointing at target')
    print('current_pos: ', start_x_pos, start_y_pos)
    print('target_pos: ', target_x_pos, target_y_pos)
    print('line angle: ', get_line_angle())

    count = 0
    loc_x = start_x_pos
    loc_y = start_y_pos
    while not in_tolerance_of_target(loc_x, loc_y) and count < step_limit:
        drift_dist, loc_x, loc_y = dist_from_line(eTaxi)
        print('Current Bot Location: ', loc_x, loc_y)
        if drift_dist > eTaxi.MAX_POS_ERROR:
            adjust_heading(eTaxi, loc_x, loc_y)
            angle_adjust_x_pos.append(loc_x)
            angle_adjust_y_pos.append(loc_y)
            measured_x_pos.append(loc_x)
            measured_y_pos.append(loc_y)

        target_delta = dist_from_target(loc_x, loc_y)
        if target_delta < CM_PER_MOVE:
            if target_delta/2 > MIN_MOVE_SIZE:
                eTaxi.move(target_delta/2)
            elif target_delta > MIN_MOVE_SIZE:
                eTaxi.move(target_delta)
            else:
                eTaxi.move(MIN_MOVE_SIZE)
        else:
            eTaxi.move(CM_PER_MOVE)

        if count % STEPS_PER_DATAPOINT == 0:
            recorded_x_pos.append(loc_x)
            recorded_y_pos.append(loc_y)
            measured_x_pos.append(loc_x)
            measured_y_pos.append(loc_y)
        count += 1

    target_distance = dist_from_target(loc_x, loc_y)
    print('eTaxi to target distance: ', target_distance)

    # eTaxi.turn_to_heading(PLANE_HEADING + math.pi)
    if isinstance(eTaxi, eTaxi_Simulated):
        success, dist = is_bot_in_target_zone(eTaxi)
        if not success:
            count = step_limit
            print('True Distance From target: ', dist)

    if not bulk_test:
        make_plot(recorded_x_pos, recorded_y_pos, angle_adjust_x_pos, angle_adjust_y_pos, measured_x_pos, measured_y_pos, target_x_pos, target_y_pos, start_x_pos, start_y_pos)
        print('\nDone')
        print('num_steps: ', count)
    return count, recorded_x_pos, recorded_y_pos, angle_adjust_x_pos, angle_adjust_y_pos, measured_x_pos, measured_y_pos, start_x_pos, start_y_pos


def adjust_heading(eTaxi, loc_x, loc_y):
    line_rad = get_line_angle()
    above_line = point_above_line(loc_x, loc_y)
    if above_line is None:
        print('Bot is turning to on to LINE: ', math.degrees(line_rad))
        eTaxi.turn_to_heading(line_rad)
    elif above_line:
        eTaxi.turn_to_heading(line_rad - (eTaxi.MAX_IMU_ERROR*ANGLE_ADJUST_CONSTANT))
        print('Bot is turning to heading: ', math.degrees(line_rad - (eTaxi.MAX_IMU_ERROR*ANGLE_ADJUST_CONSTANT)))
    else:
        eTaxi.turn_to_heading(line_rad + (eTaxi.MAX_IMU_ERROR*ANGLE_ADJUST_CONSTANT))
        print('Bot is turning to heading: ', math.degrees(line_rad + (eTaxi.MAX_IMU_ERROR * ANGLE_ADJUST_CONSTANT)))


def get_line_angle():
    y_diff = target_y_pos - start_y_pos
    x_diff = target_x_pos - start_x_pos
    if x_diff != 0 and y_diff != 0:
        line_rad = math.atan(y_diff/x_diff)
        if x_diff < 0:
            return line_rad + math.pi
        elif y_diff < 0 and x_diff > 0:
            return (2*math.pi) + line_rad
        else:
            return line_rad
    elif x_diff == 0:
        if y_diff > 0:
            return math.pi/2
        else:
            return 3*math.pi/2
    elif y_diff == 0:
        if x_diff > 0:
            return 0
        else:
            return math.pi


def point_above_line(loc_x, loc_y):
    v1 = (target_x_pos - start_x_pos, target_y_pos - start_y_pos)  # Vector 1
    v2 = (target_x_pos - loc_x, target_y_pos - loc_y)  # Vector 1
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    if xp == 0:
        return None
    elif xp > 0:
        return False
    else:
        return True


def dist_from_target(loc_x, loc_y):
    dist = math.sqrt((target_x_pos - loc_x)**2 + (target_y_pos-loc_y)**2)
    return dist


def dist_from_line(eTaxi):
    loc_x, loc_y = eTaxi.get_position()
    num = abs( ((target_y_pos - start_y_pos)*loc_x) - ((target_x_pos - start_x_pos)*loc_y) + (target_x_pos*start_y_pos) - (target_y_pos*start_x_pos) )
    denom = math.sqrt((target_y_pos-start_y_pos)**2 + (target_x_pos-start_x_pos)**2)
    distance = num/denom
    return num/denom, loc_x, loc_y


def in_tolerance_of_target(loc_x, loc_y):
    x_diff = loc_x - target_x_pos
    y_diff = loc_y - target_y_pos
    dist = math.sqrt((x_diff**2) + (y_diff**2))
    return dist <= TARGET_TOLERANCE


def set_start_position(eTaxi):
    global start_x_pos, start_y_pos
    sum_x = 0
    sum_y = 0
    num_queries = 10
    for _ in range(num_queries):
        x, y = eTaxi.get_position()
        sum_x += x
        sum_y += y
    start_x_pos = sum_x/num_queries
    start_y_pos = sum_y/num_queries

def is_bot_in_target_zone(eTaxi):
    true_x, true_y = eTaxi.get_true_position()
    x_diff = true_x - target_x_pos
    y_diff = true_y - target_y_pos
    dist = math.sqrt((x_diff ** 2) + (y_diff ** 2))
    return dist <= TARGET_TOLERANCE, dist


def set_plane(plane_x, plane_y, plane_heading):
    global target_x_pos, target_y_pos, PLANE_HEADING
    PLANE_HEADING = plane_heading
    target_x_pos = plane_x + (TARGET_DIST_FROM_PLANE*math.cos(plane_heading))
    target_y_pos = plane_y + (TARGET_DIST_FROM_PLANE*math.sin(plane_heading))


def get_target():
    return target_x_pos, target_y_pos


def distance_from_target(loc_x, loc_y):
    x_diff = loc_x - target_x_pos
    y_diff = loc_y - target_y_pos
    dist = math.sqrt((x_diff ** 2) + (y_diff ** 2))
    return dist