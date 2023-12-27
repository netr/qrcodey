from enum import Enum


class Mode(Enum):
    NUMERIC: str = "Numeric"
    ALPHANUMERIC: str = "Alphanumeric"
    BYTE: str = "Byte"
    KANJI: str = "Kanji"


ALIGNMENT_PATTERN_LOCATIONS = {
    1: [],
    2: [6, 18],  # version: [center, module row and column]
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98, 122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170]
}

VERSION_TABLE = {
    7: '000111110010010100',
    8: '001000010110111100',
    9: '001001101010011001',
    10: '001010010011010011',
    11: '001011101111110110',
    12: '001100011101100010',
    13: '001101100001000111',
    14: '001110011000001101',
    15: '001111100100101000',
    16: '010000101101111000',
    17: '010001010001011101',
    18: '010010101000010111',
    19: '010011010100110010',
    20: '010100100110100110',
    21: '010101011010000011',
    22: '010110100011001001',
    23: '010111011111101100',
    24: '011000111011000100',
    25: '011001000111100001',
    26: '011010111110101011',
    27: '011011000010001110',
    28: '011100110000011010',
    29: '011101001100111111',
    30: '011110110101110101',
    31: '011111001001010000',
    32: '100000100111010101',
    33: '100001011011110000',
    34: '100010100010111010',
    35: '100011011110011111',
    36: '100100101100001011',
    37: '100101010000101110',
    38: '100110101001100100',
    39: '100111010101000001',
    40: '101000110001101001',
}

FORMAT_STRINGS = {
    'L': {
        0: '111011111000100',
        1: '111001011110011',
        2: '111110110101010',
        3: '111100010011101',
        4: '110011000101111',
        5: '110001100011000',
        6: '110110001000001',
        7: '110100101110110',
    },
    'M': {
        0: '101010000010010',
        1: '101000100100101',
        2: '101111001111100',
        3: '101101101001011',
        4: '100010111111001',
        5: '100000011001110',
        6: '100111110010111',
        7: '100101010100000',
    },
    'Q': {
        0: '011010101011111',
        1: '011000001101000',
        2: '011111100110001',
        3: '011101000000110',
        4: '010010010110100',
        5: '010000110000011',
        6: '010111011011010',
        7: '010101111101101',
    },
    'H': {
        0: '001011010001001',
        1: '001001110111110',
        2: '001110011100111',
        3: '001100111010000',
        4: '000011101100010',
        5: '000001001010101',
        6: '000110100001100',
        7: '000100000111011',
    }
}

CAPACITY_TABLE = {
    1: {Mode.NUMERIC.value: 34, Mode.ALPHANUMERIC.value: 14},
    2: {Mode.NUMERIC.value: 63, Mode.ALPHANUMERIC.value: 26},
    3: {Mode.NUMERIC.value: 101, Mode.ALPHANUMERIC.value: 42},
    4: {Mode.NUMERIC.value: 149, Mode.ALPHANUMERIC.value: 62},
    5: {Mode.NUMERIC.value: 202, Mode.ALPHANUMERIC.value: 84},
    6: {Mode.NUMERIC.value: 255, Mode.ALPHANUMERIC.value: 106},
    7: {Mode.NUMERIC.value: 293, Mode.ALPHANUMERIC.value: 122},
    8: {Mode.NUMERIC.value: 365, Mode.ALPHANUMERIC.value: 152},
    9: {Mode.NUMERIC.value: 432, Mode.ALPHANUMERIC.value: 180},
    10: {Mode.NUMERIC.value: 513, Mode.ALPHANUMERIC.value: 213},
    11: {Mode.NUMERIC.value: 604, Mode.ALPHANUMERIC.value: 251},
    12: {Mode.NUMERIC.value: 691, Mode.ALPHANUMERIC.value: 287},
    13: {Mode.NUMERIC.value: 796, Mode.ALPHANUMERIC.value: 331},
    14: {Mode.NUMERIC.value: 871, Mode.ALPHANUMERIC.value: 362},
    15: {Mode.NUMERIC.value: 991, Mode.ALPHANUMERIC.value: 412},
    16: {Mode.NUMERIC.value: 1082, Mode.ALPHANUMERIC.value: 450},
    17: {Mode.NUMERIC.value: 1212, Mode.ALPHANUMERIC.value: 504},
    18: {Mode.NUMERIC.value: 1346, Mode.ALPHANUMERIC.value: 560},
    19: {Mode.NUMERIC.value: 1500, Mode.ALPHANUMERIC.value: 624},
    20: {Mode.NUMERIC.value: 1600, Mode.ALPHANUMERIC.value: 666},
    21: {Mode.NUMERIC.value: 1708, Mode.ALPHANUMERIC.value: 711},
    22: {Mode.NUMERIC.value: 1872, Mode.ALPHANUMERIC.value: 779},
    23: {Mode.NUMERIC.value: 2059, Mode.ALPHANUMERIC.value: 857},
    24: {Mode.NUMERIC.value: 2188, Mode.ALPHANUMERIC.value: 911},
    25: {Mode.NUMERIC.value: 2395, Mode.ALPHANUMERIC.value: 997},
    26: {Mode.NUMERIC.value: 2544, Mode.ALPHANUMERIC.value: 1059},
    27: {Mode.NUMERIC.value: 2701, Mode.ALPHANUMERIC.value: 1125},
    28: {Mode.NUMERIC.value: 2857, Mode.ALPHANUMERIC.value: 1190},
    29: {Mode.NUMERIC.value: 3035, Mode.ALPHANUMERIC.value: 1264},
    30: {Mode.NUMERIC.value: 3289, Mode.ALPHANUMERIC.value: 1370},
    31: {Mode.NUMERIC.value: 3486, Mode.ALPHANUMERIC.value: 1452},
    32: {Mode.NUMERIC.value: 3693, Mode.ALPHANUMERIC.value: 1538},
    33: {Mode.NUMERIC.value: 3909, Mode.ALPHANUMERIC.value: 1628},
    34: {Mode.NUMERIC.value: 4134, Mode.ALPHANUMERIC.value: 1722},
    35: {Mode.NUMERIC.value: 4343, Mode.ALPHANUMERIC.value: 1809},
    36: {Mode.NUMERIC.value: 4588, Mode.ALPHANUMERIC.value: 1911},
    37: {Mode.NUMERIC.value: 4775, Mode.ALPHANUMERIC.value: 1989},
    38: {Mode.NUMERIC.value: 5039, Mode.ALPHANUMERIC.value: 2099},
    39: {Mode.NUMERIC.value: 5313, Mode.ALPHANUMERIC.value: 2213},
    40: {Mode.NUMERIC.value: 5596, Mode.ALPHANUMERIC.value: 2331}
}

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

ECC_BLOCKS = {
    1: {
        "L": (19, 7, 1, 19, 0, 0),
        "M": (16, 10, 1, 16, 0, 0),
        "Q": (13, 13, 1, 13, 0, 0),
        "H": (9, 17, 1, 9, 0, 0)
    },
    2: {
        "L": (34, 10, 1, 34, 0, 0),
        "M": (28, 16, 1, 28, 0, 0),
        "Q": (22, 22, 1, 22, 0, 0),
        "H": (16, 28, 1, 16, 0, 0)
    },
    3: {
        "L": (55, 15, 1, 55, 0, 0),
        "M": (44, 26, 1, 44, 0, 0),
        "Q": (34, 18, 2, 17, 0, 0),
        "H": (26, 22, 2, 13, 0, 0)
    },
    4: {
        "L": (80, 20, 1, 80, 0, 0),
        "M": (64, 18, 2, 32, 0, 0),
        "Q": (48, 26, 2, 24, 0, 0),
        "H": (36, 16, 4, 9, 0, 0)
    },
    5: {
        "L": (108, 26, 1, 108, 0, 0),
        "M": (86, 24, 2, 43, 0, 0),
        "Q": (62, 18, 2, 15, 2, 16),
        "H": (46, 22, 2, 11, 2, 12)
    },
    6: {
        "L": (136, 18, 2, 68, 0, 0),
        "M": (108, 16, 4, 27, 0, 0),
        "Q": (76, 24, 4, 19, 0, 0),
        "H": (60, 28, 4, 15, 0, 0)
    },
    7: {
        "L": (156, 20, 2, 78, 0, 0),
        "M": (124, 18, 4, 31, 0, 0),
        "Q": (88, 18, 2, 14, 4, 15),
        "H": (66, 26, 4, 13, 1, 14)
    },
    8: {
        "L": (194, 24, 2, 97, 0, 0),
        "M": (154, 22, 2, 38, 2, 39),
        "Q": (110, 22, 4, 18, 2, 19),
        "H": (86, 26, 4, 14, 2, 15)
    },
    9: {
        "L": (232, 30, 2, 116, 0, 0),
        "M": (182, 22, 3, 36, 2, 37),
        "Q": (132, 20, 4, 16, 4, 17),
        "H": (100, 24, 4, 12, 4, 13)
    },
    10: {
        "L": (274, 18, 2, 68, 2, 69),
        "M": (216, 26, 4, 43, 1, 44),
        "Q": (154, 24, 6, 19, 2, 20),
        "H": (122, 28, 6, 15, 2, 16)
    },
    11: {
        "L": (324, 20, 4, 81, 0, 0),
        "M": (254, 30, 1, 50, 4, 51),
        "Q": (180, 28, 4, 22, 4, 23),
        "H": (140, 24, 3, 12, 8, 13)
    },
    12: {
        "L": (370, 24, 2, 92, 2, 93),
        "M": (290, 22, 6, 36, 2, 37),
        "Q": (206, 26, 4, 20, 6, 21),
        "H": (158, 28, 7, 14, 4, 15)
    },
    13: {
        "L": (428, 26, 4, 107, 0, 0),
        "M": (334, 22, 8, 37, 1, 38),
        "Q": (244, 24, 8, 20, 4, 21),
        "H": (180, 22, 12, 11, 4, 12)
    },
    14: {
        "L": (461, 30, 3, 115, 1, 116),
        "M": (365, 24, 4, 40, 5, 41),
        "Q": (261, 20, 11, 16, 5, 17),
        "H": (197, 24, 11, 12, 5, 13)
    },
    15: {
        "L": (523, 22, 5, 87, 1, 88),
        "M": (415, 24, 5, 41, 5, 42),
        "Q": (295, 30, 5, 24, 7, 25),
        "H": (223, 24, 11, 12, 7, 13)
    },
    16: {
        "L": (589, 24, 5, 98, 1, 99),
        "M": (453, 28, 7, 45, 3, 46),
        "Q": (325, 24, 15, 19, 2, 20),
        "H": (253, 30, 3, 15, 13, 16)
    },
    17: {
        "L": (647, 28, 1, 107, 5, 108),
        "M": (507, 28, 10, 46, 1, 47),
        "Q": (367, 28, 1, 22, 15, 23),
        "H": (283, 28, 2, 14, 17, 15)
    },
    18: {
        "L": (721, 30, 5, 120, 1, 121),
        "M": (563, 26, 9, 43, 4, 44),
        "Q": (397, 28, 17, 22, 1, 23),
        "H": (313, 28, 2, 14, 19, 15)
    },
    19: {
        "L": (795, 28, 3, 113, 4, 114),
        "M": (627, 26, 3, 44, 11, 45),
        "Q": (445, 26, 17, 21, 4, 22),
        "H": (341, 26, 9, 13, 16, 14)
    },
    20: {
        "L": (861, 28, 3, 107, 5, 108),
        "M": (669, 26, 3, 41, 13, 42),
        "Q": (485, 30, 15, 24, 5, 25),
        "H": (385, 28, 15, 15, 10, 16)
    },
    21: {
        "L": (932, 28, 4, 116, 4, 117),
        "M": (714, 26, 17, 42, 0, 0),
        "Q": (512, 28, 17, 22, 6, 23),
        "H": (406, 30, 19, 16, 6, 17)
    },
    22: {
        "L": (1006, 28, 2, 111, 7, 112),
        "M": (782, 28, 17, 46, 0, 0),
        "Q": (568, 30, 7, 24, 16, 25),
        "H": (442, 24, 34, 13, 0, 0)
    },
    23: {
        "L": (1094, 30, 4, 121, 5, 122),
        "M": (860, 28, 4, 47, 14, 48),
        "Q": (614, 30, 11, 24, 14, 25),
        "H": (464, 30, 16, 15, 14, 16)
    },
    24: {
        "L": (1174, 30, 6, 117, 4, 118),
        "M": (914, 28, 6, 45, 14, 46),
        "Q": (664, 30, 11, 24, 16, 25),
        "H": (514, 30, 30, 16, 2, 17)
    },
    25: {
        "L": (1276, 26, 8, 106, 4, 107),
        "M": (1000, 28, 8, 47, 13, 48),
        "Q": (718, 30, 7, 24, 22, 25),
        "H": (538, 30, 22, 15, 13, 16)
    },
    26: {
        "L": (1370, 28, 10, 114, 2, 115),
        "M": (1062, 28, 19, 46, 4, 47),
        "Q": (754, 28, 28, 22, 6, 23),
        "H": (596, 30, 33, 16, 4, 17)
    },
    27: {
        "L": (1468, 30, 8, 122, 4, 123),
        "M": (1128, 28, 22, 45, 3, 46),
        "Q": (808, 30, 8, 23, 26, 24),
        "H": (628, 30, 12, 15, 28, 16)
    },
    28: {
        "L": (1531, 30, 3, 117, 10, 118),
        "M": (1193, 28, 3, 45, 23, 46),
        "Q": (871, 30, 4, 24, 31, 25),
        "H": (661, 30, 11, 15, 31, 16)
    },
    29: {
        "L": (1631, 30, 7, 116, 7, 117),
        "M": (1267, 28, 21, 45, 7, 46),
        "Q": (911, 30, 1, 23, 37, 24),
        "H": (701, 30, 19, 15, 26, 16)
    },
    30: {
        "L": (1735, 30, 5, 115, 10, 116),
        "M": (1373, 28, 19, 47, 10, 48),
        "Q": (985, 30, 15, 24, 25, 25),
        "H": (745, 30, 23, 15, 25, 16)
    },
    31: {
        "L": (1843, 30, 13, 115, 3, 116),
        "M": (1455, 28, 2, 46, 29, 47),
        "Q": (1033, 30, 42, 24, 1, 25),
        "H": (793, 30, 23, 15, 28, 16)
    },
    32: {
        "L": (1955, 30, 17, 115, 0, 0),
        "M": (1541, 28, 10, 46, 23, 47),
        "Q": (1115, 30, 10, 24, 35, 25),
        "H": (845, 30, 19, 15, 35, 16)
    },
    33: {
        "L": (2071, 30, 17, 115, 1, 116),
        "M": (1631, 28, 14, 46, 21, 47),
        "Q": (1171, 30, 29, 24, 19, 25),
        "H": (901, 30, 11, 15, 46, 16)
    },
    34: {
        "L": (2191, 30, 13, 115, 6, 116),
        "M": (1725, 28, 14, 46, 23, 47),
        "Q": (1231, 30, 44, 24, 7, 25),
        "H": (961, 30, 59, 16, 1, 17)
    },
    35: {
        "L": (2306, 30, 12, 121, 7, 122),
        "M": (1812, 28, 12, 47, 26, 48),
        "Q": (1286, 30, 39, 24, 14, 25),
        "H": (986, 30, 22, 15, 41, 16)
    },
    36: {
        "L": (2434, 30, 6, 121, 14, 122),
        "M": (1914, 28, 6, 47, 34, 48),
        "Q": (1354, 30, 46, 24, 10, 25),
        "H": (1054, 30, 2, 15, 64, 16)
    },
    37: {
        "L": (2566, 30, 17, 122, 4, 123),
        "M": (1992, 28, 29, 46, 14, 47),
        "Q": (1426, 30, 49, 24, 10, 25),
        "H": (1096, 30, 24, 15, 46, 16)
    },
    38: {
        "L": (2702, 30, 4, 122, 18, 123),
        "M": (2102, 28, 13, 46, 32, 47),
        "Q": (1502, 30, 48, 24, 14, 25),
        "H": (1142, 30, 42, 15, 32, 16)
    },
    39: {
        "L": (2812, 30, 20, 117, 4, 118),
        "M": (2216, 28, 40, 47, 7, 48),
        "Q": (1582, 30, 43, 24, 22, 25),
        "H": (1222, 30, 10, 15, 67, 16)
    },
    40: {
        "L": (2956, 30, 19, 118, 6, 119),
        "M": (2334, 28, 18, 47, 31, 48),
        "Q": (1666, 30, 34, 24, 34, 25),
        "H": (1276, 30, 20, 15, 61, 16),
    }
}


class InvalidErrorCorrectionCode(Exception):
    pass


class InvalidErrorCorrectionVersion(Exception):
    pass


def get_required_length_of_ecc_block(version: int, ecc: str) -> int:
    block = ECC_BLOCKS.get(version)
    if block is None:
        raise InvalidErrorCorrectionVersion(version)

    ecc_block = block.get(ecc)
    if ecc_block is None:
        raise InvalidErrorCorrectionCode(ecc)

    return ECC_BLOCKS[version][ecc][0] * 8