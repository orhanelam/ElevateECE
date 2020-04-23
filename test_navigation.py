import math
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib import style
from integration_layer import navigate_bot, get_line_angle, drive_to_target, MAX_NUM_STEPS

# Simulation Vars
MAX_NUM_TRIALS = 5


def main(bulk_test=False, num_trials=MAX_NUM_TRIALS):
    global x_pos, y_pos, target_x_pos, target_y_pos, start_y_pos, start_x_pos
    # x_pos = 10.2
    # y_pos = 10.2
    # target_x_pos = 2000.2
    # step_count, rec_x, rec_y, adj_x, adj_y, measured_x, measured_y, defined_start_x, defined_start_y = drive_to_target(MAX_NUM_STEPS)
    # make_plot(rec_x, rec_y, adj_x, adj_y, measured_x, measured_y)

    # start_x_pos = 5500.2
    # start_y_pos = 4000.2
    # target_x_pos = 100.2
    # step_count, rec_x, rec_y, adj_x, adj_y, measured_x, measured_y, defined_start_x, defined_start_y = drive_to_target(MAX_NUM_STEPS)
    # make_plot(rec_x, rec_y, adj_x, adj_y, measured_x, measured_y)

    # x_pos = 10.2
    # y_pos = 2000.2
    # target_x_pos = 2500.2
    # target_y_pos = 10.2
    # step_count, rec_x, rec_y, adj_x, adj_y, measured_x, measured_y, defined_start_x, defined_start_y = drive_to_target(MAX_NUM_STEPS)
    # make_plot(rec_x, rec_y, adj_x, adj_y, measured_x, measured_y)
    #
    # x_pos = 2000.2
    # y_pos = 10.2
    # target_x_pos = 10.2
    # target_y_pos = 3500.2
    # step_count, rec_x, rec_y, adj_x, adj_y, measured_x, measured_y, defined_start_x, defined_start_y = drive_to_target(MAX_NUM_STEPS)
    # make_plot(rec_x, rec_y, adj_x, adj_y, measured_x, measured_y)

    if bulk_test:
        num_failures = 0
        for x in range(num_trials):
            print("Trial: ", x)
            x_pos = random.randint(0, 1000)
            y_pos = random.randint(0, 1000)
            inital_x = x_pos
            inital_y = y_pos
            target_x_pos = random.randint(0, 1000)
            target_y_pos = random.randint(0, 1000)
            step_count, rec_x, rec_y, adj_x, adj_y, measured_x, measured_y, defined_start_x, defined_start_y, target_x, target_y = drive_to_target(MAX_NUM_STEPS, bulk_test=True)
            if step_count >= MAX_NUM_STEPS:
                num_failures += 1
                print('start_coords: ', inital_x, inital_y)
                print('bot start coords: ', defined_start_x, defined_start_y)
                print('target_coords', target_x_pos, target_y_pos)
                print('end_coords: ', x_pos, y_pos)
                line_angle = math.degrees(get_line_angle())
                print('line_angle: ', line_angle)
                print()
            make_plot(rec_x, rec_y, adj_x, adj_y, measured_x, measured_y, target_x, target_y, defined_start_x, defined_start_y)

        print('Results:')
        print('Trials Run: ', num_trials)
        print("Trials Failed:  ", num_failures)
        print('Failure Rate: ', num_failures/num_trials)


def test_navigate_bot():

    way_points = []
    for x in range(500):
        point_x = random.randint(0, 10000)
        point_y = random.randint(0, 10000)
        way_points.append([point_x, point_y])

    full_rec_x, full_rec_y, full_adj_x, full_adj_y, target_point_x, target_point_y = navigate_bot(way_points)
    make_plot(full_rec_x, full_rec_y, full_adj_x, full_adj_y, target_point_x, target_point_y)


def make_plot(x_pos, y_pos, adj_x, adj_y, measured_x, measured_y, target_x_pos=None, target_y_pos=None, start_x_pos=None, start_y_pos=None):
    plt.clf()

    plt.plot(x_pos, y_pos, 'b-')
    plt.plot(adj_x, adj_y, 'go')

    plt.plot(measured_x, measured_y, 'c--')

    if target_x_pos is not None and target_y_pos is not None:
        plt.plot([target_x_pos], [target_y_pos], 'ro')
    if start_x_pos is not None and start_y_pos is not None:
        plt.plot([start_x_pos], [start_y_pos], 'mo')

    plt.show()
