from numerical import ReductionMethod


def main():
    '''The function arguments represent the following polynomial terms:
    Ly(x) = y"(x) + p(x)y'(x) + q(x)y(x) = f(x)
    with the following boundary conditions:
    a0*y(a) + a1*y'(a) = A,
    b0*y(b) + b1*y'(b) = B'''
    print("Ly(x) = y\"(x) + y'(x)*", end='')
    p = input()
    print('\b', end='')
    q = input(' + y(x)*')
    f = input(' = ')
    #temp_stuff = ReductionMethod()
    pass


if __name__ == '__main__':
    main()