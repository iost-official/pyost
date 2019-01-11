from __future__ import annotations
from typing import List

SLICE_SEP = b'^'
FIELD_SEP = b'`'
MAPKV_SEP = b'/'
MAP_SEP = b'<'
SLASH = b'\\'


class SimpleNotation:
    def __init__(self, byteorder='big'):
        self.buffer = bytearray()
        self.byteorder = byteorder

    @staticmethod
    def escape(bs: bytes) -> bytes:
        return bs.replace(SLASH, SLASH + SLASH)\
            .replace(SLICE_SEP, SLASH + SLICE_SEP)\
            .replace(FIELD_SEP, SLASH + FIELD_SEP)\
            .replace(MAPKV_SEP, SLASH + MAPKV_SEP)\
            .replace(MAP_SEP, SLASH + MAP_SEP)

    def to_bytes(self) -> bytes:
        return bytes(self.buffer)

    def write_bytes(self, bs: bytes, escape: bool = True) -> SimpleNotation:
        self.buffer += FIELD_SEP
        self.buffer += self.escape(bs) if escape else bs
        return self

    def write_string(self, s: str, escape: bool = True) -> SimpleNotation:
        return self.write_bytes(s.encode('latin1'), escape)

    def write_int64(self, i: int, escape: bool = True) -> SimpleNotation:
        return self.write_bytes(i.to_bytes(8, self.byteorder, signed=False), escape)

    def write_string_slice(self, ls: List[str], escape: bool = True) -> SimpleNotation:
        self.buffer += FIELD_SEP
        for s in ls:
            self.buffer += SLICE_SEP
            bs = s.encode('latin1')
            self.buffer += self.escape(bs) if escape else bs
        return self

    def write_bytes_slice(self, ls: List[bytes], escape: bool = True) -> SimpleNotation:
        self.buffer += FIELD_SEP
        for bs in ls:
            self.buffer += SLICE_SEP
            self.buffer += self.escape(bs) if escape else bs
        return self
