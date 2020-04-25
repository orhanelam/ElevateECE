import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


def make_plot(x_pos, y_pos, adj_x, adj_y, measured_x, measured_y, target_x, target_y, start_x, start_y, plane_x=None, plane_y=None):
    plt.clf()

    plt.plot(x_pos, y_pos, 'b-')
    plt.plot(adj_x, adj_y, 'go')

    plt.plot(measured_x, measured_y, 'c--')

    plt.plot([target_x], [target_y], 'ro')
    plt.plot([start_x], [start_y], 'mo')
    if plane_x is not None and plane_y is not None:
        plt.plot([plane_x], [plane_y], 'ko')

    plt.show()
