import threading

from DWMTag import DWMTag
from eTaxi_Dima import eTaxi_Dima


def main():
    bot = eTaxi_Dima()
    while True:
        position = bot.get_position()
        print('position: ', position)


main()