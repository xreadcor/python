from math import *

def prod_naturlog(n):
    prod = 1
    for i in range(1,n+1):
        prod *= i
    x = log1p(prod)
    return x

x = prod_naturlog(5)
print(x)