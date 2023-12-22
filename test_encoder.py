from encoder import AlphanumericEncoder, AlphanumericPair


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
