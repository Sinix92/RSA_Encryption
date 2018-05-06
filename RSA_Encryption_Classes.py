import random

from Arithmetic_functions import is_prime_number, share_common_factor
from customized_decorators import singleton


class Person:
    PEOPLE = set()

    def __init__(self, name, nb_figures_prime_numbers, start_e_nb, end_e_nb, step_e_nb, start_k_nb, end_k_nb):
        self.name = name
        self.e_encrypt_public_key, self.n_encrypt_public_key, self.__d_decrypt_private_key = \
            RSAMethods.initialize_keys(nb_figures_prime_numbers, start_e_nb, end_e_nb, step_e_nb, start_k_nb, end_k_nb)
        self.packages = []
        self.received_packages = []
        self.dict_person_key = {}
        Person.PEOPLE.add(self)

    @classmethod
    def check_person(cls, person):
        return True if person in cls.PEOPLE else False

    def ask_connection(self, recipients):
        my_recipients = []

        for recipient in recipients:
            if recipient not in self.dict_person_key:
                self.create_package("connection_request", recipients=recipient)
                my_recipients.append(recipient)

        if my_recipients:
            self.send_packages()
            for recipient in my_recipients:
                recipient.read_packages()

            self.read_packages()

    def provide_connection(self):
        self.create_package("public_key")
        self.send_packages()

    def create_package(self, package_type, message=None, recipients=None):
        if package_type == "public_key":
            self.packages.append(Package(package_type, (self.e_encrypt_public_key, self.n_encrypt_public_key), self))
        elif package_type == "connection_request":
            self.packages.append(Package(package_type, "N/A", self, recipients))
        elif package_type == "message" and message and recipients:
            for recipient in recipients:

                if Person.check_person(recipient):
                    if recipient in self.dict_person_key:
                        e_encryption_public_key = self.dict_person_key[recipient][0]
                        n_encryption_public_key = self.dict_person_key[recipient][1]
                        self.packages.append(Package(package_type,
                                                     RSAMethods.encrypt(message, e_encryption_public_key,
                                                                        n_encryption_public_key)
                                                     , self, recipient))
                    else:
                        # ask for public keys
                        self.ask_connection([recipient])
                        self.create_package(package_type, message, [recipient])

    def send_packages(self):
        for package in self.packages:
            if package.recipient == "All":
                for person in Person.PEOPLE - {self}:
                    person.receive_package(package)
                    print("Message sent from: {} to: {} Description: {}".format(self.name, person.name, package.header))
            else:
                package.recipient.receive_package(package)
                print("Message sent from: {} to: {} Description: {}".format(self.name, package.recipient.name,
                                                                            package.header))

        del self.packages[:]

    def receive_package(self, package):
        self.received_packages.append(package)

    def read_packages(self):
        for package in self.received_packages:
            if package.header == "public_key":
                if package.sender not in self.dict_person_key:
                    self.dict_person_key[package.sender] = package.content
                    print("{} is speaking: Public Keys coming from: {} Public Key: {}".format(self.name,
                                                                                              package.sender.name,
                                                                                              package.content))
            elif package.header == "connection_request":
                print("{} is speaking: Connection Request coming from: {}".format(self.name, package.sender.name))
                self.provide_connection()
            elif package.header == "message":
                decrypted_message = RSAMethods.decrypt(package.content, self.__d_decrypt_private_key,
                                                       self.n_encrypt_public_key)
                print("{} is speaking: Message coming from: {} Content: {}".format(self.name, package.sender.name,
                                                                                   decrypted_message))

        del self.received_packages[:]


class Package:

    def __init__(self, header, content, sender, recipient="All"):
        self.header = header
        self.content = content
        self.sender = sender
        self.recipient = recipient


class CharToAsciiCode:

    @staticmethod
    def encrypt(message):

        '''
        :param message: string of characters
        :return: list of ascii codes
        '''

        list_ascii_codes = []
        for letter in message:  # each character in the message is turned into an ASCII Code
            list_ascii_codes.append(ord(letter))

        return list_ascii_codes

    @staticmethod
    def decrypt(list_ascii_codes):

        '''
        :param list_ascii_codes: list of ascii codes
        :return: string of characters
        '''

        decrypted_msg_list = []
        for decrypted_code in list_ascii_codes:
            letter = chr(decrypted_code)  # each ASCII Code is turned into a character
            decrypted_msg_list.append(letter)

        return ''.join(decrypted_msg_list)


class RSAMethods:

    @staticmethod
    def initialize_keys(nb_figures_prime_numbers, start_e_nb, end_e_nb, step_e_nb, start_k_nb, end_k_nb):

        '''
        :param nb_figures_prime_numbers: If 2, then the method will yield 2-digit prime numbers
        :param start_e_nb: e will be randomly drawn from a list beginning with this parameter
        :param end_e_nb: e will be randomly drawn from a list ending with this parameter
        :param step_e_nb: the step between each element in the list of possible 'e'
        :param start_k_nb: k will be randomly drawn from a list beginning with this parameter
        :param end_k_nb: k will be randomly drawn from a list ending with this parameter
        :return: returns the public keys e, n and the private key d

        Watch out:
        n has to be greater than the message, let's say n is 324, then the ascii message has to be below 324
        e has to be odd and must not share any common factor with Phi(n)
        k has to be chosen so that ((k*Phi(n)+1)/e) to be an integer, sometimes it is not possible so we have to chose
        new parameters (n and e)
        '''

        level_of_dozen = 10 ** (nb_figures_prime_numbers - 1)
        list_prime_numbers = PrimeNumbers(level_of_dozen, (10 * level_of_dozen) - 1).list

        list_k_numbers = []
        while not list_k_numbers:  # sometimes list_k_numbers can be empty, hence the loop here
            p1 = random.choice(list_prime_numbers)
            list_prime_numbers.remove(p1)  # p2 must be different from p1, so we remove p1 from the list
            p2 = random.choice(list_prime_numbers)
            n = p1 * p2
            phi_n = (p1 - 1) * (p2 - 1)

            list_e_numbers = ENumbers(start_e_nb, end_e_nb, step_e_nb, phi_n).list
            e = random.choice(list_e_numbers)

            list_k_numbers = KNumbers(start_k_nb, end_k_nb, phi_n, e).list

        k = random.choice(list_k_numbers)

        d = int(((k * phi_n) + 1) / e)

        return e, n, d

    @staticmethod
    def encrypt(message, e_encryption_public_key, n_encryption_public_key):

        '''
        :param message: string of characters to encrypt
        :param e_encryption_public_key: public key that belongs to the recipient to encrypt the message
        :param n_encryption_public_key: public key that belongs to the recipient to encrypt the message
        :return: list of encrypted codes
        '''

        # turn char in ascii code
        list_ascii_codes = CharToAsciiCode.encrypt(message)

        # process to encrypt with RSA
        list_encrypted_codes = []
        for ascii_code in list_ascii_codes:
            encrypted_code = (ascii_code ** e_encryption_public_key) % n_encryption_public_key
            list_encrypted_codes.append(encrypted_code)

        return list_encrypted_codes

    @staticmethod
    def decrypt(list_encrypted_codes, d_decryption_private_key, n_encryption_public_key):

        '''
        :param list_encrypted_codes: list of encrypted codes to decrypt
        :param d_decryption_private_key: private key that belongs to the recipient to decrypt the message
        :param n_encryption_public_key: public key that belongs to the recipient to decrypt the message
        :return: the decrypted message
        '''

        # process to decrypt with RSA
        list_ascii_codes = []
        for encrypted_code in list_encrypted_codes:
            ascii_code = (encrypted_code ** d_decryption_private_key) % n_encryption_public_key
            list_ascii_codes.append(ascii_code)

        # turn ascii codes in char
        decrypted_message = CharToAsciiCode.decrypt(list_ascii_codes)

        return decrypted_message


class ListNumbers:
    def __init__(self, start, end):
        self.start = start
        self.end = end


@singleton
class PrimeNumbers(ListNumbers):

    def __init__(self, start, end):
        super().__init__(start, end)
        self.list = [i for i in range(start, end + 1) if is_prime_number(i)]


@singleton
class ENumbers(ListNumbers):

    def __init__(self, start, end, step, phi_n):
        super().__init__(start, end)
        self.step = step
        self.list = [i for i in range(start, end + 1, step) if not share_common_factor(i, phi_n) and (i % 2 != 0)]


class KNumbers(ListNumbers):

    def __init__(self, start, end, phi_n, e):
        super().__init__(start, end)
        self.list = [i for i in range(start, end + 1) if ((i * phi_n) + 1) / e == ((i * phi_n) + 1) // e]
