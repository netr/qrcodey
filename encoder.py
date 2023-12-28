from enum import Enum
from typing import List

from const import get_required_length_of_ecc_block, Mode
from util import choose_qr_version

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

        if ord("0") <= ord(ch) <= ord("9"):
            return int(ch)
        elif ord("A") <= ord(ch) <= ord("Z"):
            return ord(ch) - ord("A") + 10

        if ch == " ":
            return 36
        if ch == "$":
            return 37
        if ch == "%":
            return 38
        if ch == "*":
            return 39
        if ch == "+":
            return 40
        if ch == "-":
            return 41
        if ch == ".":
            return 42
        if ch == "/":
            return 43
        if ch == ":":
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


class DataEncoder:
    @classmethod
    def encode(cls, text: str, version: int, ecc: str) -> str:
        # infer the encoding mode and get the respective indicator string and bit chunks
        encoding_mode = cls._get_encoding_mode(text)
        encoding_chunks = []
        encoded_string = ""
        match encoding_mode:
            case Mode.NUMERIC:
                encoded_string = ModeInidicators.NUMERIC.value
                encoding_chunks = cls._encode_numeric(text)
            case Mode.ALPHANUMERIC:
                encoded_string = ModeInidicators.ALPHANUMERIC.value
                encoding_chunks = cls._encode_alphanumeric_pairs(text)
            case Mode.BYTE:
                encoded_string = ModeInidicators.BYTE.value
                encoding_chunks = cls._encode_bytes(text)

        # set mode indicator and character length
        encoded_string += cls.get_character_count_indicator(text, encoding_mode)
        encoded_string += "".join(encoding_chunks)

        # terminator zeros (up to 4 zeros if padding is required)
        terminator_zeros = cls.pad_terminator_zeros(encoded_string)
        encoded_string += terminator_zeros

        # pad zeros until current string len is a multiple of 8
        modulus_padding = cls.pad_to_modulus_eight(encoded_string)
        encoded_string += modulus_padding

        # https://www.thonky.com/qr-code-tutorial/error-correction-table
        # Total Number of Data Codewords for this Version and EC Level (Multiplied by 8 bytes for binary length)
        required_length = get_required_length_of_ecc_block(version, ecc)

        # pad final alternating bytes of 0xEC and 0x11 to the end of encoded string
        encoded_string = cls.pad_remaining_bytes(encoded_string, required_length)

        return encoded_string

    @staticmethod
    def _get_encoding_mode(text: str) -> Mode:
        if text.isdigit():
            return Mode.NUMERIC

        for ch in text:
            if ch not in ALPHANUMERIC_CHARS:
                return Mode.BYTE

        return Mode.ALPHANUMERIC

    @staticmethod
    def _encode_alphanumeric_pairs(text: str) -> List[str]:
        encs = []
        for i in range(0, len(text), 2):
            if i + 1 < len(text):
                pair = AlphanumericPair(text[i], text[i + 1])
            else:
                pair = AlphanumericPair(text[i], "")

            encs.append(pair.encode())
        return encs

    @staticmethod
    def _encode_bytes(text: str) -> List[str]:
        """
        Convert the bytes into an 8-bit binary string.
        Pad on the left with 0s if necessary to make each one 8-bits long.
        """
        return [format(ord(char), "08b") for char in text]

    @staticmethod
    def _encode_numeric(text: str) -> List[str]:
        """
        Convert the bytes into an 8-bit binary string.
        Pad on the left with 0s if necessary to make each one 8-bits long.
        """
        enc = []
        splits = [text[i : i + 3] for i in range(0, len(text), 3)]
        for s in splits:
            fmt = ""
            # If the final group consists of only two digits, you should convert it to 7 binary bits, and if the
            # final group consists of only one digit, you should convert it to 4 binary bits.

            if len(s) == 3:
                fmt = format(int(s), "010b")
            elif len(s) == 2:
                fmt = format(int(s), "07b")
            elif len(s) == 1:
                fmt = format(int(s), "04b")

            # If a group starts with a zero, it should be interpreted as a two-digit number and you should convert it
            # to 7 binary bits, and if there are two zeroes at the beginning of a group, it should be interpreted as
            # a one-digit number and you should convert it to 4 binary bits.

            if s[:1] == "00":
                fmt = format(int(s), "04b")
            elif s[0] == "0":
                fmt = format(int(s), "07b")

            enc.append(fmt)
        return enc

    @staticmethod
    def get_character_count_indicator(text: str, mode: Mode):
        version = choose_qr_version(len(text), mode.value)
        width = 0
        if 1 <= version <= 9:
            width = 9
        elif 10 <= version <= 26:
            width = 11
        elif 27 <= version:
            width = 13
        return "{0:b}".format(len(text)).rjust(width, "0")

    @staticmethod
    def pad_terminator_zeros(encoded_string: str) -> str:
        rem = len(encoded_string) % 8
        return "0" * min(rem, 4)

    @staticmethod
    def pad_to_modulus_eight(encoded_string: str) -> str:
        remaining_slots_to_modulus_eight = len(encoded_string) % 8
        if remaining_slots_to_modulus_eight > 0:
            # we need to invert the remainer to get amount of zeros required to fill
            remaining_slots_to_modulus_eight = 8 - remaining_slots_to_modulus_eight

        return "0" * remaining_slots_to_modulus_eight

    @staticmethod
    def pad_remaining_bytes(encoded_string: str, required_length: int) -> str:
        """
        Alternate between adding 0xEC (11101100) and 0x11 (00010001) to the end of the encoded data until it reaches
        the required length.
        """
        remaining_zero_slots = (required_length - len(encoded_string)) // 8
        for r in range(remaining_zero_slots):
            encoded_string += "11101100" if r % 2 == 0 else "00010001"
        return encoded_string

    @staticmethod
    def get_8bit_binary_numbers(encoded_string: str) -> List[int]:
        nums: List[int] = []
        for i in range(0, len(encoded_string), 8):
            nums.append(int(encoded_string[i : i + 8], 2))
        return nums

    @staticmethod
    def get_8bit_binary_numbers_from_list(numbers: List[int]) -> List[str]:
        res: List[str] = []
        for i in range(0, len(numbers)):
            res.append("{0:b}".format(numbers[i]).rjust(8, "0"))
        return res
