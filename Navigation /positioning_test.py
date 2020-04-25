import threading

from DWMTag import DWMTag

myTag = DWMTag()


def main():
    initialize_positioning_system()
    position = myTag.get_pos()
    print('position: ', position[0], position[1])


def initialize_positioning_system():
    positioning_thread = threading.Thread(target=update_positioning)
    positioning_thread.start()


def update_positioning():
    while True:
        myTag.update_position()
