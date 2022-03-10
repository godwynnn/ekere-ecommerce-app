import math

def solution():


    x=float(input('Enter value for X: '))
    y=float(input('Enter value for Y: '))
    z=float(input('Enter value for Z: '))


    k=math.pow(z,y)

    m=math.pow(y,2)
    f=7*x*math.sin(k)+m-0.5*math.sqrt(x+y-2*x)

    if f < 4:
        print ('NEGATIVE')
    elif 4 <= f <=7:
        print('WORSE THAN AVERAGE')
    elif f==7:
        print('AVERAGE')
    elif 7< f <10:
        print('BETTER THAN AVERAGE')
    elif f==10:
        print('GREAT')
    else:
        print('ABOVE MAX LIMIT')
    print(f)

    # print(x)
solution()