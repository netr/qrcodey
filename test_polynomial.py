from encoder import AlphanumericEncoder
from polynomial import GeneratorPolynomial


def test_generator_polynomial():
    expected = [0, 251, 67, 46, 61, 118, 70, 64, 94, 32, 45]
    assert GeneratorPolynomial(10) == expected

    expected = [0, 87, 229, 146, 149, 238, 102, 21]
    assert GeneratorPolynomial(7) == expected


def test_divide_generator_with_message():
    expected = [196, 35, 39, 119, 235, 215, 231, 226, 93, 23]
    data = (
        "0010000001011011000010110111100011010001011100101101110001001101"
        "0100001101000000111011000001000111101100000100011110110000010001"
    )
    ans = GeneratorPolynomial(10) / AlphanumericEncoder.get_8bit_binary_numbers(data)
    assert ans == expected

    ans = GeneratorPolynomial(10).divide(
        AlphanumericEncoder.get_8bit_binary_numbers(data)
    )
    assert ans == expected

    ans = GeneratorPolynomial(28) / AlphanumericEncoder.get_8bit_binary_numbers(data)
    assert len(ans) == 28
