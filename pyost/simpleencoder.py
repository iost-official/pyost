from __future__ import annotations
from typing import List


class SimpleEncoder:
    """Provides methods to encodes different types to bytes.
    Each `write` call adds bytes to the internal `buffer`.
    Before each data, the data's length is encoded as an int32.

    Args:
        byteorder: Indicates in which order bytes must be encoded, can be ``big`` or ``little`` endian.

    Attributes:
        buffer: The internal bytes array.
        byteorder: Indicates in which order bytes must be encoded, can be ``big`` or ``little`` endian.
    """
    def __init__(self, byteorder='big'):
        self.buffer = bytearray()
        self.byteorder = byteorder

    def to_bytes(self) -> bytes:
        """Returns the internal buffer as a bytes type.

        Returns:
            The internal buffer as a bytes type.
        """
        return bytes(self.buffer)

    def write_bytes(self, bs: bytes, with_len=True) -> SimpleEncoder:
        """Adds bytes to the buffer.
        If `with_len`, before adding the bytes, add the number of bytes, encoded as an int32.

        Args:
            bs: The bytes to add to the buffer.
            with_len: Whether to add length before the bytes

        Returns:
            Itself.
        """
        if with_len:
            self.write_int32(len(bs))
        self.buffer += bs
        return self

    def write_string(self, s: str, encoding='latin1') -> SimpleEncoder:
        """Encodes a ``latin1`` string to bytes and adds it to the buffer.

        Args:
            s: The string to encode.
            encoding: ``latin1`` by default.

        Returns:
            Itself.
        """
        return self.write_bytes(s.encode(encoding))

    def write_int32(self, i: int) -> SimpleEncoder:
        """Encodes a number as an int32 and adds it to the buffer.

        Args:
            i: The number to encode.

        Returns:
            Itself.
        """
        self.buffer += i.to_bytes(4, self.byteorder, signed=False)
        return self

    def write_int64(self, i: int) -> SimpleEncoder:
        """Encodes a number as an int64 and adds it to the buffer.

        Args:
            i: The number to encode.

        Returns:
            Itself.
        """
        self.buffer += i.to_bytes(8, self.byteorder, signed=False)
        return self

    def write_string_slice(self, ls: List[str]) -> SimpleEncoder:
        """Encodes a list of ``latin1`` strings and adds them to the buffer.

        Args:
            ls: The list of strings to encode.

        Returns:
            Itself.
        """
        self.write_int32(len(ls))
        for s in ls:
            self.write_string(s)
        return self

    def write_bytes_slice(self, ls: List[bytes]) -> SimpleEncoder:
        """Encodes a list of bytes and adds them to the buffer.

        Args:
            ls: The list of bytes to encode.

        Returns:
            Itself.
        """
        self.write_int32(len(ls))
        for bs in ls:
            self.write_bytes(bs)
        return self
