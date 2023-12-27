from enum import Enum
from typing import List

ALPHANUMERIC_CHARS: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$%*+-.,/: "


# codewords. There are four parts to the encoded data: the mode indicator, the character count indicator, the encoded
# payload, and extra padding.

class ModeInidicators(Enum):
    NUMERIC: str = "0001"
    ALPHANUMERIC: str = "0010"
    BYTE: str = "0100"
    KANJI: str = "1000"


# HELLO WORLD is 11 characters long, the QR code is Version 2, and we are using alphanumeric encoding mode.
# Therefore, the character count indicator is the value 11 encoded using 9 bits, or 000001011.
class ModeIndicatorSize(Enum):
    NUMERIC = 10
    ALPHANUMERIC = 9


class InvalidAlphanumericCharacter(Exception):
    """Character is not valid

    Attributes:
        char -- `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$%*+-.,/: `
    """
    pass


CAPACITY_TABLE = {
    1: {"Numeric": 34, "Alphanumeric": 14},
    2: {"Numeric": 63, "Alphanumeric": 26},
    3: {"Numeric": 101, "Alphanumeric": 42},
    4: {"Numeric": 149, "Alphanumeric": 62},
    5: {"Numeric": 202, "Alphanumeric": 84},
    6: {"Numeric": 255, "Alphanumeric": 106},
    7: {"Numeric": 293, "Alphanumeric": 122},
    8: {"Numeric": 365, "Alphanumeric": 152},
    9: {"Numeric": 432, "Alphanumeric": 180},
    10: {"Numeric": 513, "Alphanumeric": 213},
    11: {"Numeric": 604, "Alphanumeric": 251},
    12: {"Numeric": 691, "Alphanumeric": 287},
    13: {"Numeric": 796, "Alphanumeric": 331},
    14: {"Numeric": 871, "Alphanumeric": 362},
    15: {"Numeric": 991, "Alphanumeric": 412},
    16: {"Numeric": 1082, "Alphanumeric": 450},
    17: {"Numeric": 1212, "Alphanumeric": 504},
    18: {"Numeric": 1346, "Alphanumeric": 560},
    19: {"Numeric": 1500, "Alphanumeric": 624},
    20: {"Numeric": 1600, "Alphanumeric": 666},
    21: {"Numeric": 1708, "Alphanumeric": 711},
    22: {"Numeric": 1872, "Alphanumeric": 779},
    23: {"Numeric": 2059, "Alphanumeric": 857},
    24: {"Numeric": 2188, "Alphanumeric": 911},
    25: {"Numeric": 2395, "Alphanumeric": 997},
    26: {"Numeric": 2544, "Alphanumeric": 1059},
    27: {"Numeric": 2701, "Alphanumeric": 1125},
    28: {"Numeric": 2857, "Alphanumeric": 1190},
    29: {"Numeric": 3035, "Alphanumeric": 1264},
    30: {"Numeric": 3289, "Alphanumeric": 1370},
    31: {"Numeric": 3486, "Alphanumeric": 1452},
    32: {"Numeric": 3693, "Alphanumeric": 1538},
    33: {"Numeric": 3909, "Alphanumeric": 1628},
    34: {"Numeric": 4134, "Alphanumeric": 1722},
    35: {"Numeric": 4343, "Alphanumeric": 1809},
    36: {"Numeric": 4588, "Alphanumeric": 1911},
    37: {"Numeric": 4775, "Alphanumeric": 1989},
    38: {"Numeric": 5039, "Alphanumeric": 2099},
    39: {"Numeric": 5313, "Alphanumeric": 2213},
    40: {"Numeric": 5596, "Alphanumeric": 2331}
}


def choose_qr_version(char_count, char_type):
    """
    Choose the appropriate QR code version for the given character count and type.

    :param char_count: Number of characters in the QR code.
    :param char_type: Type of characters ('Numeric' or 'Alphanumeric').
    :return: The smallest version number that can accommodate the character count, or None if not possible.
    """

    if char_count < 0:
        return None

    for version, capacities in CAPACITY_TABLE.items():
        if capacities[char_type] >= char_count:
            return version
    return None


class AlphanumericPair:
    @staticmethod
    def get_char_value(ch: str) -> int:
        """
        Converts a character into it's numerical form to be used for the encoding.
        https://zavier-henry.medium.com/an-introductory-walkthrough-for-encoding-qr-codes-5a33e1e882b5

        :param ch: Character to be encoded
        :return: Numerical representation between 0-44. -1 means character is invalid
        """
        if ch == "":
            return -1

        if ord('0') <= ord(ch) <= ord('9'):
            return int(ch)
        elif ord('A') <= ord(ch) <= ord('Z'):
            return ord(ch) - ord('A') + 10

        if ch == ' ':
            return 36
        if ch == '$':
            return 37
        if ch == '%':
            return 38
        if ch == '*':
            return 39
        if ch == '+':
            return 40
        if ch == '-':
            return 41
        if ch == '.':
            return 42
        if ch == '/':
            return 43
        if ch == ':':
            return 44

        return -1

    def __init__(self, first: str, second: str):
        self._first = first
        self._second = second

    def _first_value(self) -> int:
        return self.get_char_value(self._first)

    def _second_value(self) -> int:
        return self.get_char_value(self._second)

    def encode(self) -> str:
        value = self.get_pair_value()
        bin_text = "{0:b}".format(value)
        width = 6 if self._second_value() == -1 else 11

        return bin_text.rjust(width, "0")

    def get_pair_value(self) -> int:
        if self._second_value() == -1:
            value = self._first_value()
        else:
            value = (45 * self._first_value()) + self._second_value()
        return value


class AlphanumericEncoder:

    @classmethod
    def encode(cls, text: str) -> str:
        # set mode indicator and character length
        encoded_string = ModeInidicators.ALPHANUMERIC.value
        encoded_string += cls.get_character_count_indicator(text)

        # encode each set of pairs and join into a string
        encs = cls._encode_pairs(text)
        encoded_string += "".join(encs)

        # terminator zeros (up to 4 zeros if padding is required)
        min_length = 128
        min_length_padding = cls.pad_to_minimum_length(encoded_string, min_length)

        # pad zeros until current string len is a multiple of 8
        modulus_padding = cls.pad_to_modulus_eight(encoded_string)
        encoded_string += min_length_padding + modulus_padding

        # pad final alternating bytes of 0xEC and 0x11 to the end of encoded string
        encoded_string = cls.pad_remaining_bytes(encoded_string, min_length)

        return encoded_string

    @staticmethod
    def _encode_pairs(text) -> List[str]:
        encs = []
        for i in range(0, len(text), 2):
            if i + 1 < len(text):
                pair = AlphanumericPair(text[i], text[i + 1])
            else:
                pair = AlphanumericPair(text[i], "")

            encs.append(pair.encode())
        return encs

    @staticmethod
    def get_character_count_indicator(text: str):
        return "{0:b}".format(len(text)).rjust(9, "0")

    @staticmethod
    def pad_to_minimum_length(encoded_string: str, min_length: int) -> str:
        if len(encoded_string) < min_length:
            return "0" * min(min_length - len(encoded_string), 4)
        return ""

    @staticmethod
    def pad_to_modulus_eight(encoded_string: str) -> str:
        remaining_slots_to_modulus_eight = len(encoded_string) % 8
        return "0" * remaining_slots_to_modulus_eight

    @staticmethod
    def pad_remaining_bytes(encoded_string: str, min_length: int) -> str:
        """
        Alternate between adding 0xEC (11101100) and 0x11 (00010001) to the end of the encoded data until it reaches
        the required length.
        """
        remaining_zero_slots = ((min_length - len(encoded_string)) // 8)
        for r in range(remaining_zero_slots):
            encoded_string += "11101100" if r % 2 == 0 else "00010001"
        return encoded_string

    @staticmethod
    def get_8bit_binary_numbers(encoded_string: str) -> List[int]:
        nums: List[int] = []
        for i in range(0, len(encoded_string), 8):
            nums.append(int(encoded_string[i:i + 8], 2))
        return nums

    @staticmethod
    def get_8bit_binary_numbers_from_list(numbers: List[int]) -> List[str]:
        res: List[str] = []
        for i in range(0, len(numbers)):
            res.append("{0:b}".format(numbers[i]).rjust(8, "0"))
        return res
