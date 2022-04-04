import random
import time

import Cryptodome.Util.number as crypto

from math import gcd as gcd


def coprime(a):
    for i in range(2, a):
        if gcd(a, i) == 1:
            return i


def generate_parameters():
    while True:
        p = crypto.getPrime(512)
        q = crypto.getPrime(512)
        r = crypto.getPrime(512)
        if p != q and p != r and q != r:
            break
    n = p * q * r
    print(crypto.size(n))
    omega = (p - 1) * (q - 1) * (r - 1)
    e = coprime(omega)
    d = pow(e, -1, omega)
    return p, q, r, n, e, d


def simple_encrypt(x, e, n):
    return pow(x, e, n)


def simple_decrypt(y, d, n):
    return pow(y, d, n)


def simple_multiprime_rsa(p, q, r, n, e, d):
    start = time.time()
    x = crypto.getPrime(512)
    y = simple_encrypt(x, e, n)
    result = simple_decrypt(y, d, n)
    if result == x:
        print("Decryption successful with Simple Multiprime Rsa")
    end = time.time()
    print("Time" + f"{start - end}")


def faster_multiprime_rsa(p, q, r, n, e, d):
    start = time.time()
    x = random.randint(0, n)
    y = simple_encrypt(x, e, n)
    x_p = generate_x_indices(y, p, d)
    x_q = generate_x_indices(y, q, d)
    x_r = generate_x_indices(y, r, d)
    result = garner(x_p, x_q, x_r, p, q, r)
    if result == x:
        print("Decryption successful with Faster Multiprime Rsa")
    end = time.time()
    print("Time" + f"{start - end}")


def congruent(a, modulo):
    for i in range(1, modulo):
        if i % modulo == a % modulo:
            return 1


def garner(x_p, x_q, x_r, p, q, r):
    x1 = x_p
    alpha = ((x_q - x1) * pow(p, -1, q)) % q
    x2 = x1 + p * alpha
    beta = ((x_r - x2) * pow(q * p, -1, r)) % r
    return beta * q * p + x2


def generate_x_indices(y, indices, d):
    return pow((y % indices), (d % (indices - 1)), indices)


p, q, r, n, e, d = generate_parameters()
simple_multiprime_rsa(p, q, r, n, e, d)
faster_multiprime_rsa(p, q, r, n, e, d)
