from const import Mode
from util import choose_qr_version


def test_capacity_table_choose_version():
    """
    <3 chatgpt
    """
    # Minimum Boundary
    assert choose_qr_version(1, "Q", Mode.NUMERIC) == 1
    assert choose_qr_version(1, "Q", Mode.ALPHANUMERIC) == 1

    # Just Below Maximum Boundary
    assert choose_qr_version(5595, "M", Mode.NUMERIC) == 40
    assert choose_qr_version(2330, "Q", Mode.ALPHANUMERIC) == 40

    # At Maximum Boundary
    assert choose_qr_version(5596, "M", Mode.NUMERIC) == 40
    assert choose_qr_version(2331, "Q", Mode.ALPHANUMERIC) == 40

    # Just Above Maximum Boundary
    assert choose_qr_version(5597, "Q", Mode.NUMERIC) is None
    assert choose_qr_version(2332, "H", Mode.ALPHANUMERIC) is None

    # Far Above Maximum Boundary
    assert choose_qr_version(10000, "M", Mode.NUMERIC) is None
    assert choose_qr_version(5000, "M", Mode.ALPHANUMERIC) is None

    # Zero Characters
    assert choose_qr_version(0, "M", Mode.NUMERIC) is None
    assert choose_qr_version(0, "M", Mode.ALPHANUMERIC) is None

    # Negative Character Count
    assert choose_qr_version(-1, "M", Mode.NUMERIC) is None
    assert choose_qr_version(-1, "M", Mode.ALPHANUMERIC) is None

    # Non-integer Character Count
    assert choose_qr_version(100.5, "M", Mode.NUMERIC) == 3
    assert choose_qr_version(50.5, "M", Mode.ALPHANUMERIC) == 3

    # Exact Capacity Match
    assert choose_qr_version(34, "M", Mode.NUMERIC) == 1
    assert choose_qr_version(14, "M", Mode.ALPHANUMERIC) == 1
