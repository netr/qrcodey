from functools import cache
from typing import Dict


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
        return GaloisField.get_exponents_table()[num]

    @staticmethod
    def get_log(num: int) -> int:
        try:
            return GaloisField.get_log_table()[num]
        except KeyError:
            return 0
