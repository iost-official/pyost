from __future__ import annotations
from typing import List
from pprint import pformat
from protobuf_to_dict import protobuf_to_dict
from pyost.api.rpc.pb import rpc_pb2 as pb
from pyost.transaction import AmountLimit


class Contract:
    class ABI:
        def __init__(self):
            self.name: str = ''
            self.args: List[str] = []
            self.amount_limit: List[AmountLimit] = []

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, abi: pb.Contract.ABI) -> Contract.ABI:
            self.name = abi.name
            self.args = abi.args
            self.amount_limit = [AmountLimit().from_raw(al) for al in abi.amount_limit
                                 ] if abi.amount_limit is not None else []
            return self

        def to_raw(self) -> pb.Contract.ABI:
            return pb.Contract.ABI(
                name=self.name,
                args=self.args,
                amount_limit=[al.to_raw() for al in self.amount_limit]
            )

    def __init__(self):
        self.id: str = ''
        self.code: str = ''
        self.language: str = ''
        self.version: str = ''
        self.abis: List[Contract.ABI] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, c: pb.Contract) -> Contract:
        self.id = c.id
        self.code = c.code
        self.language = c.language
        self.version = c.version
        self.abis = [Contract.ABI().from_raw(abi) for abi in c.abis
                     ] if c.abis is not None else []
        return self

    def to_raw(self) -> pb.Contract:
        return pb.Contract(
            id=self.id,
            code=self.code,
            language=self.language,
            version=self.version,
            abis=[abi.to_raw() for abi in self.abis]
        )
