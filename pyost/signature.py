from typing import Type
from hashlib import sha3_256 as sha3
from protobuf_to_dict import protobuf_to_dict
from base58 import b58encode, b58decode

from pyost.api.crypto.signature_pb2 import SignatureRaw
from pyost.algorithm import Algorithm, Secp256k1, Ed25519


class Signature():
    # message SignatureRaw {
    #     int32 algorithm = 1;
    #     bytes sig = 2;
    #     bytes pubKey = 3;
    # }
    def __init__(self, algorithm: Type[Algorithm] = Ed25519, info: bytes = None, privkey: bytes = None):
        self.algorithm: Type[Algorithm] = algorithm
        self.sig: bytes = algorithm.sign(info, privkey) if info is not None and privkey is not None else None
        self.pubkey: bytes = algorithm.get_pubkey(privkey) if privkey is not None else None

    def verify(self, info: bytes) -> bool:
        if self.pubkey is None or self.sig is None:
            raise ValueError('The Signature is missing pubkey and/or sig.')
        return self.algorithm.verify(info, self.pubkey, self.sig)

    def to_raw(self) -> SignatureRaw:
        return SignatureRaw(
            algorithm=self.algorithm.__int__(),
            sig=self.sig,
            pubKey=b58decode(self.pubkey)
        )

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def from_raw(self, sr: SignatureRaw) -> None:
        self.algorithm = Algorithm.get_algorithm_by_id(sr.algorithm)
        self.sig = sr.sig
        self.pubkey = b58encode(sr.pubKey)

    def decode(self, data: bytes) -> None:
        sr = SignatureRaw()
        sr.ParseFromString(data)
        self.from_raw(sr)

    def hash(self) -> bytes:
        return sha3(self.encode())

    def __str__(self) -> str:
        return str(protobuf_to_dict(self.to_raw()))
        #return f'Signature(algo={self.algorithm} sig={len(self.sig)}b pubkey={len(self.pubkey)}b'


if __name__ == '__main__':
    pass