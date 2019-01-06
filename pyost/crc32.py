from typing import List

KOOPMAN = 0xeb31d82e


def make_table(poly: int = KOOPMAN):
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


def update(crc: int, table: List[int], data: bytes) -> int:
    crc = ~ crc & 0xffffffff
    for v in data:
        crc = table[(crc ^ v) & 0xff] ^ (crc >> 8)
    return ~ crc & 0xffffffff


def checksum(data: bytes, table: List[int]) -> int:
    return update(0, table, data)


def parity(bit: bytes, little_endian=True) -> bytes:
    crc32q = make_table(KOOPMAN)
    crc = checksum(bit, crc32q)
    return crc.to_bytes(4, 'little' if little_endian else 'big')


if __name__ == '__main__':
    base = bytes.fromhex('12345abcde')

    assert parity(base, little_endian=False).hex() == 'b98eda0f'
