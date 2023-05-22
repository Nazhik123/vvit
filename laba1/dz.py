a=float(input())
if a==0:
    print('не квадратное уравнение')
else:
    b=float(input())
    c=float(input())
    D=b**2-4*a*c
    if D<0:
        print('корней нет')
    elif D==0:
        print(-b/(2*a))
    else:
        print((-b+D**0.5)/(2*a))
        print((-b - D ** 0.5) / (2 * a))
