from const import CAPACITY_TABLE


def choose_qr_version(char_count, char_type):
    """
    Choose the appropriate QR code version for the given character count and type.

    :param char_count: Number of characters in the QR code.
    :param char_type: Type of characters ('Numeric' or 'Alphanumeric').
    :return: The smallest version number that can accommodate the character count, or None if not possible.
    """

    if char_count <= 0:
        return None

    for version, capacities in CAPACITY_TABLE.items():
        if capacities[char_type] >= char_count:
            return version
    return None
