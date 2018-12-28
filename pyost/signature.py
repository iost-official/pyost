from typing import Type
from hashlib import sha3_256 as sha3
from protobuf_to_dict import protobuf_to_dict
from base58 import b58encode, b58decode
from pprint import pformat

from pyost.api.rpc.pb import rpc_pb2 as pb
from pyost.algorithm import Algorithm, Secp256k1, Ed25519


class Signature:
    def __init__(self, algorithm: Type[Algorithm] = Ed25519,
                 info: str = None, privkey: str = None):
        self.algorithm: Type[Algorithm] = algorithm
        self.sig: str = algorithm.sign(info, privkey) if info is not None and privkey is not None else None
        self.pubkey: str = algorithm.get_pubkey(privkey) if privkey is not None else None

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def verify(self, info: str) -> bool:
        if self.pubkey is None or self.sig is None:
            raise ValueError('The Signature is missing pubkey and/or sig.')
        return self.algorithm.verify(info, self.pubkey, self.sig)

    def from_raw(self, sr: pb.Signature) -> None:
        self.algorithm = Algorithm.get_algorithm_by_id(sr.algorithm)
        self.sig = sr.sig
        self.pubkey = b58encode(sr.pubKey)

    def to_raw(self) -> pb.Signature:
        return pb.Signature(
            algorithm=self.algorithm.__int__(),
            sig=self.sig,
            public_key=b58decode(self.pubkey)
        )

    def hash(self) -> str:
        return sha3(self.to_raw().SerializeToString())


if __name__ == '__main__':
    pass
