from typing import Tuple, List
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

ALIGNMENT_PATTERN_LOCATIONS = {
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


class InvalidVersionNumber(Exception):
    """
    This class represents an exception that is raised when an invalid version number is encountered.

    """
    pass


class QrCode:
    """
    The QrCode class represents a QR code.

    Attributes:
        MAX_VERSION (int): The maximum version number of the QR code.
        MIN_VERSION (int): The minimum version number of the QR code.
        MODULES_INCREMENT (int): The number of modules to increment for each version.
        MIN_MODULES (int): The minimum number of modules for a QR code.
        FINDER_OFFSET (int): The offset value for calculating the finder pattern position.

    Methods:
        __init__(self, version: int): Initializes a new instance of the QrCode class.
        get_module_size(self) -> int: Calculates the number of modules based on the QR code version.
        add_patterns_and_separators(self): Adds the finder patterns and separators to the QR code.
        calculate_finder_position(self, is_bottom_left=False) -> tuple: Calculates the position of the finder patterns.
        add_finder_pattern(self, xoffset, yoffset): Adds the finder pattern to the QR code matrix.
        add_separators(self): Adds the separators to the QR code matrix.
        add_horiz_separators(self): Adds the horizontal separators to the QR code matrix.
        add_vertical_separators(self): Adds the vertical separators to the QR code matrix.
        calculate_top_right(self) -> list: Calculates the position of the top-right finder pattern.
        calculate_bottom_left(self) -> list: Calculates the position of the bottom-left finder pattern.
    """
    MAX_VERSION = 40  # REF 1
    MIN_VERSION = 1
    MODULES_INCREMENT = 4
    MIN_MODULES = 21
    FINDER_OFFSET = 7
    WHITE_MODULE = 2
    BLACK_MODULE = 0

    def __init__(self, version: int):
        self._version = version
        self._modules = self.get_module_size()
        self.matrix = [[1] * self._modules for _ in range(self._modules)]
        self.add_patterns_and_separators()

    def get_module_size(self) -> int:
        """
        There are 40 versions of QR codes (from Version 1 (21 × 21 modules) to Version 40 (177 × 177 modules)).
        Each version has a different module configuration for storing different amounts of data.
        Each increment in version number increases the number of modules by 4 per side.
        More: https://tritonstore.com.au/qr-code-size/
        :return: Number of modules to be represented by a nxn grid
        """
        if self._version < self.MIN_VERSION or self._version > self.MAX_VERSION:
            raise InvalidVersionNumber(self._version)

        return self.MODULES_INCREMENT * (self._version - 1) + self.MIN_MODULES  # REF 1

    def add_patterns_and_separators(self):
        top_right = self.calculate_finder_position()
        bottom_left = self.calculate_finder_position(is_bottom_left=True)

        self.add_finder_pattern(0, 0)
        self.add_finder_pattern(*top_right)  # Use tuple unpacking
        self.add_finder_pattern(*bottom_left)
        self.add_separators()

    def calculate_finder_position(self, is_bottom_left=False):
        mod_minus_offset = self._modules - self.FINDER_OFFSET  # REF 1
        return (0, mod_minus_offset) if is_bottom_left else (mod_minus_offset, 0)

    def add_finder_pattern(self, xoffset, yoffset):
        """
        The top-left finder pattern's top left corner is always placed at (0,0).
        The top-right finder pattern's top LEFT corner is always placed at ([(((V-1)*4)+21) - 7], 0)
        The bottom-left finder pattern's top LEFT corner is always placed at (0,[(((V-1)*4)+21) - 7])
        """
        for i in range(yoffset + 0, yoffset + self.FINDER_OFFSET):
            for j in range(xoffset + 0, xoffset + self.FINDER_OFFSET):
                self.matrix[i][j] = self.BLACK_MODULE

        for i in range(yoffset + 1, yoffset + (self.FINDER_OFFSET - 1)):
            for j in range(xoffset + 1, xoffset + (self.FINDER_OFFSET - 1)):
                self.matrix[i][j] = self.WHITE_MODULE

        for i in range(yoffset + 2, yoffset + (self.FINDER_OFFSET - 2)):
            for j in range(xoffset + 2, xoffset + (self.FINDER_OFFSET - 2)):
                self.matrix[i][j] = self.BLACK_MODULE

    def add_separators(self):
        self.add_horiz_separators()
        self.add_vertical_separators()

    def add_horiz_separators(self):
        for i in range(0, (self.FINDER_OFFSET + 1)):
            self.matrix[self.FINDER_OFFSET][i] = self.WHITE_MODULE
            self.matrix[self.FINDER_OFFSET][len(self.matrix[0]) - i - 1] = self.WHITE_MODULE
            self.matrix[len(self.matrix) - (self.FINDER_OFFSET + 1)][i] = self.WHITE_MODULE

    def add_vertical_separators(self):
        for i in range(0, (self.FINDER_OFFSET + 1)):
            self.matrix[i][self.FINDER_OFFSET] = self.WHITE_MODULE
            self.matrix[i][len(self.matrix[0]) - (self.FINDER_OFFSET + 1)] = self.WHITE_MODULE
            self.matrix[len(self.matrix[0]) - i - 1][self.FINDER_OFFSET] = self.WHITE_MODULE

    def calculate_top_right(self) -> [int, int]:
        return [(((self._version - 1) * self.MODULES_INCREMENT) + self.MIN_MODULES) - self.FINDER_OFFSET, 0]

    def calculate_bottom_left(self) -> [int, int]:
        return [0, (((self._version - 1) * self.MODULES_INCREMENT) + self.MIN_MODULES) - self.FINDER_OFFSET]

    def add_alignment_patterns(self):
        """
        Draw the alignment patterns across the entire QR Code. To avoid overlapping with finder patterns,
        the function `get_alignment_center_points` is used. It incorporates the `_validate_alignment_points` method
        internally to resolve this issue.

        https://www.thonky.com/qr-code-tutorial/module-placement-matrix#step-3-add-the-alignment-patterns
        """
        points = self.get_alignment_center_points()
        for x, y in points:
            self.matrix[x][y] = self.BLACK_MODULE
            # draw white in a 'circle' around the center
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                self.matrix[x + dx][y + dy] = self.WHITE_MODULE
            # draw the outer most, horizontal black rows
            for dx, dy in [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]:
                self.matrix[x + dx][y + dy] = self.BLACK_MODULE
            # draw the outer most, vertical black rows
            for dx, dy in [(-1, -2), (0, -2), (1, -2), (-1, 2), (0, 2), (1, 2)]:
                self.matrix[x + dx][y + dy] = self.BLACK_MODULE

    def add_reserve_modules(self):
        for i in range(0, 8):
            self.matrix[8][i] = self.BLACK_MODULE
            self.matrix[8][len(self.matrix[0]) - i - 1] = self.BLACK_MODULE

        for i in range(0, 9):
            self.matrix[i][8] = self.BLACK_MODULE

        for i in range(0, 7):
            self.matrix[len(self.matrix) - i - 1][8] = self.BLACK_MODULE

    def get_alignment_center_points(self) -> List[Tuple[int, int]]:
        """
        The locations at which the alignment patterns must be placed are defined in the `ALIGNMENT_PATTERN_LOCATIONS`
        dictionary. The numbers are to be used as BOTH row and column coordinates.

        For example, Version 2 has the numbers 6 and 18. This means that the CENTER MODULES of the alignment patterns
        are to be placed  at (6, 6), (6, 18), (18, 6) and (18, 18).

        :return: List of center alignment pixels as (x,y) cartesian points
        """
        locations = ALIGNMENT_PATTERN_LOCATIONS[self._version]

        points = []
        for i in range(len(locations)):
            for j in range(len(locations)):
                points.append((locations[i], locations[j]))

        return self._validate_alignment_points(points)

    def _validate_alignment_points(self, points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        The alignment patterns must be put into the matrix AFTER the finder patterns and separators have been placed,
        and the alignment patterns MUST NOT overlap the finder patterns or separators.

        :param points: List of all alignment points for specified version
        :return: List of valid center alignment pixels as (x,y) cartesian points
        """
        res = []
        for x, y in points:
            if x <= self.FINDER_OFFSET and y <= self.FINDER_OFFSET:  # top left
                continue
            if x <= self.FINDER_OFFSET and y >= (len(self.matrix[0]) - self.FINDER_OFFSET):  # top right
                continue
            if x >= (len(self.matrix) - self.FINDER_OFFSET) and y <= self.FINDER_OFFSET:  # bottom left
                continue
            res.append((x, y))

        return res

    def add_timing_patterns(self):
        """
        The timing patterns are two lines, one horizontal and one vertical, of alternating dark and light modules.
        The horizontal timing pattern is placed on the 6th row of the QR code between the separators. The vertical
        timing pattern is placed on the 6th column of the QR code between the separators. The timing patterns always
        start and end with a dark module.
        """
        # draw vertical timing pattern
        for r in range(self.FINDER_OFFSET + 1, len(self.matrix) - self.FINDER_OFFSET - 1):
            self.matrix[r][self.FINDER_OFFSET - 1] = self.BLACK_MODULE if r % 2 == 0 else self.WHITE_MODULE

        # draw horizontal timing pattern
        for c in range(self.FINDER_OFFSET + 1, len(self.matrix[0]) - self.FINDER_OFFSET - 1):
            self.matrix[self.FINDER_OFFSET - 1][c] = self.BLACK_MODULE if c % 2 == 0 else self.WHITE_MODULE

    def add_dark_module(self):
        r, c = ((self.MODULES_INCREMENT * self._version) + 9, 8)
        self.matrix[r][c] = self.BLACK_MODULE

    def add_encoded_data(self, encoded_string: str):
        """
        Start at bottom left and zig zag data into matrix
        :param encoded_string:
        :return:
        """

        ROWS, COLS = len(self.matrix[0]), len(self.matrix)
        r, c = ROWS - 1, COLS - 1
        nr, nc, order = -1, 0, 1
        vis = set()
        for i, ch in enumerate(encoded_string):
            pixel = self.WHITE_MODULE if ch == '0' else self.BLACK_MODULE
            self.matrix[r][c] = pixel

            # iterate until we find the next available module point
            try:
                while self.matrix[r][c] != 1:
                    # change pixel positions for next column and row
                    if order is 1:  # up
                        if nc == -1:
                            nr, nc = -1, 0
                            r -= 1
                            c += 1
                        else:
                            nr, nc = 0, -1
                            c -= 1
                    else:
                        if nc == -1:
                            nr, nc = -1, 0
                            r += 1
                            c += 1
                        else:
                            nr, nc = 0, -1
                            c -= 1

                    # check if out of bounds
                    if r < 0:
                        order = -1
                        r = 0
                        c -= 2
                        nr, nc = -1, 0
                    if r >= ROWS:
                        order = 1
                        r = ROWS - 1
                        c -= 2
                        nr, nc = -1, 0

                vis.add((r, c))
            except:
                print("what?", r, c)
                break
            # print((r, c))
            # print("iter", r, c, i, ch, start, self.matrix[r][c])

        print(len(vis))
        print(vis)

    def draw(self):
        # Visualize the data
        plt.imshow(np.array(self.matrix), cmap='gray', vmin=0, vmax=2)

        # Display the image
        plt.show()
