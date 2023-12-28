from encoder import DataEncoder, AlphanumericPair


def test_alphanumeric_encoder_encode():
    assert (
        DataEncoder.encode("HELLO WORLD", 2, "H")
        == "0010000001011011000010110111100011010001011100101101110001001101"
        "0100001101000000111011000001000111101100000100011110110000010001"
    )

    assert (
        DataEncoder.encode("HELLO CC WORLD", 2, "H")
        == "0010000001110011000010110111100011010001011100010001010001100111"
        "0100100010100110111011111000000011101100000100011110110000010001"
    )


def test_get_8bit_binary_numbers():
    data = (
        "0010000001011011000010110111100011010001011100101101110001001101"
        "0100001101000000111011000001000111101100000100011110110000010001"
    )
    expected = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]
    assert DataEncoder.get_8bit_binary_numbers(data) == expected


def test_get_character_count_indicator():
    assert DataEncoder.get_character_count_indicator("HELLO WORLD") == "000001011"


def test_alphanumeric_pair():
    assert AlphanumericPair("H", "E").encode() == "01100001011"
    assert AlphanumericPair(":", ":").encode() == "11111101000"
    assert AlphanumericPair("D", "").encode() == "001101"


def test_get_pair_value():
    assert AlphanumericPair("H", "E").get_pair_value() == 779
    assert AlphanumericPair(":", ":").get_pair_value() == 2024
    assert AlphanumericPair("D", "").get_pair_value() == 13


def test_byte_encoding():
    expected = [
        "01001000",
        "01100101",
        "01101100",
        "01101100",
        "01101111",
        "00101100",
        "00100000",
        "01110111",
        "01101111",
        "01110010",
        "01101100",
        "01100100",
        "00100001",
    ]
    assert DataEncoder._encode_bytes("Hello, world!") == expected


def test_numeric_encoding():
    assert DataEncoder._encode_numeric("8675309") == [
        "1101100011",
        "1000010010",
        "1001",
    ]


def test_get_8bit_binary_numbers_from_list():
    expected = ["01000101", "11110010", "00010001", "10101011"]
    assert DataEncoder.get_8bit_binary_numbers_from_list([69, 242, 17, 171]) == expected
