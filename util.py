from const import CAPACITY_TABLE, Mode


def choose_qr_version(char_count: int, error_correction_level: str, mode: Mode):
    """
    Choose the appropriate QR code version for the given character count, error correction level, and character type.

    :param char_count: Number of characters in the QR code.
    :param error_correction_level: Error correction level ('L', 'M', 'Q', 'H').
    :param mode: Type of characters ('Numeric', 'Alphanumeric', 'Byte', 'Kanji').
    :return: The smallest version number that can accommodate the character count, or None if not possible.
    """

    if char_count <= 0:
        return None

    for version, ec_levels in CAPACITY_TABLE.items():
        # Check if the version and error correction level combination can accommodate the character count
        if ec_levels[error_correction_level][mode.value] >= char_count:
            return version
    return None
