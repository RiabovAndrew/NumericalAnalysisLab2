from numpy import arange
from runge_kut import RungeKutta
from graphics import Graphics


class ReductionMethod:
    '''Solution of the boundary value problem by dividing it into 2 Cauchy problems.'''


    def __init__(self, a: float, b: float, a0: float, a1: float, A: float, b0: float, b1: float, B: float, p: str, q: str, f: str):
        '''The function arguments represent the following polynomial terms:\n
        Ly(x) = y"(x) + p(x)y'(x) + q(x)y(x) = f(x)\n
        with the following boundary conditions:\n
        a0*y(a) + a1*y'(a) = A,\n
        b0*y(b) + b1*y'(b) = B'''

        if abs(a0) + abs(a1) == 0 or abs(b0) + abs(b1) == 0:
            raise RuntimeError('The boundary condition does not exist.')
        else:
            self.a = a
            self.b = b
            self.C = lambda v, dv, u, du: (B - (b0 * v + b1 * dv)) / (b0 * u + b1 * du)

            self.Lu = f"0 - ({p})*y' - ({q})*y"
            self.Lv = f"({f}) - ({p})*y' - ({q})*y"

            self.u_func_val = (-(a1 / a0)) if a0 != 0 else 1
            self.u_diff_val = 1 if a0 != 0 else (-(a0 / a1))
            self.v_func_val = (A / a0) if a0 != 0 else 0
            self.v_diff_val = 0 if a0 != 0 else (A / a1)

            self.u_rk = RungeKutta(self.Lu, a, self.u_func_val, self.u_diff_val)
            self.v_rk = RungeKutta(self.Lv, a, self.v_func_val, self.v_diff_val)


    def get_values(self, step: float) -> float:
        C = None
        for u_zip, v_zip in zip(self.u_rk.get_values(self.a, self.b, step),
                                self.v_rk.get_values(self.a, self.b, step)):
            x, u, du = u_zip
            x, v, dv = v_zip
            C = self.C(v, dv, u, du)# if C is None else C
            yield x, C * u + v


if __name__ == '__main__':  #Some tests.
    RM = ReductionMethod(1, 2, 1, 0, 1, 3, 1, 0.5, 'x**6', '-(x**5)', '6 - 3*(x**2)')
    #RM = ReductionMethod(0.5, 1.5, 1, 0, 0.303728369615394, 1, -1, 0.447281594100796, '2', '-1/x', '(-1) * x*(2.71**(-x)) + 2.71**(-x)')
    #RM = ReductionMethod(0.5, 1, 0, 1, 1.5, 1, 1, 4, '2', '-4/x', '1')
    xs = list()
    ys = list()
    rys = list()
    grph = Graphics()
    for x, y in RM.get_values(0.0001):
        xs.append(x)
        ys.append(y)
        rys.append(x**(-2))
        # print('x: {}, y: {}, true y: {}'.format(round(x, 3),
        #                                         round(y, 3),
        #                                         #round(x**(-2), 3))
        #                                         #round(x*(2.7**(-x)), 3))
        #                                         round(x**2 + 0.5*x,3))
        # )
    grph.draw([xs, xs], [ys, rys], 'Title')
    
    print('Finish!')
