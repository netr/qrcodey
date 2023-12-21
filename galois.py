from copy import copy
from functools import cache
from typing import Dict, List

from const import GENERATOR_POLYNOMIALS
from encoder import AlphanumericEncoder


class GaloisField:
    @staticmethod
    @cache
    def get_exponents_table() -> Dict[int, int]:
        exps = {0: 1}
        value = 1
        for exp in range(1, 255):
            value = (value << 1) ^ 285 if value & 0x80 else value << 1
            exps[exp] = value
        return exps

    @staticmethod
    @cache
    def get_log_table() -> Dict[int, int]:
        exps = GaloisField.get_exponents_table()
        return {value: exp for exp, value in exps.items()}

    @staticmethod
    def multiply(a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        exps, log = GaloisField.get_exponents_table(), GaloisField.get_log_table()
        return exps[(log[a] + log[b]) % 255]

    @staticmethod
    def divide(a: int, b: int) -> int:
        exps, log = GaloisField.get_exponents_table(), GaloisField.get_log_table()
        return exps[(log[a] + log[b] * 254) % 255]

    @staticmethod
    def get_exp(num: int) -> int:
        """
        There are φ(255) = 192 primitive elements in GF(256), where φ is Euler's totient function.
        https://dev.to/maxart2501/let-s-develop-a-qr-code-generator-part-iii-error-correction-1kbm
        https://en.wikiversity.org/wiki/Reed%E2%80%93Solomon_codes_for_coders#Multiplication
        :param num:
        :return:
        """
        return GaloisField.get_exponents_table()[num]

    @staticmethod
    def get_log(num: int) -> int:
        """
        There are φ(255) = 192 primitive elements in GF(256), where φ is Euler's totient function.
        https://dev.to/maxart2501/let-s-develop-a-qr-code-generator-part-iii-error-correction-1kbm
        https://en.wikiversity.org/wiki/Reed%E2%80%93Solomon_codes_for_coders#Multiplication
        :param num:
        :return:
        """
        return GaloisField.get_log_table()[num]


def test_get_numbers():
    assert GaloisField.get_exp(3) == 8
    assert GaloisField.get_exp(8) == 29
    assert GaloisField.get_exp(9) == 58
    assert GaloisField.get_exp(10) == 116
    assert GaloisField.get_exp(11) == 232
    assert GaloisField.get_exp(12) == 205


def test_multiply_gf():
    assert GaloisField.multiply(76, 43) == 251


class GeneratorPolynomial:
    def __init__(self, degree: int):
        if degree not in GENERATOR_POLYNOMIALS:
            raise ValueError(f"No generator polynomial available for degree {degree}")
        self.polynomial = GENERATOR_POLYNOMIALS[degree]

    @staticmethod
    def create(degree: int) -> List[int]:
        return GENERATOR_POLYNOMIALS[degree]

    def __truediv__(self, message: List[int]) -> List[int]:
        return self.divide(message)

    def divide(self, message: List[int]) -> List[int]:
        """
        Divides the generator polynomial by the message polynomial
        in Galois Field arithmetic to get the remainder, which is
        the error correction code.

        :param message: The message polynomial coefficients
        :return: The remainder polynomial coefficients (error correction code)
        """
        steps = len(message)
        for step in range(steps):
            gen_polys = copy(self.polynomial)
            lead_term_log = GaloisField.get_log(message[0])

            # add the exponents and the alphas together. if > 255, then modulo 255
            for i in range(len(gen_polys)):
                gen_polys[i] += lead_term_log
                if gen_polys[i] >= 255:
                    gen_polys[i] %= 255

            # convert all the generator polynomials into their exponent form
            for i in range(len(gen_polys)):
                gen_polys[i] = GaloisField.get_exp(gen_polys[i])

            # extend message polynomial to the correct error correction code length if req.
            if len(message) < len(gen_polys):
                message.extend([0] * (len(gen_polys) - len(message)))

            # xor the ith generator polynomial and message polynomial values
            for i in range(len(message)):
                if i < len(gen_polys):
                    message[i] ^= gen_polys[i]
                else:
                    message[i] ^= 0

            # trim the leading 0
            message = message[1:]

        return message


def test_generator_polynomial():
    expected = [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]
    assert GeneratorPolynomial.create(10) == expected

    expected = [0, 87, 229, 146, 149, 238, 102, 21]
    assert GeneratorPolynomial.create(7) == expected


def test_divide_generator_with_message():
    expected = [196, 35, 39, 119, 235, 215, 231, 226, 93, 23]
    data = "0010000001011011000010110111100011010001011100101101110001001101" \
           "0100001101000000111011000001000111101100000100011110110000010001"
    ans = GeneratorPolynomial(10) / AlphanumericEncoder.get_8bit_binary_numbers(data)
    assert ans == expected

    ans = GeneratorPolynomial(10).divide(AlphanumericEncoder.get_8bit_binary_numbers(data))
    assert ans == expected
