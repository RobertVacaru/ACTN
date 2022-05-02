import math
import random
import time
import timeit
from datetime import datetime

import numpy as np


def number_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def exponentiation(a, k, n):
    b = 1
    if k == 0:
        return b
    A = a
    k = number_to_base(k, 2)
    if k[len(k) - 1] == 1:
        b = a
    for i in range(len(k) - 2, -1, -1):
        A = pow(A, 2, n)
        if k[i] == 1:
            b = A * b % n
    return b


def generate_e(a):
    e = 0
    while a % 2 == 0:
        e += 1
        a = a / 2
    a1 = a
    return e, a1


def jacobi_symbol(a, n):
    s = 0
    if a == 0:
        return 0
    elif a == 1:
        return 1
    e, a1 = generate_e(a)
    if e % 2 == 0:
        s = 1
    else:
        if n % 8 == 1 or n % 8 == 7:
            s = 1
        elif n % 8 == 3 or n % 8 == 5:
            s = -1
    if n % 4 == 3 and a1 % 4 == 3:
        s = -s
    n1 = n % a1
    if a1 == 1:
        return s
    else:
        return s * jacobi_symbol(n1, a1)


def solovay_strassen(n, t):
    for i in range(1, t):
        a = random.randint(2, n - 2)
        r = exponentiation(a, (n - 1) / 2, n)
        if r != 1 and r != n - 1:
            return "composite"
        s = jacobi_symbol(a, n)
        if r % n != s % n:
            return "composite"
    return "prime"


def lucas_lehmer(n, s, type):
    for i in range(2, int(math.sqrt(s)) + 1):
        if s % i == 0:
            return "composite"
    u = 4
    for k in range(1, s - 1):
        if type == 1:
            u = (u * u - 2) % n
        else:
            u = mersenne_exp((u * u - 2), s)
    if u == 0:
        return "prime"
    else:
        return "composite"


def mersenne_exp(a, n):
    exp = pow(2, n)
    a1 = 1
    while a1 * exp < a:
        a1 += 1
    a1 -= 1
    a0 = a - a1 * exp
    if a0 + a1 < pow(2, n) - 1:
        result = a0 + a1
    elif pow(2, n) - 1 <= a0 + a1 < 2 * (pow(2, n) - 1):
        result = a0 + a1 - (pow(2, n) - 1)
    return result


# print(exponentiation(2, 3, 3))
print(solovay_strassen(101, 1000))
# print(jacobi_symbol(1235, 20003))
s = random.randint(3,5000)
n = pow(2, s) - 1
start = timeit.default_timer()
print(lucas_lehmer(n, s, 1))
end = timeit.default_timer()
print(str(end-start))
start = timeit.default_timer()
print(lucas_lehmer(n, s, 0))
end = timeit.default_timer()
print(str(end-start))
