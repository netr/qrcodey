from galois import GaloisField


def test_galois_field_get_exponents():
    assert GaloisField.get_exp(3) == 8
    assert GaloisField.get_exp(8) == 29
    assert GaloisField.get_exp(9) == 58
    assert GaloisField.get_exp(10) == 116
    assert GaloisField.get_exp(11) == 232
    assert GaloisField.get_exp(12) == 205


def test_galois_field_multiply():
    assert GaloisField.multiply(76, 43) == 251
