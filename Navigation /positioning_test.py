import threading

from DWMTag import DWMTag

myTag = DWMTag()


def main():
    initialize_positioning_system()
    while True:
        position = myTag.get_pos()
        print('position: ', position)


def initialize_positioning_system():
    positioning_thread = threading.Thread(target=update_positioning)
    positioning_thread.start()


def update_positioning():
    while True:
        print('thread_hit')
        myTag.update_position()


main()