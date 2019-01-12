from __future__ import annotations
from typing import List


class SimpleEncoder:
    def __init__(self, byteorder='big'):
        self.buffer = bytearray()
        self.byteorder = byteorder

    def to_bytes(self) -> bytes:
        return bytes(self.buffer)

    def write_bytes(self, bs: bytes) -> SimpleEncoder:
        self.write_int32(len(bs))
        self.buffer += bs
        return self

    def write_string(self, s: str) -> SimpleEncoder:
        return self.write_bytes(s.encode('latin1'))

    def write_int32(self, i: int) -> SimpleEncoder:
        self.buffer += i.to_bytes(4, self.byteorder, signed=False)
        return self

    def write_int64(self, i: int) -> SimpleEncoder:
        self.buffer += i.to_bytes(8, self.byteorder, signed=False)
        return self

    def write_string_slice(self, ls: List[str]) -> SimpleEncoder:
        self.write_int32(len(ls))
        for s in ls:
            self.write_string(s)
        return self

    def write_bytes_slice(self, ls: List[bytes]) -> SimpleEncoder:
        self.write_int32(len(ls))
        for bs in ls:
            self.write_bytes(bs)
        return self
