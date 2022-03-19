from random import random, randrange


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def baseToNumber(n, b):
    number = 0
    power = 0
    for i in range(len(n) - 1, -1, -1):
        number += n[i] * pow(b, power)
        power += 1
    return number


# print(numberToBase(29, 11))


def polynom(x, digits):
    power_of_x = len(digits)
    poly = 0
    for dig in digits:
        poly = poly + dig * (x ** power_of_x)
        power_of_x -= 1
    return poly


def algorithm_encoding(m, p, s):
    m_tuple = numberToBase(m, p)
    k = len(m_tuple) + 1
    n = 2 * s + k
    y = []
    for i in range(1, n + 1):
        y.append(polynom(i, m_tuple) % p)
    return y, k


def compare_y_z(z, y):
    counter = 0
    poz = 1
    final_poz = 0
    for i in range(len(z)):
        if z[i] != y[i]:
            counter += 1
            final_poz = poz
        poz += 1
    return counter, final_poz


def generate_array_a(n):
    a = []
    for i in range(1, n + 1):
        a.append(i)
    return a


def generate_random_a(s, k):
    x = len(s)
    list_a = []
    final_list_a = []
    for i in range(1 << x):
        list_a.append([s[j] for j in range(x) if (i & (1 << j))])
    # print(list_a)
    for element in list_a:
        if len(element) == k:
            final_list_a.append(element)
    return final_list_a


def algorithm_decoding(z, y, k, s, p):
    counter, poz = compare_y_z(z, y)
    array_a = generate_array_a(k + 2 * s)

    a_list = generate_random_a(array_a, k)
    # print(a_list)

    if counter:
        # (element_j / (element_j - element_i))
        for element in a_list:
            sum = 0
            for element_i in element:
                multiply = 1
                diff = 1
                for element_j in [v for v in element if v != element_i]:
                    multiply *= element_j
                    diff *= element_j - element_i
                multiply *= find_mod_inv(diff, p)
                multiply *= z[element_i - 1]
                sum += multiply
            # print("Sum:" + f'{sum % p}')
            if sum % p == 0:
                result = find_polynom(element, z, p, k)
                return result


def generate_polynom(list, k, p):
    a = []
    # for i in range(0, k + 1):
    #     a.append(0)
    a.append(0)
    a.append(0)
    for i in range(0, k - 1):
        a.append(0)
        if i == 0:
            a[i] = 1
            a[i + 1] = (list[i] + list[i + 1]) % p
            a[i + 2] = (list[i] * list[i + 1]) % p
            # print(a)

        else:
            a[i + 2] = (a[i + 1] * list[i + 1]) % p
            for j in range(len(a) - 2, 0, -1):
                a[j] += (a[j - 1] * list[i + 1])
                a[j] %= p
            a[0] = 1
    for i in range(0, k + 1):
        a[i] %= p
    # print(a)
    return a


def find_mod_inv(a, m):
    for x in range(1, m):
        if (a % m) * (x % m) % m == 1:
            return x
    raise Exception('The modular inverse does not exist.')


def find_polynom(A, z, p, k):
    # final_result = [0, 0, 0]
    # for element_i in A:
    #     multiply = 1
    #     coef_list = []
    #     for element_j in [v for v in A if v != element_i]:
    #         aux = element_i - element_j
    #         if aux > 0:
    #             inv = pow(aux, -1, p)
    #         else:
    #             inv = pow(-aux, -1, p)
    #         multiply *= inv
    #         print(multiply)
    #         coef_list.append(-element_j)
    #     # print(coef_list)
    #     result = generate_polynom(coef_list, len(coef_list))
    #     multiply *= z[element_i - 1]
    #     for j in range(0, len(result)):
    #         result[j] *= multiply
    #     print(result)
    #     for i in range(0, len(final_result)):
    #         final_result[i] += result[i]
    #         final_result[i] %= p
    #
    # print(final_result)
    # return final_result
    coefs = []

    for i in range(k):
        coefs.append(z[A[i] - 1])
    # print(coefs)
    result = []
    for index, i in enumerate(A):
        divide = 1
        poly_coefs = []
        for j in A:
            if i != j:
                divide *= i - j
                divide %= p
                poly_coefs.append(-j)
        # inv modular peste j-i
        coefs[index] *= find_mod_inv(divide, p)
        coefs[index] %= p
        # print(coefs)
        # coef rezultati pentru polinom
        result_coefs = generate_polynom(poly_coefs, len(poly_coefs), p)
        # print(result_coefs)
        #   coef rezultati ii inmultesc
        aux = []
        for elem in result_coefs:
            aux.append(coefs[index] * elem % p)
        result.append(aux)

    # print(result)
    final_result = []
    for i in range(k):
        final_result.append(0)
    for tuple in result:
        for poz in range(len(tuple)):
            final_result[poz] += tuple[poz]
    for i in range(k):
        final_result[i] %= p
    return final_result


def textToAscii(text):
    return ''.join(str(ord(c)) for c in text)


def generate_z(y, p):
    i = randrange(0, len(y))
    j = randrange(0, p)
    while j == y[i]:
        j = randrange(0, p)
    z = y.copy()
    z[i] = j
    return z


def main_code():
    text = "hi"
    ascii_text = int(textToAscii(text))
    print("Text in ascii:" + f'{ascii_text}')
    p = 11

    m = numberToBase(ascii_text, p)
    print("m:" + f'{m}')
    y, k = algorithm_encoding(ascii_text, p, 1)
    print("y:" + f'{y}')
    z = generate_z(y, p)
    print("z:" + f'{z}')
    result = algorithm_decoding(z, y, k, 1, p)
    # print(result)
    result = result[:len(result) - 1]
    print("Coef o final polynom:" + f'{result}')
    print("Final ascii text:"f'{baseToNumber(result, p)}')


# z = [9, 2, 6, 5, 8]
# print("m:" + f'{29}')
# y, k = algorithm_encoding(29, 11, 1)
# print("y:" + f'{y}')
# result = algorithm_decoding(z, y, k, 1, 11)
# result = result[:len(result) - 1]
# print("Coef o final polynom:" + f'{result}')
# print(baseToNumber(result, 11))
main_code()
