import math
import threading
import time
from motorController import motorController
from pi_script import tag_present, trust_reading, get_x, test, TEST, \
    test_threading, get_THREAD_TEST, get_tag_present, get_tag_x_offset, get_trust_reading

X_OFFSET_MAX = 80
CM_PER_MOVE = 20
motors = motorController()


TURN_SPEED = 100
MOVE_SPEED = 100


fov_degrees = 10
fov_rad = math.radians(fov_degrees)


def dock_v1():
    print('Dock_v1')
    initalize_openMV()
    time.sleep(0.5)
    while not get_tag_present():
        print('test: ', TEST)
        print('looking for tag')
        print('THREAD_TEST: ', THREAD_TEST)
        print('THREAD_TEST through getter: ', get_THREAD_TEST())
    if get_tag_present():
        print("Tag is present")
        offset = get_tag_x_offset()
        degrees_off_from_tag_heading = (offset/X_OFFSET_MAX)*fov_degrees
        if offset < 0:
            motors.turnLeft(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turnRight(degrees_off_from_tag_heading, TURN_SPEED)
        print('Bot just turned hopefully')
        while not get_trust_reading():
            motors.move(CM_PER_MOVE, MOVE_SPEED)
        print('bot just moved')
        if offset < 0:
            motors.turnRight(degrees_off_from_tag_heading, TURN_SPEED)
        else:
            motors.turnLeft(degrees_off_from_tag_heading, TURN_SPEED)
        print('done')


def initalize_openMV():
    MV_update_thread = threading.Thread(target=update_openMV)
    MV_update_thread.start()


def update_openMV():
    while True:
        tag_present()
        trust_reading()
        get_x()
        test()
        test_threading()


dock_v1()

