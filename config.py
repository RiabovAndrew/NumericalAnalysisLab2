try:
    from sympy import Symbol, simplify, diff
    from sympy.utilities.lambdify import implemented_function
    from math import sin, cos, log  # 'log', 'tan' and all other math functions shall be imported here if needed.
    from typing import Dict, Union, Callable
except ModuleNotFoundError as mnfe:
    print(mnfe)
    exit()


DEBUG : bool = False


class Config:
    '''Storing and verification for ReductionMethod'''


    __values : Dict[str, Union[str, float]]


    def __init__(self):
        self.__values = {
            'a' : None, 'b' : None,
            'a0' : None, 'a1' : None, 'A' : None,
            'b0' : None, 'b1' : None, 'B' : None,
            'g(x)' : '1.0', 'p(x)' : None, 'q(x)' : None, 'f(x)' : None
        }


    def __getitem__(self, key : str):
        if key in self.__values:
            return self.__values[key]
        else:
            raise KeyError()

    # TODO: type checking?
    def __setitem__(self, key, value):
        if key in self.__values.keys():
            self.__values[key] = value
        else:
            raise ValueError()


    def is_valid(self, accurate : str) -> bool:
        for key in self.__values.keys():
            if key is None:
                return False

        x = Symbol('x')

        if float(self.__values['a']) >= float(self.__values['b']):
            return False

        y = eval(accurate)

        a = float(self.__values['a'])
        b = float(self.__values['b'])
        a0 = float(self.__values['a0'])
        a1 = float(self.__values['a1'])
        b0 = float(self.__values['b0'])
        b1 = float(self.__values['b1'])
        A = float(self.__values['A'])
        B = float(self.__values['B'])

        y_a = y.evalf(subs = {x : a})
        dy_a = diff(y, x).evalf(subs = {x : a})
        y_b = y.evalf(subs = {x : b})
        dy_b = diff(y, x).evalf(subs = {x : b})

        dy = diff(y, x)
        ddy = diff(dy, x)

        # a0*y(a) + a1*y'(a) - A = 0
        if simplify(eval(f"({a0})*({y_a}) + ({a1})*({dy_a}) - ({A})")) != 0:
            return False

        # b0*y(b) + b1*y'(b) - B = 0
        if simplify(eval(f"({b0})*({y_b}) + ({b1})*({dy_b}) - ({B})")) != 0:
            return False

        # g(x)*y"(x) + p(x)*y'(x) + q(x)*y(x) = f(x)
        if simplify(eval(f"({ddy}) + ({self.__values['p(x)']})*({dy})/({self.__values['g(x)']}) + ({self.__values['q(x)']})*({y})/({self.__values['g(x)']}) - ({self.__values['f(x)']})/({self.__values['g(x)']})")) != 0:
            return False
        
        return True


if __name__ == '__main__':  # Some tests.
    if not DEBUG:
        print('WARNING! This file is not intended to be main file. Consider running "main.py".')
        print('If you want to just test if it all works - change the DEBUG variable to True.')
        exit()
    else:
        print('ReductionMethodConfig...')

        config = Config()
        config['a'] = 0
        config['b'] = 1

        config['g(x)'] = '1'
        config['p(x)'] = '1'
        config['q(x)'] = '-2'
        config['f(x)'] = '2*(-x**2 + x + 1)'

        config['a0'] = 1
        config['a1'] = 0
        config['A'] = 1

        config['b0'] = 1
        config['b1'] = -1
        config['B'] = 1

        print(config.is_valid('x**(-2)'))