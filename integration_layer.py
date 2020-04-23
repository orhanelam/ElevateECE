import math
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib import style

#eTaxi Variables
x_pos = 0.0
y_pos = 0.0
start_x_pos = 0.0
start_y_pos = 0.0
adj_target_x_pos = 0.0
adj_target_y_pos = 0.0
heading = 0.0

#Target
target_x_pos = 2500.2
target_y_pos = 10.2

#Config vars
TARGET_TOLERANCE = 20
MAX_POS_ERROR = 20
MAX_IMU_ERROR_DEG = 0.5
MAX_IMU_ERROR = (MAX_IMU_ERROR_DEG/360) * 2*math.pi
ANGLE_ADJUST_CONSTANT = 2
MAX_NUM_STEPS = 6000
METERS_PER_MOVE = 0.1
MAX_NUM_TRIALS = 1000000
STEPS_PER_DATAPOINT = 20


def main(bulk_test=False, num_trials=MAX_NUM_TRIALS):
    global x_pos, y_pos, target_x_pos, target_y_pos
    x_pos = 10.2
    y_pos = 10.2
    target_x_pos = 2000.2
    target_y_pos = 3500.2
    drive_to_target(MAX_NUM_STEPS)

    x_pos = 3500.2
    y_pos = 2000.2
    target_x_pos = 10.2
    target_y_pos = 11.3
    drive_to_target(MAX_NUM_STEPS)

    x_pos = 10.2
    y_pos = 2000.2
    target_x_pos = 2500.2
    target_y_pos = 10.2
    drive_to_target(MAX_NUM_STEPS)

    x_pos = 2000.2
    y_pos = 10.2
    target_x_pos = 10.2
    target_y_pos = 3500.2
    drive_to_target(MAX_NUM_STEPS)

    if bulk_test:
        num_failures = 0
        for x in range(1000):
            x_pos = random.randint(0, 100000)
            y_pos = random.randint(0, 100000)
            target_x_pos = random.randint(0, 100000)
            target_y_pos = random.randint(0, 100000)
            step_count, rec_x, rec_y, adj_x, adj_y = drive_to_target(MAX_NUM_STEPS, bulk_test=True)
            if step_count >= MAX_NUM_STEPS:
                num_failures += 1
                # print('end_coords: ', x_pos, y_pos)
                # print('target_coords', target_x_pos, target_y_pos)
                # print()
                # make_plot(rec_x, rec_y, adj_x, adj_y)
        print('Results:')
        print('Trials Run: ', num_trials)
        print("Trials Failed:  ", num_failures)
        print('Failure Rate: ', num_failures/num_trials)


def make_plot(x_pos, y_pos, adj_x, adj_y):
    plt.clf()
    plt.plot([target_x_pos], [target_y_pos], 'ro')
    plt.plot([start_x_pos], [start_y_pos], 'mo')

    plt.plot(x_pos, y_pos, 'bo')
    plt.plot(adj_x, adj_y, 'go')

    plt.show()


# grid is quad I, 0 degree is parrallel to x axis
def drive_to_target(step_limit=float('inf'), bulk_test=False):
    global start_x_pos, start_y_pos

    recorded_x_pos = []
    recorded_y_pos = []
    angle_adjust_x_pos = []
    angle_adjust_y_pos = []

    start_x_pos, start_y_pos = get_position()
    adjust_heading(start_x_pos, start_y_pos)
    count = 0

    while not in_tolerance_of_target() and count < step_limit:
        drift_dist, loc_x, loc_y = dist_from_line()
        if drift_dist > MAX_POS_ERROR:
            adjust_heading(loc_x, loc_y)
            angle_adjust_x_pos.append(x_pos)
            angle_adjust_y_pos.append(y_pos)
        move(METERS_PER_MOVE*100)

        if count % STEPS_PER_DATAPOINT == 0:
            recorded_x_pos.append(x_pos)
            recorded_y_pos.append(y_pos)
        count += 1

    if not bulk_test:
        make_plot(recorded_x_pos, recorded_y_pos, angle_adjust_x_pos, angle_adjust_y_pos)
        print('\nDone')
        print('eTaxi Position: ', x_pos, y_pos)
        print('num_steps: ', count)
    return count, recorded_x_pos, recorded_y_pos, angle_adjust_x_pos, angle_adjust_y_pos


def adjust_heading(loc_x, loc_y):
    line_rad = math.atan((target_y_pos-start_y_pos)/(target_x_pos-start_x_pos))
    if loc_x > target_x_pos:
        line_rad += math.pi

    if point_above_line(loc_x, loc_y):
        turn_to_heading(line_rad - (MAX_IMU_ERROR*ANGLE_ADJUST_CONSTANT))
    else:
        turn_to_heading(line_rad + (MAX_IMU_ERROR*ANGLE_ADJUST_CONSTANT))


def point_above_line(loc_x, loc_y):
    v1 = (target_x_pos - start_x_pos, target_y_pos - start_y_pos)  # Vector 1
    v2 = (target_x_pos - loc_x, target_y_pos - loc_y)  # Vector 1
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    if xp > 0:
        return False
    else:
        return True


def dist_from_line():
    loc_x, loc_y = get_position()
    num = abs( ((target_y_pos - start_y_pos)*loc_x) - ((target_x_pos - start_x_pos)*loc_y) + (target_x_pos*start_y_pos) - (target_y_pos*start_x_pos) )
    denom = math.sqrt((target_y_pos-start_y_pos)**2 + (target_x_pos-start_x_pos)**2)
    distance = num/denom
    return num/denom, loc_x, loc_y


def in_tolerance_of_target():
    x_diff = x_pos - target_x_pos
    y_diff = y_pos - target_y_pos
    dist = math.sqrt((x_diff**2) + (y_diff**2))
    return dist <= TARGET_TOLERANCE


def get_position():
    rad_error = (random.randint(0, 100)/100) * math.pi
    dist_error = random.randint(0, MAX_POS_ERROR)
    x_error = dist_error * math.cos(rad_error)
    y_error = dist_error * math.sin(rad_error)
    #print('x_pos_error: ', x_error, ' y_pos_error: ', y_error)
    return (x_pos + x_error), (y_pos + y_error)


def move(dist):
    global x_pos, y_pos
    x_diff = dist * math.cos(heading)
    y_diff = dist * math.sin(heading)
    x_pos += x_diff
    y_pos += y_diff
    #print("x_pos: ", x_pos, " y_pos: ", y_pos)


def turn_to_heading(rads):
    global heading
    error = ((random.randint(0, 200) - 100)/100) * MAX_IMU_ERROR
    heading = rads + error
    #print('IMU skew is: ', error)
    #print('Heading: ', heading)




