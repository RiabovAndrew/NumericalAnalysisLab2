#import matplotlib.pylab as plt
from matplotlib import pyplot as plt

class Graphics:
    def __init__(self):
        pass


    def draw(self, xs: list, ys: list, title: str):
        if len(xs) == 0 or len(ys) == 0:
            raise RuntimeError('Lists of points can not be empty.')
        if not isinstance(xs[0], list):
            if len(xs) != len(ys):
                raise RuntimeError('Different number of x and y points.')
            plt.plot(xs, ys)
        else:
            for x_pnt, y_pnt in zip(xs, ys):
                if len(x_pnt) != len(y_pnt):
                    raise RuntimeError('Different number of x and y points')
                else:
                    plt.plot(x_pnt, y_pnt, 'b--')
        plt.title(title)
        plt.grid(True)
        plt.xlabel('x axis')
        plt.ylabel('y axis')
        plt.show()
