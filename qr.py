def build(version):
    modules = get_module_size_from_version(version)
    grid = [[0] * modules for _ in range(modules)]
    return grid


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


def add_finder_pattern(grid, xoffset, yoffset):
    """
    The top-left finder pattern's top left corner is always placed at (0,0).
    The top-right finder pattern's top LEFT corner is always placed at ([(((V-1)*4)+21) - 7], 0)
    The bottom-left finder pattern's top LEFT corner is always placed at (0,[(((V-1)*4)+21) - 7])
    """
    for i in range(yoffset + 0, yoffset + 7):
        for j in range(xoffset + 0, xoffset + 7):
            grid[i][j] = 2

    for i in range(yoffset + 1, yoffset + 6):
        for j in range(xoffset + 1, xoffset + 6):
            grid[i][j] = 1

    for i in range(yoffset + 2, yoffset + 5):
        for j in range(xoffset + 2, xoffset + 5):
            grid[i][j] = 2


def add_separator(grid, xoffset, yoffset):
    for i in range(0, 8):
        grid[i][xoffset + 7] = 4
        grid[yoffset + 7][i] = 3


def add_horiz_separators(grid):
    for i in range(0, 8):
        grid[7][i] = 1
        grid[7][len(grid[0]) - i - 1] = 1
        grid[len(grid) - 8][i] = 1


def add_vertical_separators(grid):
    for i in range(0, 8):
        grid[i][7] = 1
        grid[i][len(grid[0]) - 8] = 1
        grid[len(grid[0]) - i - 1][7] = 1


def calculate_top_right(version: int) -> [int, int]:
    return [(((version - 1) * 4) + 21) - 7, 0]


def calculate_bottom_left(version: int) -> [int, int]:
    return [0, (((version - 1) * 4) + 21) - 7]
