try:
    from runge_kutta import RungeKutta
    from graphics import Graphics
    from math import sin, cos, log  # 'log', 'tan' and all other math functions shall be imported here if needed.
    from copy import copy
except ModuleNotFoundError as mnfe:
    print(mnfe)
    exit()


DEBUG = True


class ReductionMethod:
    '''Solution of the boundary value problem by dividing it into 2 Cauchy problems.'''

    
    def __init__(self, a: float, b: float, a0: float, a1: float, A: float, b0: float, b1: float, B: float, p: str, q: str, f: str, g: str = '1'):
        '''The function arguments represent the following polynomial terms:\n
        Ly(x) = g(x)y"(x) + p(x)y'(x) + q(x)y(x) = f(x)\n
        with the following boundary conditions:\n
        a0*y(a) + a1*y'(a) = A,\n
        b0*y(b) + b1*y'(b) = B'''

        if abs(a0) + abs(a1) == 0 or abs(b0) + abs(b1) == 0:
            raise RuntimeError('The boundary condition does not exist.')

        else:
            self.a = a
            self.b = b
            self.C = lambda v, dv, u, du: (B - b0 * v - b1 * dv) / (b0 * u + b1 * du)

            self.Lu = f"0 - ({p})*y' / ({g}) - ({q})*y / ({g})"
            self.Lv = f"({f}) / ({g}) - ({p})*y' / ({g}) - ({q})*y / ({g})"

            self.u_func_val = -(a1 / a0) if a0 != 0 else 1
            self.u_diff_val = 1 if a0 != 0 else -(a0 / a1)
            self.v_func_val = A / a0 if a0 != 0 else 0
            self.v_diff_val = 0 if a0 != 0 else A / a1

            self.u_rk = RungeKutta(self.Lu, a, self.u_func_val, self.u_diff_val)  # First Cauchy problem 
            self.v_rk = RungeKutta(self.Lv, a, self.v_func_val, self.v_diff_val)  # Second Cauchy problem


    def get_values(self, step: float) -> float:
        '''Calculates the approximate values of the needed funciton and yields them.'''

        un, vn, dun, dvn = None, None, None, None
        crutch_u = copy(self.u_rk)
        crutch_v = copy(self.v_rk)

        for u_zip, v_zip in zip(crutch_u.get_values(self.a, self.b, step),   # Just a crutch for getting the values of v(b) and u(b).
                                crutch_v.get_values(self.a, self.b, step)):  # Year, I've made the separate loop for getting these values.
            un, dun = u_zip[1], u_zip[2]                                     # Year, I've gone through this loop twice.
            vn, dvn = v_zip[1], v_zip[2]                                     # I just don't know how to get it without this loop, so this will be depricated in future.

        C = self.C(vn, dvn, un, dun)
        for u_zip, v_zip in zip(self.u_rk.get_values(self.a, self.b, step),
                                self.v_rk.get_values(self.a, self.b, step)):
            x, u, _ = u_zip  # We don't need the derivate here, so it's ommited.
            x, v, _ = v_zip
            yield x, C * u + v


if __name__ == '__main__':  # Some tests.
    if not DEBUG:
        print('WARNING! This file is not intended to be main file. Consider running "main.py".')
        print('If you want to just test if it all works - change the "DEBUG" variable to True.')
        exit()
    else:
        print('Reduction method test.')

    # IMPORTANT! Red - approximate function, green - original funciton
    conditions = {
        0: (ReductionMethod(1, 2, 1, 0, 1, 3, 1, 0.5, 'x**2', '-x', '(6 - (3*(x**3))) / (x**4)'), lambda x: x**(-2)),               # Test example, Ok
        1: (ReductionMethod(0.5, 1, 0, 1, 1.5, 1, 1, 4, '2', '-4/x', '1'), lambda x: x**2 + 0.5*x),                                 # v11, Ok
        2: (ReductionMethod(0, 1, 1, 0, 1, 1, 2, 0, '-1', '-2', '-3*2.7182**(-x)'), lambda x: (x+1)*2.7181**(-x)),                  # v13, Ok
        3: (ReductionMethod(0, 0.5, 0, 1, 0, 1, 0, 0.5 * sin(0.5), '2*x', '-1', '2 * cos(x) * (x**2 + 1)'), lambda x: x*sin(x)),    # v10, Ok
        4: (ReductionMethod(0, 1, 1, 1, 1, 0, 1, 4, '2', '-3', '-6*x**2+8*x+1'), lambda x: 2*x**2 + 1),                             # v1, Ok
        5: (ReductionMethod(0, 1, 1, 0, -0.25, 1, -3, 0, '2 / (x-4)', '(x-4)', '1'), lambda x: 1 / (x-4))                           # v2, Ok
    }
    destiny = 5  # Change this to switch equations
    step = 0.001  # Change this to change step

    xs, ys, rys = list(), list(), list()
    grph = Graphics()

    for x, y in conditions[destiny][0].get_values(step):
        xs.append(x)
        ys.append(y)
        rys.append(conditions[destiny][1](x))
    grph.draw([xs, xs], [ys, rys], 'Title')
    
    print('Finish!')
