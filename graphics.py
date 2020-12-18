try:
    from matplotlib import pyplot as plt
except Exception as mnfe:
    print(mnfe)
    exit()


DEBUG = False


if DEBUG:
    from numpy import arange
    from math import sin


class Graphics:
    def __init__(self):
        self.style = [ 'r', 'g', 'b', 'r--', 'g--', 'b--', 'r:', 'g:', 'b:']


    def draw(self, xs: list, ys: list, names: 'list of str', title: str):
        if len(xs) == 0 or len(ys) == 0:
            raise RuntimeError('Lists of points can not be empty.')
        if not isinstance(xs[0], list):
            if len(xs) != len(ys):
                raise RuntimeError('Different number of x and y points.')
            plt.plot(xs, ys)
        else:
            for x_pnt, y_pnt, style, name in zip(xs, ys, self.style, names):  # If the grahics number is more than styles in 'self',
                                                                 # all overflowing graphics are not drawn
                if len(x_pnt) != len(y_pnt):
                    raise RuntimeError('Different number of x and y points')
                else:
                    plt.plot(x_pnt, y_pnt, style, label=name)
        plt.title(title)
        plt.grid(True)
        plt.xlabel('x axis')
        plt.ylabel('y axis')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    if not DEBUG:
        print('WARNING! This file is not intended to be main file. Consider running "main.py".')
        print('If you want to just test if it all works - change the "DEBUG" variable to True.')
        exit()
    else:
        print('Graphics test.')
    grph = Graphics()
    xpoints, ypoints, rpoints = list(), list(), list()

    for x in arange(0, 1, 0.001):
        xpoints.append(x)
        ypoints.append(sin(x) / sin(1) - x)
        rpoints.append((55/202) * x * (1 - x))

    grph.draw([xpoints, xpoints], [ypoints, rpoints], 'TEST')
