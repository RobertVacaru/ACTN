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
    omega = (p - 1) * (q - 1) * (r - 1)
    e = coprime(omega)
    d = pow(e, -1, omega)
    return p, q, r, n, e, d


def simple_encrypt(x, e, n):
    return pow(x, e, n)


def simple_decrypt(y, d, n):
    return pow(y, d, n)


# Multiprime
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
    result = garner_for_three(x_p, x_q, x_r, p, q, r)
    if result == x:
        print("Decryption successful with Faster Multiprime Rsa")
    end = time.time()
    print("Time" + f"{start - end}")


def congruent(a, modulo):
    for i in range(1, modulo):
        if i % modulo == a % modulo:
            return 1


def garner_for_three(x_p, x_q, x_r, p, q, r):
    x1 = x_p
    alpha = ((x_q - x1) * pow(p, -1, q)) % q
    x2 = x1 + p * alpha
    beta = ((x_r - x2) * pow(q * p, -1, r)) % r
    return beta * q * p + x2


def generate_x_indices(y, indices, d):
    # (y mod p)^d mod(p-1) mod p pentru x_p (T.Fermat)
    return pow((y % indices), (d % (indices - 1)), indices)


# Multipower
def simple_multipower_rsa(p, q, n, e, d):
    start = time.time()
    x = random.randint(0, n)
    y = simple_encrypt(x, e, n)
    result = simple_decrypt_multipower(y, d, n, p, q)
    if result == x:
        print("Decryption successful with Simple Multipower Rsa")
    end = time.time()
    print("Time" + f"{start - end}")


def faster_multipower_rsa(p, q, n, e, d):
    start = time.time()
    x = random.randint(0, n)
    y = simple_encrypt(x, e, n)
    result = faster_decrypt_multipower(y, d, n, p, q)
    if result == x:
        print("Decryption successful with Faster Multipower Rsa")
    end = time.time()
    print("Time" + f"{start - end}")


def generate_parameters_multipower(p, q):
    n = p * p * q
    omega = (p * p - p) * (q - 1)
    e = coprime(omega)
    d = pow(e, -1, omega)
    return n, e, d


def simple_decrypt_multipower(y, d, n, p, q):
    value = pow(y, d, n)
    # x_p^2 = y^d mod n mod p^2
    x_p = value % (p * p)
    # x_q = y^d mod n mod q
    x_q = value % q
    return garner_for_two(x_p, x_q, p * p, q)


def faster_decrypt_multipower(y, d, n, p, q):
    x0 = pow(y % p, d % (p - 1), p)
    alpha = ((y - pow(x0, e, p * p)) // p) % p
    z = (e * pow(x0, e - 1, p * p)) % p
    x1 = (alpha * pow(z, -1, p))
    xp2 = x1 * p + x0
    x_q = pow(y, d, n) % q
    return garner_for_two(xp2, x_q, p * p, q)


def garner_for_two(x_p, x_q, p, q):
    x1 = x_p
    alpha = ((x_q - x1) * pow(p, -1, q)) % q
    return x1 + p * alpha


# Left to right binary
def number_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def right_to_left(x, n, m):
    n = number_to_base(n, 2)
    k = len(n)
    y = 1
    for i in range(0, k):
        y = (y * y) % m
        if n[i] == 1:
            y = (y * x) % m
    return y


def faster_multiprime_rsa_with_binary(p, q, r, n, e, d):
    start = time.time()
    x = random.randint(0, n)
    y = simple_encrypt(x, e, n)
    x_p = right_to_left(y % p, d % (p - 1), p)
    x_q = right_to_left(y % q, d % (q - 1), q)
    x_r = right_to_left(y % r, d % (r - 1), r)
    result = garner_for_three(x_p, x_q, x_r, p, q, r)
    if result == x:
        print("Decryption successful with Faster Multiprime Rsa with Binary")
    end = time.time()
    print("Time" + f"{start - end}")


# Left to right Fixed Window

def fixed_window(x, n, m, base):
    x_list = []
    for i in range(0, base):
        x_list.append(0)
    x_list[0] = 1
    for i in range(1, base):
        x_list[i] = (x_list[i - 1] * x) % m
    n = number_to_base(n, base)
    k = len(n)
    y = 1
    for i in range(k):
        y = pow(y, base, m)
        y = y * x_list[n[i]] % m
    return y


def faster_multiprime_rsa_with_fixed_window(p, q, r, n, e, d):
    start = time.time()
    x = random.randint(0, n)
    y = simple_encrypt(x, e, n)
    x_p = fixed_window(y % p, d % (p - 1), p, 2)
    x_q = fixed_window(y % q, d % (q - 1), q, 2)
    x_r = fixed_window(y % r, d % (r - 1), r, 2)
    result = garner_for_three(x_p, x_q, x_r, p, q, r)
    if result == x:
        print("Decryption successful with Faster Multiprime Rsa with Fixed Window")
    end = time.time()
    print("Time" + f"{start - end}")


# Multiprime
##
p, q, r, n, e, d = generate_parameters()
simple_multiprime_rsa(p, q, r, n, e, d)
faster_multiprime_rsa(p, q, r, n, e, d)
# Multipower
##
n, e, d = generate_parameters_multipower(p, q)
simple_multipower_rsa(p, q, n, e, d)
faster_multipower_rsa(p, q, n, e, d)
# Chains
##
p, q, r, n, e, d = generate_parameters()
# print("Right to left binary compared to pow:" + f"{right_to_left(x, n, m) == pow(x, n, m)}")
faster_multiprime_rsa_with_binary(p, q, r, n, e, d)
faster_multiprime_rsa_with_fixed_window(p, q, r, n, e, d)

##
# start = time.time()
# print("Right to left Fixed window compared to pow:" + f"{fixed_window(x, n, m, 2) == pow(x, n, m)} ")
# end = time.time()
# print("Time" + f"{start - end}")
