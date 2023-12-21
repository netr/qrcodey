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


class InvalidVersionNumber(Exception):
    """Version number must be between 1 and 40

    Attributes:
        version -- version number given
    """
    pass


def get_module_size_from_version(version: int) -> int:
    """
    There are 40 versions of QR codes (from Version 1 (21 × 21 modules) to Version 40 (177 × 177 modules)).
    Each version has a different module configuration for storing different amounts of data.
    Each increment in version number increases the number of modules by 4 per side.
    More: https://tritonstore.com.au/qr-code-size/
    :param version: Version number between 1-40
    :return: Number of modules to be represented by a nxn grid
    """
    if version <= 0 or version > 40:
        raise InvalidVersionNumber(version)

    return 4 * (version - 1) + 21


class InvalidAlphanumericCharacter(Exception):
    """Character is not valid

    Attributes:
        char -- `0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$%*+-.,/: `
    """
    pass


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
