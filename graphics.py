try:
    from matplotlib import pyplot as plt
except ModuleNotFoundError as mnfe:
    print(mnfe)
    exit()


class Graphics:
    def __init__(self):
        self.style = [ 'r', 'g', 'b', 'r--', 'g--', 'b--', 'r:', 'g:', 'b:']


    def draw(self, xs: list, ys: list, title: str):
        if len(xs) == 0 or len(ys) == 0:
            raise RuntimeError('Lists of points can not be empty.')
        if not isinstance(xs[0], list):
            if len(xs) != len(ys):
                raise RuntimeError('Different number of x and y points.')
            plt.plot(xs, ys)
        else:
            for x_pnt, y_pnt, style in zip(xs, ys, self.style):  # If the grahics number is more than styles in 'self',
                                                                 # all overflowing graphics are not drawn
                if len(x_pnt) != len(y_pnt):
                    raise RuntimeError('Different number of x and y points')
                else:
                    plt.plot(x_pnt, y_pnt, style)
        plt.title(title)
        plt.grid(True)
        plt.xlabel('x axis')
        plt.ylabel('y axis')
        plt.show()
