from functools import cache
from typing import Dict, List

from const import GENERATOR_POLYNOMIALS
from encoder import AlphanumericEncoder


class GaloisField:
    @staticmethod
    @cache
    def get_exponents_table() -> Dict[int, int]:
        value = 1
        exps: Dict[int, int] = {i: 0 for i in range(0, 255)}
        for exp in range(1, 256):
            value = ((value << 1) ^ 285) if value > 127 else value << 1
            exps[exp % 255] = value
        return exps

    @staticmethod
    @cache
    def get_log_table() -> Dict[int, int]:
        value = 1
        log: Dict[int, int] = {i: 0 for i in range(0, 255)}
        for exp in range(1, 256):
            value = ((value << 1) ^ 285) if value > 127 else value << 1
            log[value] = exp % 255
        return log

    @staticmethod
    def multiply(a: int, b: int) -> int:
        exps, log = GaloisField.get_exponents_table(), GaloisField.get_log_table()
        return exps[(log[a] + log[b])] if a and b else 0

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


class Polynomial:
    def __init__(self, coefficients: list[int]):
        self.coefficients = coefficients

    def __eq__(self, other: 'Polynomial'):
        return self.coefficients == other.coefficients

    def __getitem__(self, index):
        return self.coefficients[index]

    def __iter__(self):
        return iter(self.coefficients)

    def __len__(self):
        return len(self.coefficients)

    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        # Initialize the result coefficient array
        degrees = len(self.coefficients) + len(other.coefficients) - 1
        coeffs = [0] * degrees

        # Perform polynomial multiplication
        for i, cur_poly in enumerate(self.coefficients):
            for j, other_poly in enumerate(other.coefficients):
                coeffs[i + j] ^= GaloisField.multiply(cur_poly, other_poly)

        return Polynomial(coeffs)


def test_polynomial_multiplication():
    # Assuming Polynomial takes a list of coefficients from highest to lowest degree
    # and implements __eq__ for comparison

    # Basic Multiplication
    assert Polynomial([1, 1]) * Polynomial([1, 2]) == Polynomial([1, 3, 2])

    # Multiplication with Zero
    assert Polynomial([1, 0, 4, 4]) * Polynomial([0]) == Polynomial([0, 0, 0, 0])

    # Multiplication with One
    assert Polynomial([3, 2, 1]) * Polynomial([1]) == Polynomial([3, 2, 1])

    # Different Lengths
    # assert Polynomial([1, 1, 1, 0]) * (Polynomial([1, 1])) == Polynomial([1, 2, 2, 1, 0])

    # Coefficients > 255
    # You need to adjust the coefficients according to your Galois Field implementation
    # Example coefficients here are placeholders
    # assert Polynomial([300, 200]).multiply(Polynomial([2])) == Polynomial(
    #     [GaloisField.some_reduction(600), GaloisField.some_reduction(400)])

    # Complex Polynomials
    # assert Polynomial([1, 0, 1, 1]) * (Polynomial([1, 0, 1])) == Polynomial([1, 0, 2, 1, 1])


class GeneratorPolynomial:
    def __init__(self, degree: int):
        self.polynomial = self.create(degree)

    @staticmethod
    def create(degree: int) -> List[int]:
        return GENERATOR_POLYNOMIALS[degree]

    def __truediv__(self, other: List[int]) -> List[int]:
        for step in range(16):
            start = self.polynomial[:]
            lead_term = other[0]
            lead_term_log = GaloisField.get_log(lead_term)
            # print("step", step + 1, "lead_term", lead_term, "log", GaloisField.get_log(lead_term))
            for i in range(len(start)):
                start[i] += lead_term_log
                if start[i] >= 255:
                    start[i] %= 255

            # print("start", start)

            next = [0] * len(start)
            for i in range(len(start)):
                next[i] = GaloisField.get_exp(start[i])
            # print("next", next, "--->", len(other), len(next))
            if len(other) < len(next):
                other.extend([0] * (len(next) - len(other)))
            for i in range(len(other)):
                if i < len(next):
                    other[i] ^= next[i]
                else:
                    other[i] ^= 0
            #
            # print("other", other)
            other = other[1:]
            print("")

        return other


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
