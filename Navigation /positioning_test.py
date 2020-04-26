import threading

from DWMTag import DWMTag
from eTaxi import eTaxi


def main():
    bot = eTaxi()
    while True:
        position = bot.get_position()
        print('position: ', position)


main()