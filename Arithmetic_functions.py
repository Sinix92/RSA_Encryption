import random
import collections
import matplotlib.pyplot as plt

"""
Fundamental Theorem of Arithmetic:
Every positive integer (except the number 1) can be represented in exactly one way apart from rearrangement as a product
of one or more primes.
"""


# Prime Number Function: Trivial function (not used in the code but to check the results of Primality Test function)
def is_prime_number(number):
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


# Randomly draw a prime number
def draw_prime(max_nb, min_nb=2):
    my_prime = random.randint(min_nb, max_nb)
    set_of_drawn_nb = set()
    while not fermat_primality_test(my_prime, 20):
        set_of_drawn_nb.add(my_prime)
        while my_prime in set_of_drawn_nb:
            my_prime = random.randint(min_nb, max_nb)

    return my_prime


# Used in the code to check if the input integer is a Prime number (reduced complexity compared to trivial function)
def fermat_primality_test(p, nb_tests):
    # randomly draw an integer a < p
    a = random.randint(2, p - 1)
    # find the gcd(a,p) with Euclidean Algorithm
    greatest_common_divisor = gcd(p, a)

    # if gcd(a,p) != 1 then p is not prime and we need to draw again a and p
    if greatest_common_divisor != 1:
        return False
    # else: we can proceed to the second test
    else:
        result_test = fast_modular_exponentiation(a, p - 1, p)
        # if result test is not 1, then we are sure p is not Prime
        if result_test != 1:
            return False
        # else, as we could have drawn an "a" that is a fool, we are going to test again P with another a, to be sure
        else:
            if nb_tests == 1:
                return True
            else:
                return fermat_primality_test(p, nb_tests - 1)


# Sieve of Eratosthenes: to get all the prime numbers from 2 to max_number
def sieve_of_eratosthenes(max_number):
    if max_number >= 2:
        set_prime_numbers = set(range(2, max_number + 1))
        for i in range(2, int(max_number ** 0.5) + 1):
            if i in set_prime_numbers:
                composite_number = i * i
                while composite_number <= max_number:
                    if composite_number in set_prime_numbers:
                        set_prime_numbers.discard(composite_number)
                    composite_number += i

        return set_prime_numbers


# Find Prime Factors of a given number
def find_prime_factors(number):
    if not is_prime_number(number):
        set_prime_numbers = [i for i in range(2, (number // 2) + 1) if is_prime_number(i)]

        set_prime_factors = []
        for prime_number in set_prime_numbers:
            if number % prime_number == 0:
                set_prime_factors.append(prime_number)

    else:
        set_prime_factors = [number]

    return set_prime_factors


# Find the Prime Factorization of a given number
def find_prime_factorization(number, set_prime_factors):
    set_factorization = []
    for prime_factor in set_prime_factors:
        power = -1
        while number % prime_factor == 0:
            power += 1
            number = number / prime_factor
        set_factorization.append((prime_factor, prime_factor ** power))

    return set_factorization


""" 
Discrete Logarithm Problem:
Given 12, find the exponent 3 needs to be raised to: 3 ** x % 17 = 12?
The function just below helps in retrieving the different solutions to this equation.

Diffie-Hellman Key Exchange (used in TLS/SSL): 
https://www.khanacademy.org/computing/computer-science/cryptography/modern-crypt/v/diffie-hellman-key-exchange-part-2
"""


def find_remainders_prime_modulo(generator, prime_modulus, max_power):
    list_remainders = []
    dict_remainders = {}
    for power in range(1, max_power + 1):
        remainder = generator ** power % prime_modulus
        list_remainders.append(remainder)

        if remainder not in dict_remainders:
            dict_remainders[remainder] = [power]
        else:
            dict_remainders[remainder].append(power)

    return collections.Counter(list_remainders), dict_remainders


# Phi function (Euler's Totient/ Indicatrice d'Euler)
def phi_function(number):
    if number == 1:
        return 1
    elif is_prime_number(number):
        return number - 1
    else:
        factors_list = []
        # no_factors_list = []
        nb_of_no_factor = 0

        for n in range(1, number):
            if n != 1 and number % n == 0:
                factors_list.append(n)
            else:
                for factor in factors_list:
                    if n % factor == 0:
                        break
                else:
                    # no_factors_list.append(n)
                    nb_of_no_factor += 1

        # return no_factors_list
        return nb_of_no_factor


def share_common_factor(nb1, nb2):
    nb1, nb2 = sorted([nb1, nb2])

    if nb2 % nb1 == 0:
        return True
    else:
        for nb in range(2, (nb1 // 2) + 1):
            if nb1 % nb == 0 and nb2 % nb == 0:
                return True

        return False


# Euclidean Algorithm: to find the gcd in an easy way
def gcd(nb1, nb2):
    if any((nb1, nb2)):
        nb1 = abs(nb1)
        nb2 = abs(nb2)
        if nb1 < nb2:
            nb1, nb2 = nb2, nb1
        if nb2 == 0:
            return nb1
        else:
            nb3 = nb1 % nb2
            return gcd(nb2, nb3)


# Fast Modular Exponentiation helps in calculating modulo with big numbers: a ** b % c
def fast_modular_exponentiation(a, b, c):
    k = -1
    set_of_results = set()
    dict_modulo_power_of_two = {}
    binary_nb = bin(b).split('b')[-1]

    for bit in reversed(binary_nb):
        k += 1
        if bit == '1':
            set_of_results.add(2 ** k)

    modulo_power_of_two(a, 2 ** k, c, dict_modulo_power_of_two)

    product = 1
    for power in dict_modulo_power_of_two:
        if power in set_of_results:
            product *= dict_modulo_power_of_two[power]

    return product % c


def modulo_power_of_two(a, b, c, dict_results):
    if b == 1:
        result = a ** 1 % c
    else:
        temp_result = modulo_power_of_two(a, b // 2, c, dict_results)
        result = (temp_result * temp_result) % c

    dict_results[b] = result
    return result


# def test_prime_factorization():
#     my_number = 437231
#     print(find_prime_factorization(my_number, find_prime_factors(my_number)))
#
#
# def test_find_remainders_prime_modulo():
#     my_generator = 3
#     my_prime_modulus = 17
#     my_multiplier = 1
#     my_list_of_remainders, my_dict_remainders = find_remainders_prime_modulo(my_generator, my_prime_modulus,
#                                                                              my_prime_modulus * my_multiplier)
#     print(my_list_of_remainders)
#     print(my_dict_remainders)
#
#
# def test_phi_function():
#     # my_number = 15
#     # print(phi_function(my_number))
#
#     y_coordinates = []
#     for n in range(1, 1001):
#         y_coordinates.append(phi_function(n))
#
#     plt.scatter(range(1, 1001), y_coordinates, s=1)
#     plt.xlabel('n')
#     plt.ylabel('Phi(n)')
#     plt.ylim([0, 1000])
#     plt.xlim([0, 1000])
#     plt.show()


if __name__ == '__main__':
    # test_prime_factorization()
    # test_find_remainders_prime_modulo()
    # test_phi_function()
    # share_common_factor(100, 15)
    # print(sieve_of_eratosthenes(100))
    # print(gcd(192, 270))
    # print(fermat_primality_test(32416190071, 20))
    # print(fermat_primality_test(90071992547409932343, 20))
