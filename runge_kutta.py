try:
    from numpy import arange
    from math import sin, cos, log, e
    from typing import Tuple
except ModuleNotFoundError as mnfe:
    print(mnfe)
    exit()


DEBUG = False


class RungeKutta:
    '''Runge Kuttas method to solve differential equations of the second power.'''
    
    def __init__(self, func: str, x_init_val: float, func_init_val: float, diff_init_val: float):
        '''## RungeKuttas initialization.\n
            `x_init_val` - x cooridnate values of which we know\n
            `func_init_val` - known to us y value\n
            `diff_init_val` - known to us y' value'''

        self.zdiff = lambda x, y, z: eval(  # Not the safest way but the easyest one. For univercity lab is just perfect!
            func.replace('x', f'({x})')
                .replace("y'", f'({z})')
                .replace('y', f'({y})')
        )
        self.ydiff = lambda z: z
        self.x = x_init_val
        self.y = func_init_val
        self.z = diff_init_val


    def get_values(self, begin: float, end: float, step: float) -> Tuple[float, float, float]:
        '''Calculates the approximate values of a function using Runge Kuttas method.\n
            Returns an approximate value of a function.\n
            `begin` - x point we start with\n
            `end` - x point we finish with\n
            `step` - value, the x is increased on each iteration'''
            
        for i in arange(begin, end + step, step):  # Main Runge Kuttas method logic.
            yield self.x, self.y, self.z  # x - x points cordinate, y - function value in current x, z - derivate of y.
            hlfstp = step / 2
            q0 = self.zdiff(self.x, self.y, self.z)
            k0 = self.ydiff(self.z)
            q1 = self.zdiff(self.x + hlfstp, self.y + k0 * hlfstp, self.z + q0 * hlfstp)
            k1 = self.ydiff(self.z + q0 * hlfstp)
            q2 = self.zdiff(self.x + hlfstp, self.y + k1 * hlfstp, self.z + q1 * hlfstp)
            k2 = self.ydiff(self.z + q1 * hlfstp)
            q3 = self.zdiff(self.x + step, self.y + k2 * step, self.z + q2 * step)
            k3 = self.ydiff(self.z + q2 * step)
            self.z = self.z + (step / 6) * (q0 + 2*q1 + 2*q2 + q3)
            self.y = self.y + (step / 6) * (k0 + 2*k1 + 2*k2 + k3)
            self.x += step


# Simple test.
if __name__ == '__main__':
    if not DEBUG:
        print('WARNING! This file is not intended to be main file. Consider running "main.py".')
        print('If you want to just test if it all works - change the "DEBUG" variable to True.')
        exit()
    else:
        print('Runge Kuttas method tests:')
    func = "0.8 + x*y' - 2*x*y"
    x_init_val = 1.5
    func_init_val = -0.2
    diff_init_val = 2
    runge_kutta = RungeKutta(func, x_init_val, func_init_val, diff_init_val)
    for (i, val, diff) in runge_kutta.get_values(1.5, 2.5, 0.1):
        print('X: {}, D: {}, Y: {}'.format(round(i, 3), round(diff, 3), round(val, 3)))
