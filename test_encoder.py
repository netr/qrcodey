from encoder import AlphanumericEncoder, AlphanumericPair, choose_qr_version


def test_alphanumeric_encoder_encode():
    assert AlphanumericEncoder.encode("HELLO WORLD") == \
           "0010000001011011000010110111100011010001011100101101110001001101" \
           "0100001101000000111011000001000111101100000100011110110000010001"

    assert AlphanumericEncoder.encode("HELLO CC WORLD") == \
           "0010000001110011000010110111100011010001011100010001010001100111" \
           "0100100010100110111011111000000011101100000100011110110000010001"


def test_get_8bit_binary_numbers():
    data = "0010000001011011000010110111100011010001011100101101110001001101" \
           "0100001101000000111011000001000111101100000100011110110000010001"
    expected = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    assert AlphanumericEncoder.get_8bit_binary_numbers(data) == expected


def test_get_character_count_indicator():
    assert AlphanumericEncoder.get_character_count_indicator("HELLO WORLD") == "000001011"


def test_alphanumeric_pair():
    assert AlphanumericPair("H", "E").encode() == "01100001011"
    assert AlphanumericPair(":", ":").encode() == "11111101000"
    assert AlphanumericPair("D", "").encode() == "001101"


def test_get_pair_value():
    assert AlphanumericPair("H", "E").get_pair_value() == 779
    assert AlphanumericPair(":", ":").get_pair_value() == 2024
    assert AlphanumericPair("D", "").get_pair_value() == 13


def test_get_8bit_binary_numbers_from_list():
    expected = ["01000101", "11110010", "00010001", "10101011"]
    assert AlphanumericEncoder.get_8bit_binary_numbers_from_list([69, 242, 17, 171]) == expected


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
    assert choose_qr_version(0, 'Numeric') == 1
    assert choose_qr_version(0, 'Alphanumeric') == 1

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
