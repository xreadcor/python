from math import *

def sum_naturlog(n):
    summa = 0
    for i in range(1,n):
        summa += log1p(i)
    return summa


z = sum_naturlog(5)
z