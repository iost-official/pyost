from typing import Type
from hashlib import sha3_256 as sha3
from protobuf_to_dict import protobuf_to_dict
from pprint import pformat

from pyost.api.rpc.pb import rpc_pb2 as pb
from pyost.algorithm import KeyPair, Algorithm, get_algorithm_by_id


class Signature:
    def __init__(self, message: bytes = None, kp: KeyPair = None):
        self.algo_cls: Type[Algorithm] = kp.algo_cls if kp is not None else None
        self.sig: bytes = kp.sign(message) if message is not None and kp is not None else None
        self.pubkey: bytes = kp.pubkey if kp is not None else None

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def verify(self, message: bytes) -> bool:
        if self.pubkey is None or self.sig is None:
            raise ValueError('The Signature is missing pubkey and/or sig.')
        return self.algo_cls.verify(message, self.pubkey, self.sig)

    def from_raw(self, sr: pb.Signature) -> None:
        self.algo_cls = get_algorithm_by_id(sr.algorithm)
        self.sig = sr.signature
        self.pubkey = sr.public_key

    def to_raw(self) -> pb.Signature:
        return pb.Signature(
            algorithm=self.algo_cls.__int__(),
            signature=self.sig,
            public_key=self.pubkey,
        )

    def decode(self, data: bytes) -> None:
        sr = pb.Signature()
        sr.ParseFromString(data)
        self.from_raw(sr)

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def hash(self) -> bytes:
        return sha3(self.encode()).digest()


if __name__ == '__main__':
    pass
