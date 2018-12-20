from hashlib import sha3_256 as sha3
from pyost.api.crypto.signature_pb2 import SignatureRaw
from pyost.algorithm import Algorithm, create_algorithm


class Signature():
    # message SignatureRaw {
    #     int32 algorithm = 1;
    #     bytes sig = 2;
    #     bytes pubKey = 3;
    # }
    def __init__(self, algorithm: Algorithm = None, info: bytes = None, privkey: bytes = None):
        self.algorithm: Algorithm = algorithm or create_algorithm()
        self.sig: bytes = algorithm.sign(info, privkey) if info is not None and privkey is not None else None
        self.pubkey: bytes = algorithm.get_pubkey(privkey) if privkey is not None else None

    def verify(self, info: bytes) -> bool:
        return self.algorithm.verify(info, self.pubkey, self.sig)

    def to_raw(self) -> SignatureRaw:
        return SignatureRaw(
            algorithm=int(self.algorithm),
            sig=self.sig,
            pubKey=self.pubkey)

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def from_raw(self, sr: SignatureRaw) -> None:
        self.algorithm = create_algorithm(sr.algorithm)
        self.sig = sr.sig
        self.pubkey = sr.pubKey

    def decode(self, data: bytes) -> None:
        sr = SignatureRaw()
        sr.ParseFromString(data)
        self.from_raw(sr)

    def hash(self) -> bytes:
        return sha3(self.encode())
