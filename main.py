try:
    from numerical import ReductionMethod
    from analytical import LeastSquare
    from graphics import Graphics
    from table_print import TablePrinter
    from config import Config
    from math import sin, cos, log, e
except Exception as mnfe:
    print(mnfe)
    exit()


DEBUG = False


def main():
    print('The program calculates numerical and analitical solution of the boundary values problem.')
    config = Config()
    config['a']    = float(input('Enter a: ')) if not DEBUG else 1
    config['b']    = float(input('Enter b: ')) if not DEBUG else 2
    
    config['g(x)'] =       input('Enter g(x): ') if not DEBUG else '1'
    config['p(x)'] =       input('Enter p(x): ') if not DEBUG else 'x**2'
    config['q(x)'] =       input('Enter q(x): ') if not DEBUG else '-x'
    config['f(x)'] =       input('Enter f(x): ') if not DEBUG else '(6 - (3*(x**3))) / (x**4)'
    
    config['a0']   = float(input('Enter a0: ')) if not DEBUG else 1
    config['a1']   = float(input('Enter a1: ')) if not DEBUG else 0
    config['A']    = float(input('Enter A: ')) if not DEBUG else 1
    
    config['b0']   = float(input('Enter b0: ')) if not DEBUG else 3
    config['b1']   = float(input('Enter b1: ')) if not DEBUG else 1
    config['B']    = float(input('Enter B: ')) if not DEBUG else 0.5

    step           = float(input('Enter step: ')) if not DEBUG else 0.1
    check =                input('Enter the required function (if do not have one - just press enter.)') if not DEBUG else 'x**(-2)'

    if not check == '': #or config.is_valid(check):
        rm = ReductionMethod(config)
        ls = LeastSquare(config)
        grp = Graphics()
        xpoints = list()
        rmpoints = list()
        lspoints = list()
        rpoints = list() if check != '' else None
        for set_rm, set_ls in zip(rm.get_values(step), ls.get_values(step)):
            xpoints.append(set_rm[0])
            rmpoints.append(set_rm[1])
            lspoints.append(set_ls[1])
            if rpoints is not None:
                rpoints.append(eval(check.replace('x', f'({set_rm[0]})')))
        if rpoints is not None:
            grp.draw([xpoints, xpoints, xpoints], [rmpoints, lspoints, rpoints], ['Reduction Method','Least Square Method','Original function'], 'Numerical Analisys Lab 2')
        print(ls.get_analytical_solution())
    else:
        print('Sorry, the conditions are not valid.')
        exit()


if __name__ == '__main__':
    main()
