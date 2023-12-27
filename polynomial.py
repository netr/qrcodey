from copy import copy
from typing import List

from const import GENERATOR_POLYNOMIALS
from galois import GaloisField


class GeneratorPolynomial:
    def __init__(self, degree: int):
        if degree not in GENERATOR_POLYNOMIALS:
            raise ValueError(f"No generator polynomial available for degree {degree}")
        self.polynomial = GENERATOR_POLYNOMIALS[degree]

    def __eq__(self, other: List[int] | "GeneratorPolynomial"):
        return other == self.polynomial

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
