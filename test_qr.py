import pytest

from qr import get_module_size_from_version, InvalidVersionNumber, build, calculate_top_right, calculate_bottom_left, \
    add_finder_pattern, add_horiz_separators, add_vertical_separators


def test_get_module_size_from_version():
    assert get_module_size_from_version(1) == 21
    assert get_module_size_from_version(40) == 177

    with pytest.raises(InvalidVersionNumber) as ex:
        get_module_size_from_version(0)


def test_build():
    version = 2
    grid = build(version)
    print(len(grid), len(grid[0]))
    print(calculate_top_right(version))
    top_right = calculate_top_right(version)
    bottom_left = calculate_bottom_left(version)
    add_finder_pattern(grid, 0, 0)
    add_finder_pattern(grid, top_right[0], top_right[1])
    add_finder_pattern(grid, bottom_left[0], bottom_left[1])
    add_horiz_separators(grid)
    add_vertical_separators(grid)
    # add_separator(grid, xoffset=0, yoffset=8)
    # add_separator(grid, bottom_left[0] + 7, bottom_left[1] - 7)
    for r in grid:
        print(r)


def test_calculate_finder_pattern_positions():
    assert calculate_top_right(1) == [14, 0]
    assert calculate_bottom_left(1) == [0, 14]

    assert calculate_top_right(32) == [138, 0]
    assert calculate_bottom_left(32) == [0, 138]
