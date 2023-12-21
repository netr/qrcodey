from copy import copy
from typing import List

from galois import GaloisField

GENERATOR_POLYNOMIALS = {
    7: [0, 87, 229, 146, 149, 238, 102, 21],
    10: [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45],
    13: [0, 74, 152, 176, 100, 86, 100, 106, 104, 130, 218, 206, 140, 78],
    15: [0, 8, 183, 61, 91, 202, 37, 51, 58, 58, 237, 140, 124, 5, 99, 105],
    16: [0, 120, 104, 107, 109, 102, 161, 76, 3, 91, 191, 147, 169, 182, 194,
         225, 120],
    17: [0, 43, 139, 206, 78, 43, 239, 123, 206, 214, 147, 24, 99, 150, 39,
         243, 163, 136],
    18: [0, 215, 234, 158, 94, 184, 97, 118, 170, 79, 187, 152, 148, 252, 179,
         5, 98, 96, 153],
    20: [0, 17, 60, 79, 50, 61, 163, 26, 187, 202, 180, 221, 225, 83, 239, 156,
         164, 212, 212, 188, 190],
    22: [0, 210, 171, 247, 242, 93, 230, 14, 109, 221, 53, 200, 74, 8, 172, 98,
         80, 219, 134, 160, 105, 165, 231],
    24: [0, 229, 121, 135, 48, 211, 117, 251, 126, 159, 180, 169, 152, 192, 226,
         228, 218, 111, 0, 117, 232, 87, 96, 227, 21],
    26: [0, 173, 125, 158, 2, 103, 182, 118, 17, 145, 201, 111, 28, 165, 53, 161,
         21, 245, 142, 13, 102, 48, 227, 153, 145, 218, 70],
    28: [0, 168, 223, 200, 104, 224, 234, 108, 180, 110, 190, 195, 147, 205, 27,
         232, 201, 21, 43, 245, 87, 42, 195, 212, 119, 242, 37, 9, 123],
    30: [0, 41, 173, 145, 152, 216, 31, 179, 182, 50, 48, 110, 86, 239, 96, 222,
         125, 42, 173, 226, 193, 224, 130, 156, 37, 251, 216, 238, 40, 192,
         180]
}


class GeneratorPolynomial:
    def __init__(self, degree: int):
        if degree not in GENERATOR_POLYNOMIALS:
            raise ValueError(f"No generator polynomial available for degree {degree}")
        self.polynomial = GENERATOR_POLYNOMIALS[degree]

    def __eq__(self, other: List[int] | 'GeneratorPolynomial'):
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
