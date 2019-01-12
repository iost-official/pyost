from typing import List

KOOPMAN = 0xeb31d82e


def make_table(poly: int = KOOPMAN):
    """Create a table for a polynomial.

    Args:
        poly: The polynomial function.

    Returns:
        A 256 bytes long table.
    """
    table = [0] * 256
    for i in range(256):
        crc = i & 0xffffffff
        for j in range(8):
            if crc & 1:
                crc = ((crc >> 1) & 0xffffffff) ^ poly
            else:
                crc = ((crc >> 1) & 0xffffffff)
        table[i] = crc
    return table


def checksum(data: bytes, table: List[int], crc: int = 0) -> int:
    """Calculates a checksum with a CRC code and a polynomial table.

    Args:
        data: The data to calculate the checksum for.
        table: The polynomial table created by `make_table`.
        crc: The CRC code.

    Returns:
        The checksum.
    """
    crc = ~ crc & 0xffffffff
    for v in data:
        crc = table[(crc ^ v) & 0xff] ^ (crc >> 8)
    return ~ crc & 0xffffffff


def parity(data: bytes, little_endian=True) -> bytes:
    """Creates a polynomial table and calculates the checksum of a message.

    Args:
        data: The data to calculate the checksum for.
        little_endian: Tells whether the data should be packed as little or big endian.

    Returns:
        The checksum.
    """
    crc32q = make_table(KOOPMAN)
    crc = checksum(data, crc32q)
    return crc.to_bytes(4, 'little' if little_endian else 'big')


if __name__ == '__main__':
    base = bytes.fromhex('12345abcde')

    assert parity(base, little_endian=False).hex() == 'b98eda0f'
