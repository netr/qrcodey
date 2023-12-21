def build():
    grid = [[0] * 21 for _ in range(21)]
    return grid


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


def calculate_top_right(version: int) -> [int, int]:
    return [(((version - 1) * 4) + 21) - 7, 0]


def calculate_bottom_left(version: int) -> [int, int]:
    return [0, (((version - 1) * 4) + 21) - 7]


def test_build():
    grid = build()
    print(len(grid), len(grid[0]))
    print(calculate_top_right(1))
    version = 1
    top_right = calculate_top_right(version)
    bottom_left = calculate_bottom_left(version)
    add_finder_pattern(grid, 0, 0)
    add_finder_pattern(grid, top_right[0], top_right[1])
    add_finder_pattern(grid, bottom_left[0], bottom_left[1])
    for r in grid:
        print(r)


def test_calculate_finder_pattern_positions():
    assert calculate_top_right(1) == [14, 0]
    assert calculate_bottom_left(1) == [0, 14]

    assert calculate_top_right(32) == [138, 0]
    assert calculate_bottom_left(32) == [0, 138]
