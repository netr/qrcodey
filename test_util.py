from util import choose_qr_version


def test_capacity_table_choose_version():
    """
    <3 chatgpt
    """
    # Minimum Boundary
    assert choose_qr_version(1, 'Numeric') == 1
    assert choose_qr_version(1, 'Alphanumeric') == 1

    # Just Below Maximum Boundary
    assert choose_qr_version(5595, 'Numeric') == 40
    assert choose_qr_version(2330, 'Alphanumeric') == 40

    # At Maximum Boundary
    assert choose_qr_version(5596, 'Numeric') == 40
    assert choose_qr_version(2331, 'Alphanumeric') == 40

    # Just Above Maximum Boundary
    assert choose_qr_version(5597, 'Numeric') is None
    assert choose_qr_version(2332, 'Alphanumeric') is None

    # Far Above Maximum Boundary
    assert choose_qr_version(10000, 'Numeric') is None
    assert choose_qr_version(5000, 'Alphanumeric') is None

    # Zero Characters
    assert choose_qr_version(0, 'Numeric') is None
    assert choose_qr_version(0, 'Alphanumeric') is None

    # Invalid Character Type
    try:
        choose_qr_version(100, 'InvalidType')
        assert False  # Should not reach this line
    except KeyError:
        assert True  # Expected a KeyError

    # Negative Character Count
    assert choose_qr_version(-1, 'Numeric') is None
    assert choose_qr_version(-1, 'Alphanumeric') is None

    # Non-integer Character Count
    assert choose_qr_version(100.5, 'Numeric') == 3
    assert choose_qr_version(50.5, 'Alphanumeric') == 4

    # Exact Capacity Match
    assert choose_qr_version(34, 'Numeric') == 1
    assert choose_qr_version(14, 'Alphanumeric') == 1
