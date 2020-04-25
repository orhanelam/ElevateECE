import threading
import random

thread_var = 0


def main():
    global thread_var
    thread_var = 0

    t1 = threading.Thread(target=increment)
    t2 = threading.Thread(target=randomize)

    t1.start()
    t2.start()

    while True:
        print(thread_var)


def increment():
    global thread_var

    while True:
        thread_var *= -1


def randomize():
    global thread_var
    count = 0
    while True:
        count += 1
        if count % 200 == 0:
            thread_var += 10

