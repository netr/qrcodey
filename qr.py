class InvalidVersionNumber(Exception):
    """Version number must be between 1 and 40

    Attributes:
        version -- version number given
    """
    pass


class QrCode:
    MAX_VERSION = 40  # REF 1
    MIN_VERSION = 1
    MODULES_INCREMENT = 4
    MIN_MODULES = 21
    FINDER_OFFSET = 7

    def __init__(self, version: int):
        self.version = version
        self.modules = self.get_module_size()
        self.matrix = [[0] * self.modules for _ in range(self.modules)]
        self.add_patterns_and_separators()

    def get_module_size(self) -> int:
        """
        There are 40 versions of QR codes (from Version 1 (21 × 21 modules) to Version 40 (177 × 177 modules)).
        Each version has a different module configuration for storing different amounts of data.
        Each increment in version number increases the number of modules by 4 per side.
        More: https://tritonstore.com.au/qr-code-size/
        :return: Number of modules to be represented by a nxn grid
        """
        if self.version < self.MIN_VERSION or self.version > self.MAX_VERSION:
            raise InvalidVersionNumber(self.version)

        return self.MODULES_INCREMENT * (self.version - 1) + self.MIN_MODULES  # REF 1

    def add_patterns_and_separators(self):
        top_right = self.calculate_finder_position()
        bottom_left = self.calculate_finder_position(is_bottom_left=True)

        self.add_finder_pattern(0, 0)
        self.add_finder_pattern(*top_right)  # Use tuple unpacking
        self.add_finder_pattern(*bottom_left)
        self.add_separators()

    def calculate_finder_position(self, is_bottom_left=False):
        mod_minus_offset = self.modules - self.FINDER_OFFSET  # REF 1
        return (0, mod_minus_offset) if is_bottom_left else (mod_minus_offset, 0)

    def add_finder_pattern(self, xoffset, yoffset):
        """
        The top-left finder pattern's top left corner is always placed at (0,0).
        The top-right finder pattern's top LEFT corner is always placed at ([(((V-1)*4)+21) - 7], 0)
        The bottom-left finder pattern's top LEFT corner is always placed at (0,[(((V-1)*4)+21) - 7])
        """
        for i in range(yoffset + 0, yoffset + 7):
            for j in range(xoffset + 0, xoffset + 7):
                self.matrix[i][j] = 2

        for i in range(yoffset + 1, yoffset + 6):
            for j in range(xoffset + 1, xoffset + 6):
                self.matrix[i][j] = 1

        for i in range(yoffset + 2, yoffset + 5):
            for j in range(xoffset + 2, xoffset + 5):
                self.matrix[i][j] = 2

    def add_separator(self, xoffset, yoffset):
        for i in range(0, 8):
            self.matrix[i][xoffset + 7] = 4
            self.matrix[yoffset + 7][i] = 3

    def add_separators(self):
        self.add_horiz_separators()
        self.add_vertical_separators()

    def add_horiz_separators(self):
        for i in range(0, (self.FINDER_OFFSET + 1)):
            self.matrix[self.FINDER_OFFSET][i] = 1
            self.matrix[self.FINDER_OFFSET][len(self.matrix[0]) - i - 1] = 1
            self.matrix[len(self.matrix) - (self.FINDER_OFFSET + 1)][i] = 1

    def add_vertical_separators(self):
        for i in range(0, (self.FINDER_OFFSET + 1)):
            self.matrix[i][self.FINDER_OFFSET] = 1
            self.matrix[i][len(self.matrix[0]) - (self.FINDER_OFFSET + 1)] = 1
            self.matrix[len(self.matrix[0]) - i - 1][self.FINDER_OFFSET] = 1

    def calculate_top_right(self) -> [int, int]:
        return [(((self.version - 1) * 4) + self.MIN_MODULES) - self.FINDER_OFFSET, 0]

    def calculate_bottom_left(self) -> [int, int]:
        return [0, (((self.version - 1) * 4) + self.MIN_MODULES) - self.FINDER_OFFSET]
