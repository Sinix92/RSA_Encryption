import collections
import matplotlib.pyplot as plt

"""
Fundamental Theorem of Arithmetic:
Every positive integer (except the number 1) can be represented in exactly one way apart from rearrangement as a product
of one or more primes.
"""


# Prime Number Function
def is_prime_number(number):
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True


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


def test_prime_factorization():
    my_number = 437231
    print(find_prime_factorization(my_number, find_prime_factors(my_number)))


def test_find_remainders_prime_modulo():
    my_generator = 3
    my_prime_modulus = 17
    my_multiplier = 1
    my_list_of_remainders, my_dict_remainders = find_remainders_prime_modulo(my_generator, my_prime_modulus,
                                                                             my_prime_modulus * my_multiplier)
    print(my_list_of_remainders)
    print(my_dict_remainders)


def test_phi_function():
    # my_number = 15
    # print(phi_function(my_number))

    y_coordinates = []
    for n in range(1, 1001):
        y_coordinates.append(phi_function(n))

    plt.scatter(range(1, 1001), y_coordinates, s=1)
    plt.xlabel('n')
    plt.ylabel('Phi(n)')
    plt.ylim([0, 1000])
    plt.xlim([0, 1000])
    plt.show()


if __name__ == '__main__':
    # test_prime_factorization()
    # test_find_remainders_prime_modulo()
    # test_phi_function()
    # share_common_factor(100, 15)
    print(sieve_of_eratosthenes(100))
