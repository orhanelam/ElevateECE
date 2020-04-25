import threading

thread_var = 0


def main():
    t1 = threading.Thread(target=increment)

    t1.start()

    while True:
        print(thread_var)


def increment():
    global thread_var

    while True:
        thread_var += 1

