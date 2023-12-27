import math
from pathlib import Path
from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from const import FORMAT_STRINGS, ALIGNMENT_PATTERN_LOCATIONS, Mode
from encoder import AlphanumericEncoder
from polynomial import GeneratorPolynomial
from util import choose_qr_version


class InvalidVersionNumber(Exception):
    """
    This class represents an exception that is raised when an invalid version number is encountered.

    """

    pass


class InvalidMaskPatternId(Exception):
    pass


def encode_data(data: str) -> str:
    enc = AlphanumericEncoder.encode(data, 2, "H")
    poly = GeneratorPolynomial(28).divide(
        AlphanumericEncoder.get_8bit_binary_numbers(enc)
    )
    data = (
        enc
        + "".join(AlphanumericEncoder.get_8bit_binary_numbers_from_list(poly))
        + "0000000"
    )

    return data


def make(data: str):
    qr = QrCode(data)
    qr.add_static_patterns()
    qr.add_encoded_data(encode_data(data))
    qr.add_dark_module()

    return qr


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
           calculate_finder_position(self, is_bottom_left=False) ->
       evaluator = PenaltyEvaluator()
    tuple: Calculates the position of the finder patterns.
           add_finder_pattern(self, xoffset, yoffset): Adds the finder pattern to the QR code matrix.
           add_separators(self): Adds the separators to the QR code matrix.
           add_horiz_separators(self): Adds the horizontal separators to the QR code matrix.
           add_vertical_separators(self): Adds the vertical separators to the QR code matrix.
    """

    MAX_VERSION = 40  # REF 1
    MIN_VERSION = 1
    MODULES_INCREMENT = 4
    MIN_MODULES = 21
    FINDER_OFFSET = 7
    BLACK_MODULE = 0
    EMPTY_MODULE = 1
    WHITE_MODULE = 2

    def __init__(self, data: str):
        self._rawdata = data
        self._version = choose_qr_version(len(data), Mode.ALPHANUMERIC.value)
        self._modules = self.get_module_size()
        self._dataset = set()
        self.matrix = [
            [self.EMPTY_MODULE] * self._modules for _ in range(self._modules)
        ]

    def get_module_size(self) -> int:
        """
        There are 40 versions of QR codes (from Version 1 (21 × 21 modules) to Version 40 (177 × 177 modules)).
        Each version has a different module configuration for storing different amounts of data.
        Each increment in version number increases the number of modules by 4 per side.
        More: https://tritonstore.com.au/qr-code-size/
        :return: Number of modules to be represented by a nxn grid
        """
        if (
            self._version is None
            or self._version < self.MIN_VERSION
            or self._version > self.MAX_VERSION
        ):
            raise InvalidVersionNumber(self._version)

        return self.MODULES_INCREMENT * (self._version - 1) + self.MIN_MODULES  # REF 1

    def add_static_patterns(self):
        """
        Helper function to add all of the static patterns required by the QR code to function properly
        """
        self.add_finder_patterns()
        self.add_separators()
        self.add_alignment_patterns()
        self.add_reserve_modules()
        self.add_timing_patterns()
        self.add_dark_module()

    def add_finder_patterns(self):
        """
        Adds the top-left, top-right and bottom-left finder patterns
        :return:
        """
        top_right = self._calculate_finder_position()
        bottom_left = self._calculate_finder_position(is_bottom_left=True)

        self.add_finder_pattern(0, 0)
        self.add_finder_pattern(*top_right)  # Use tuple unpacking
        self.add_finder_pattern(*bottom_left)

    def _calculate_finder_position(self, is_bottom_left=False):
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
        self._add_horiz_separators()
        self._add_vertical_separators()

    def _add_horiz_separators(self):
        for i in range(0, (self.FINDER_OFFSET + 1)):
            self.matrix[self.FINDER_OFFSET][i] = self.WHITE_MODULE
            self.matrix[self.FINDER_OFFSET][
                len(self.matrix[0]) - i - 1
            ] = self.WHITE_MODULE
            self.matrix[len(self.matrix) - (self.FINDER_OFFSET + 1)][
                i
            ] = self.WHITE_MODULE

    def _add_vertical_separators(self):
        for i in range(0, (self.FINDER_OFFSET + 1)):
            self.matrix[i][self.FINDER_OFFSET] = self.WHITE_MODULE
            self.matrix[i][
                len(self.matrix[0]) - (self.FINDER_OFFSET + 1)
            ] = self.WHITE_MODULE
            self.matrix[len(self.matrix[0]) - i - 1][
                self.FINDER_OFFSET
            ] = self.WHITE_MODULE

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
            for dx, dy in [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]:
                self.matrix[x + dx][y + dy] = self.WHITE_MODULE
            # draw the outer most, horizontal black rows
            for dx, dy in [
                (-2, -2),
                (-2, -1),
                (-2, 0),
                (-2, 1),
                (-2, 2),
                (2, -2),
                (2, -1),
                (2, 0),
                (2, 1),
                (2, 2),
            ]:
                self.matrix[x + dx][y + dy] = self.BLACK_MODULE
            # draw the outer most, vertical black rows
            for dx, dy in [(-1, -2), (0, -2), (1, -2), (-1, 2), (0, 2), (1, 2)]:
                self.matrix[x + dx][y + dy] = self.BLACK_MODULE

    def add_reserve_modules(self, pixel=None):
        if pixel is None:
            pixel = self.WHITE_MODULE
        for i in range(0, 8):
            self.matrix[8][i] = pixel
            self.matrix[8][len(self.matrix[0]) - i - 1] = pixel

        for i in range(0, 9):
            self.matrix[i][8] = pixel

        for i in range(0, 7):
            self.matrix[len(self.matrix) - i - 1][8] = pixel

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

    def _validate_alignment_points(
        self, points: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
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
            if x <= self.FINDER_OFFSET and y >= (
                len(self.matrix[0]) - self.FINDER_OFFSET
            ):  # top right
                continue
            if (
                x >= (len(self.matrix) - self.FINDER_OFFSET) and y <= self.FINDER_OFFSET
            ):  # bottom left
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
        for r in range(
            self.FINDER_OFFSET + 1, len(self.matrix) - self.FINDER_OFFSET - 1
        ):
            self.matrix[r][self.FINDER_OFFSET - 1] = (
                self.BLACK_MODULE if r % 2 == 0 else self.WHITE_MODULE
            )

        # draw horizontal timing pattern
        for c in range(
            self.FINDER_OFFSET + 1, len(self.matrix[0]) - self.FINDER_OFFSET - 1
        ):
            self.matrix[self.FINDER_OFFSET - 1][c] = (
                self.BLACK_MODULE if c % 2 == 0 else self.WHITE_MODULE
            )

    def add_dark_module(self):
        r, c = ((self.MODULES_INCREMENT * self._version) + 9, 8)
        self.matrix[r][c] = self.BLACK_MODULE

    def add_encoded_data(self, encoded_string: str):
        """
        Start at bottom left and zig zag data into matrix
        :param encoded_string:
        :return:
        """

        ORDER_UP, ORDER_DOWN = 1, -1
        ROWS, COLS = len(self.matrix[0]), len(self.matrix)
        # start at the bottom left of the matrix
        r, c = ROWS - 1, COLS - 1
        # order dictates the current direction of module swaps
        order: int = ORDER_UP
        # switch row is triggered when two modules have been swapped on the current row
        switch_row = False
        for i, ch in enumerate(encoded_string):
            module = self.WHITE_MODULE if ch == "0" else self.BLACK_MODULE
            self.matrix[r][c] = module
            self._dataset.add((r, c))

            try:
                while self._is_module_filled(r, c):
                    # change pixel positions for next column and row
                    if order == ORDER_UP:
                        match switch_row:
                            case True:
                                switch_row = False
                                r -= 1
                                c += 1
                            case False:
                                switch_row = True
                                c -= 1
                    elif order == ORDER_DOWN:
                        match switch_row:
                            case True:
                                switch_row = False
                                r += 1
                                c += 1
                            case False:
                                switch_row = True
                                c -= 1

                    # check if out of bounds
                    if r < 0:
                        order = ORDER_DOWN
                        switch_row = False
                        r = 0
                        c -= 2
                    elif r >= ROWS:
                        order = ORDER_UP
                        switch_row = False
                        r = ROWS - 1
                        c -= 2

                    # fixes the issue of modules being upside down when touching the vertical timing line
                    if self._is_on_veritcal_timing(r, c):
                        c -= 1

            except IndexError:
                break

    def apply_mask(self, pattern_id: int) -> List[List[int]]:
        strategy = MaskStrategies().get(pattern_id)
        if strategy is None:
            raise InvalidMaskPatternId

        masked = self.matrix[:]
        for r, c in self._dataset:
            if strategy(r, c):
                masked[r][c] = (
                    self.WHITE_MODULE
                    if masked[r][c] is self.BLACK_MODULE
                    else self.BLACK_MODULE
                )

        return masked

    def _is_on_veritcal_timing(self, r, c) -> bool:
        if r in range(
            self.FINDER_OFFSET + 1, len(self.matrix) - self.FINDER_OFFSET - 1
        ):
            return c == self.FINDER_OFFSET - 1
        return False

    def _is_module_filled(self, r: int, c: int) -> bool:
        return self.matrix[r][c] != self.EMPTY_MODULE

    def add_format_string(
        self, matrix: List[List[int]], ecc: str, mask_pattern_id: int
    ) -> List[List[int]]:
        fs = FORMAT_STRINGS[ecc][mask_pattern_id]
        # top-left horizontal
        for i in range(0, 9):
            if i == 6:
                continue
            c = i if i < 6 else i - 1
            matrix[8][i] = self.BLACK_MODULE if fs[c] == "1" else self.WHITE_MODULE

        # top-right horizontal
        for i in range(0, 8):
            c = 14 - i
            matrix[8][len(matrix[0]) - i - 1] = (
                self.BLACK_MODULE if fs[c] == "1" else self.WHITE_MODULE
            )

        # top-left vertical
        for i in range(0, 9):
            if i == 6:
                continue
            c = 14 - i if i < 6 else 14 - i + 1
            matrix[i][8] = self.BLACK_MODULE if fs[c] == "1" else self.WHITE_MODULE

        # bottom-left vertical
        for i in range(0, 7):
            matrix[len(matrix[0]) - i - 1][8] = (
                self.BLACK_MODULE if fs[i] == "1" else self.WHITE_MODULE
            )

        return matrix

    def find_best_mask(self, ecc: str) -> int:
        evaluator = PenaltyEvaluator()
        best_mask = -1
        best_score = math.inf
        for i in range(8):
            temp_matrix = self.apply_mask(i)
            temp_matrix = self.add_format_string(temp_matrix, ecc, i)
            score = evaluator.evaluate(temp_matrix)
            if score < best_score:
                best_mask = i
                best_score = score

        return best_mask

    def _generate_best_fit(self, ecc: str) -> List[List[int]]:
        """
        Find the mask with the lowest penalty score and apply it to the internal matrix.
        Used by `draw` and `save` to ensure they are idempotent.
        Format strings are added in this function also, because they are coupled by the ecc and mask.

        :param ecc: Error Correction Code
        :return: New matrix object with best fit mask and format strings
        """
        mask = self.find_best_mask(ecc)
        matrix = self.apply_mask(mask)
        matrix = self.add_format_string(matrix, ecc, mask)
        return matrix

    def draw(self, ecc: str = "H"):
        matrix = self._generate_best_fit(ecc)

        # Visualize the data
        plt.imshow(np.array(matrix), cmap="gray", vmin=0, vmax=2)

        # Display the image
        plt.show()

    def save(
        self,
        path: Path,
        scale=10,
        bg_color=(255, 255, 255),
        data_color=(0, 0, 0),
        ecc: str = "H",
    ):
        matrix = self._generate_best_fit(ecc)

        img = Image.new(mode="RGB", size=(len(matrix), len(matrix[0])), color=bg_color)
        pixels = img.load()

        # add qr data to image
        for r in range(img.size[0]):
            for c in range(img.size[1]):
                if matrix[r][c] == 0:
                    pixels[r, c] = data_color

        # resize image to sacle
        img = img.resize(size=(img.size[0] * scale, img.size[1] * scale))

        # save image to disk
        img.save(path)


class MaskStrategies:
    def __init__(self):
        self.strategies = {
            0: self._pattern_0,
            1: self._pattern_1,
            2: self._pattern_2,
            3: self._pattern_3,
            4: self._pattern_4,
            5: self._pattern_5,
            6: self._pattern_6,
            7: self._pattern_7,
        }

    def get(self, pattern_id: int):
        return self.strategies.get(pattern_id)

    @staticmethod
    def _pattern_0(r: int, c: int) -> bool:
        return (r + c) % 2 == 0

    @staticmethod
    def _pattern_1(r: int, c: int) -> bool:
        return r % 2 == 0

    @staticmethod
    def _pattern_2(r: int, c: int) -> bool:
        return c % 3 == 0

    @staticmethod
    def _pattern_3(r: int, c: int) -> bool:
        return (r + c) % 3 == 0

    @staticmethod
    def _pattern_4(r: int, c: int) -> bool:
        return ((r // 2) + (c // 3)) % 2 == 0

    @staticmethod
    def _pattern_5(r: int, c: int) -> bool:
        return ((r * c) % 2) + ((r * c) % 3) == 0

    @staticmethod
    def _pattern_6(r: int, c: int) -> bool:
        return (((r * c) % 2) + ((r * c) % 3)) % 2 == 0

    @staticmethod
    def _pattern_7(r: int, c: int) -> bool:
        return (((r + c) % 2) + ((r * c) % 3)) % 2 == 0


class PenaltyEvaluator:
    def __init__(self):
        self.conditions = {
            1: self._evaluate_1,
        }

    def evaluate(self, matrix: List[List[int]]) -> int:
        score = 0
        score += self._evaluate_1(matrix)
        score += self._evaluate_2(matrix)
        score += self._evaluate_3(matrix)
        score += self._evaluate_4(matrix)
        return score

    @staticmethod
    def _evaluate_1(matrix: List[List[int]]) -> int:
        points = 0
        for r in range(len(matrix)):
            count = 1
            for c in range(1, len(matrix[r])):
                if matrix[r][c] == matrix[r][c - 1]:
                    count += 1
                else:
                    count = 1

                if count == 5:
                    points += 3
                elif count > 5:
                    points += 1

        for c in range(len(matrix[0])):
            count = 1
            for r in range(1, len(matrix)):
                if matrix[r][c] == matrix[r - 1][c]:
                    count += 1
                else:
                    count = 1

                if count == 5:
                    points += 3
                elif count > 5:
                    points += 1

        return points

    @staticmethod
    def _evaluate_2(matrix: List[List[int]]) -> int:
        points = 0
        dirs = [(0, 1), (1, 0), (1, 1)]
        ROWS, COLS = len(matrix), len(matrix[0])
        for r in range(len(matrix)):
            for c in range(len(matrix[r])):
                matches = 0
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if nr in range(ROWS) and nc in range(COLS):
                        if matrix[r][c] == matrix[nr][nc]:
                            matches += 1
                        else:
                            break
                if matches == 3:
                    points += 3

        return points

    @staticmethod
    def _evaluate_3(matrix: List[List[int]]) -> int:
        points = 0
        pattern_1 = (2, 2, 2, 2, 0, 2, 0, 0, 0, 2, 0)
        pattern_2 = (0, 2, 0, 0, 0, 2, 0, 2, 2, 2, 2)

        for r in range(len(matrix)):
            for c in range(len(matrix[r])):
                if (
                    tuple(matrix[r][c : c + 11]) == pattern_1
                    or tuple(matrix[r][c : c + 11]) == pattern_2
                ):
                    points += 40

        matrix = list(zip(*matrix))
        for r in range(len(matrix)):
            for c in range(len(matrix[r])):
                if (
                    matrix[r][c : c + 11] == pattern_1
                    or matrix[r][c : c + 11] == pattern_2
                ):
                    points += 40

        return points

    @staticmethod
    def _evaluate_4(matrix: List[List[int]]) -> int:
        black = 0
        white = 0
        for r in range(len(matrix)):
            for c in range(len(matrix[r])):
                if matrix[r][c] == 0:
                    black += 1
                else:
                    white += 1

        # Calculate the percentage of dark modules in the QR code.
        dark_pct = (black / (black + white)) * 100

        # Determine the previous and next multiple of five of the percentage in step 1
        prev_multiple_of_five = dark_pct // 5 * 5
        next_multiple_of_five = prev_multiple_of_five + 5

        # Subtract 50 from the numbers in step 2. Then, take their absolute values.
        value_prev = abs(dark_pct - prev_multiple_of_five)
        value_next = abs(dark_pct - next_multiple_of_five)

        # Divide the numbers from Step 3 by 5
        value_prev /= 5
        value_next /= 5

        # Take the smaller of the two numbers and multiply it by 10.
        final_score = min(value_prev, value_next) * 10

        return int(final_score)
