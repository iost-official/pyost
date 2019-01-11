from typing import Type
from hashlib import sha3_256 as sha3
from base58 import b58encode, b58decode

from pyost.rpc.pb import rpc_pb2 as pb
from pyost.algorithm import Algorithm, get_algorithm_by_id
from pyost.simplenotation import SimpleNotation
from pyost.crc32 import parity


def get_id_by_pubkey(pubkey: bytes) -> str:
    return 'IOST' + b58encode(pubkey + parity(pubkey)).decode('utf-8')


def get_pubkey_by_id(pubid: str) -> bytes:
    b = b58decode(pubid[4:])
    return b[:-4]


class Signature:
    def __init__(self, algo_cls: Type[Algorithm] = Algorithm, message: bytes = None, seckey: bytes = None):
        self.algo_cls: Type[Algorithm] = algo_cls
        self.sig: bytes = algo_cls.sign(message, seckey)
        self.pubkey: bytes = algo_cls.get_pubkey(seckey)

    def __str__(self) -> str:
        return f"'algo': {self.algo_cls.__int__()}\n" \
            f"'sig': '{b58encode(self.sig)}'\n" \
            f"'pubkey': '{b58encode(self.pubkey)}'"

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

    def to_bytes(self) -> bytes:
        sn = SimpleNotation()
        sn.write_bytes(self.algo_cls.__int__().to_bytes(1, sn.byteorder, signed=False))
        sn.write_bytes(self.sig)
        sn.write_bytes(self.pubkey)
        return sn.to_bytes()

    def decode(self, data: bytes) -> None:
        sr = pb.Signature()
        sr.ParseFromString(data)
        self.from_raw(sr)

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def hash(self) -> bytes:
        return sha3(self.to_bytes()).digest()


class KeyPair:
    def __init__(self, algo_cls: Type[Algorithm], seckey: bytes = None):
        self.algo_cls: Type[Algorithm] = algo_cls
        self.seckey: bytes = seckey if seckey is not None else algo_cls.gen_seckey()
        self.pubkey: bytes = algo_cls.get_pubkey(self.seckey)
        self.id: str = get_id_by_pubkey(self.pubkey)

    def __repr__(self):
        return f"{{'algo_cls': {self.algo_cls.__int__()},\n" \
            f"'id': '{self.id}',\n" \
            f"'pubkey': '{b58encode(self.pubkey)}',\n" \
            f"'seckey': '{b58encode(self.seckey)}'}}"

    def __str__(self):
        return self.__repr__()

    def sign(self, message: bytes) -> Signature:
        return Signature(self.algo_cls, message, self.seckey)
