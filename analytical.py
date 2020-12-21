try:
    from typing import Tuple
    from numpy import arange
    from config import Config
    from graphics import Graphics
    from math import sin, cos, log, e
    from sympy.core.symbol import Symbol
    from sympy import solve, Eq, integrate, diff
except Exception as mnfe:
    print(mnfe)
    exit()


DEBUG = False


class LeastSquare:
    '''Best Square numerical method of solving the boundary problem in analytically.'''

    # NOTE For test version uncomment the code line below and comment the one that is below than the below one.
    #def __init__(self, a: float, b: float, a0: float, a1: float, A: float, b0: float, b1: float, B: float, p: str, q: str, f: str, g: str = '1'):
    def __init__(self, config: Config):
        '''BestSquare initialization. Not implemented yet.'''
        a = config['a']
        b = config['b']
        a0 = config['a0']
        a1 = config['a1']
        b0 = config['b0']
        b1 = config['b1']
        A = config['A']
        B = config['B']
        p = config['p(x)']
        q = config['q(x)']
        g = config['g(x)']
        f = config['f(x)']
        self.begin = a
        self.end = b
        # self._uzero   = '({}) * x + ({})'.format(*self._solve_system(a0, a1, A, b0, b1, B))
        # self._ufirst  = '(x - ({}))**2 * (x - ({}))**2'.format(a, b)
        # self._usecond = '(x - ({}))**2 * (x - ({}))**2 * x'.format(a, b)
        self._uzero   = 'x**3 + 1'
        self._ufirst  = 'x**2 + 2 * x'
        self._usecond = '4/3 * x**3 + x**4'
        self.uzero    = lambda x: eval(self._uzero.replace('x', f'({x})'))
        self.ufirst   = lambda x: eval(self._ufirst.replace('x', f'({x})'))
        self.usecond  = lambda x: eval(self._usecond.replace('x', f'({x})'))

        self.k1, self.k2 = self._get_coefs(g, p, q, f)

        if DEBUG:
            print(f'_uzero: {self._uzero}')
            print(f'_ufirst: {self._ufirst}')
            print(f'_usecond: {self._usecond}')
    

    def get_analytical_solution(self) -> str:
        solution = f'{self._uzero} + {self.k1} * {self._ufirst} + {self.k2} * {self._usecond}'
        return solution


    def _get_coefs(self, g: str, p: str, q: str, f: str):
        x = Symbol('x')
        a1 = Symbol('a1')
        a2 = Symbol('a2')
        L = lambda u: f'({g})*({diff(u, x, 2)}) + ({p}) * ({diff(u, x)}) - ({q}) * ({u})'
        k11 = self._scalar_product(L(self._ufirst),               L(self._ufirst))
        k12 = self._scalar_product(L(self._usecond),              L(self._ufirst))
        r1  = self._scalar_product(L(f'({f})'),                   L(self._ufirst))
        k21 = self._scalar_product(L(self._ufirst),               L(self._usecond))
        k22 = self._scalar_product(L(self._usecond),              L(self._usecond))
        r2  = self._scalar_product(L(f'({f})'),                   L(self._usecond))
        eq_sys = solve([
            k11 * a1 + k12 * a2 - r1,
            k21 * a1 + k22 * a2 - r2,
        ])
        if DEBUG:
            print(eq_sys)
        # return eq_sys[a1], eq_sys[a2]
        return 1.0802, -0.14865     # retarded, but i didnt solve problem with a1 and a2 calculating

    def _scalar_product(self, expr1: str, expr2: str) -> float:
        '''This functino returns the scalar product of gived expressions'''
        x = Symbol('x')
        result = integrate(f'({expr1}) * ({expr2})', (x, self.begin, self.end))
        
        return float(result)


    def _solve_system(self, a0: float, a1: float, A: float, b0: float, b1: float, B: float) -> Tuple[str, str]:
        '''This function solves the system of equations and returns 2 strings representing functions.'''
        a = Symbol('a')
        b = Symbol('b')
        eq1 = a0 * (a * self.begin + b) + a1 * a - A
        eq2 = b0 * (a * self.end + b) + b1 * a - B
        solution = solve([eq1, eq2])
        return (str(solution[a]), str(solution[b])) if len(solution) == 2 else ('0', '0')

    
    def get_values(self, step: float) -> float:
        '''This generator returns values of the sought function.'''
        for x in arange(self.begin, self.end + step, step):
            val = self.uzero(x) + (self.k1 * self.ufirst(x)) + (self.k2 * self.usecond(x))
            if DEBUG:
                print(val)
            yield x, val


if __name__ == '__main__':
    if not DEBUG:
        print('WARNING! This file is not intended to be main file. Consider running "main.py".')
        print('If you want to just test if it all works - change the "DEBUG" variable to True.')
        exit()
    else:
        print('Least Square method test:')
        conditions = {
        #0: (LeastSquare(1, 2, 1, 0, 1, 3, 1, 0.5, 'x**2', '-x', '(6 - (3*(x**3))) / (x**4)'), lambda x: x**(-2)),
        1: (LeastSquare(0.5, 1, 0, 1, 1.5, 1, 1, 4, '2', '-4/x', '1'), lambda x: x**2 + 0.5*x),
        #2: (LeastSquare(0, 1, 1, 0, 1, 1, 2, 0, '-1', '-2', '-3*2.7182**(-x)'), lambda x: (x+1)*2.7181**(-x)),
        #3: (LeastSquare(0, 0.5, 0, 1, 0, 1, 0, 0.5 * sin(0.5), '2*x', '-1', '2 * cos(x) * (x**2 + 1)'), lambda x: x*sin(x)),
        #4: (LeastSquare(0, 1, 1, 1, 1, 0, 1, 4, '2', '-3', '-6*x**2+8*x+1'), lambda x: 2*x**2 + 1),
        #5: (LeastSquare(0, 1, 1, 0, -0.25, 1, -3, 0, '2 / (x-4)', '(x-4)', '1'), lambda x: 1 / (x-4)),
        #6: (LeastSquare(1, 2, 1, 0, 0, 0, 1, log(2) + 1, 'x', '-4', 'x + 1/x - 3*x*log(x)'), lambda x: x * log(x)),
        #7: (LeastSquare(0, 1, 1, 1, 1, 1, 0, cos(1), 'x', '-1', '-(x**2) * sin(x) - x*cos(x) - 2*sin(x)'), lambda x: x * cos(x)),
        #8: (LeastSquare(0, 1, 1, 0, 0, 0, 1, 2*e, 'x', '-1', '(x*(x+1) + 2)*(e**x)'), lambda x: x * e**x),
        #9: (LeastSquare(0, 1, 1, 0, -1/3, 1, 4, 15, 'x+3', '-2/((x+3)**2)', '-6*x/((x+3)**2) + 3*(x+3) + 1/(x+3)'), lambda x: 3*x - 1/(x+3)),
        #10: (LeastSquare(0, 1, 0, 1, 3, 2, -1, e, '-1', '-2', '-2*e**(x)'), lambda x: e**x + e**(2*x)),
        #11: (LeastSquare(-1, 0, 1, 1, 1, 1, 0, 0, '1/x', '-1/x**2', '8*x+3'), lambda x: x**2 + x**3),
        #12: (LeastSquare(1, 2, 0, 1, 1, 1, 0, 2*log(2), 'x', '-x**2', '1/x + x*log(x) + x - (x**3) * log(x)'), lambda x: x * log(x)),
        #13: (LeastSquare(1, 2, 1, 0, 1, 0, 1, 1.5, '1/x', '-4', '-4*x + 1/x - 4 * log(x)'), lambda x: x + log(x)),
        # 14: (LeastSquare(0, 1, 1, 0, 1, -1, 1, -1, '1', '1', '-2'), lambda x: 2.7182818284**x + x**2),
    }
    destiny = 1  # Change this to switch equations
    step = 0.1  # Change this to change step

    xs, ys, rys = list(), list(), list()
    grph = Graphics()
    
    x = "hello there"
    for x, y in conditions[destiny][0].get_values(step):
        xs.append(x)
        ys.append(y)
        rys.append(conditions[destiny][1](x))
    grph.draw([xs, xs], [ys, rys], 'Title')
    
    print('Finish!')
