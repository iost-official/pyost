from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type
import ed25519
import ecdsa
from base58 import b58encode

from pyost.rpc.pb import rpc_pb2 as pb
from pyost import signature

def get_algorithm_by_id(id: int) -> Type[Algorithm]:
    if id == Ed25519.ID:
        return Ed25519
    elif id == Secp256k1.ID:
        return Secp256k1
    else:
        raise ValueError(f'no algorithm correspond to id {id}')


def get_algorithm_by_name(name: str) -> Type[Algorithm]:
    if name == Ed25519.NAME:
        return Ed25519
    elif name == Secp256k1.NAME:
        return Secp256k1
    else:
        raise ValueError(f'no algorithm correspond to name {name}')


class Algorithm(ABC):
    ID = pb.Signature.UNKNOWN
    NAME = 'UNKNOWN'

    @classmethod
    @abstractmethod
    def create_key_pair(cls) -> signature.KeyPair:
        pass

    @classmethod
    @abstractmethod
    def __int__(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def __str__(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def sign(cls, message: bytes, seckey: bytes) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def verify(cls, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        pass

    @classmethod
    @abstractmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        pass

    @classmethod
    @abstractmethod
    def gen_seckey(cls) -> bytes:
        pass


class Secp256k1(Algorithm):
    ID = pb.Signature.SECP256K1
    NAME = 'secp256k1'

    @classmethod
    def create_key_pair(cls) -> signature.KeyPair:
        return signature.KeyPair(Secp256k1)

    @classmethod
    def __int__(cls) -> int:
        return Secp256k1.ID

    @classmethod
    def __str__(cls) -> str:
        return Secp256k1.NAME

    @classmethod
    def sign(cls, message: bytes, seckey: bytes) -> bytes:
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        return sk.sign(message)

    @classmethod
    def verify(cls, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        vk = ecdsa.VerifyingKey.from_string(pubkey, ecdsa.SECP256k1)
        try:
            vk.verify(sig, message)
        except ecdsa.BadSignatureError:
            return False
        return True

    @classmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        return sk.get_verifying_key().to_string()

    @classmethod
    def get_compressed_pubkey(cls, seckey: bytes) -> bytes:
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        p = sk.get_verifying_key().pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), ecdsa.SECP256k1.generator.order())
        compressed = bytes(chr(2 + (p.y() & 1)), 'ascii') + x_str
        return compressed

    @classmethod
    def gen_seckey(cls) -> bytes:
        sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
        return sk.to_string()


class Ed25519(Algorithm):
    ID = pb.Signature.ED25519
    NAME = 'ed25519'

    @classmethod
    def create_key_pair(cls) -> signature.KeyPair:
        return signature.KeyPair(Ed25519)

    @classmethod
    def __int__(cls) -> int:
        return Ed25519.ID

    @classmethod
    def __str__(cls) -> str:
        return Ed25519.NAME

    @classmethod
    def sign(cls, message: bytes, seckey: bytes) -> bytes:
        sk = ed25519.SigningKey(seckey)
        return sk.sign(message)

    @classmethod
    def verify(cls, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        vk = ed25519.VerifyingKey(pubkey)
        try:
            vk.verify(sig, message)
        except ed25519.BadSignatureError:
            return False
        return True

    @classmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        sk = ed25519.SigningKey(seckey)
        return sk.get_verifying_key().to_bytes()

    @classmethod
    def gen_seckey(cls) -> bytes:
        sk, vk = ed25519.create_keypair()
        return sk.to_bytes()


def selftest():
    message = b"crypto libraries should always test themselves at powerup"

    for algo in [Ed25519, Secp256k1]:
        print(algo.NAME, algo.ID)

        kp = algo.create_key_pair()
        print(kp)

        kp2 = algo.create_key_pair()
        print(kp2)

        sig = kp.sign(message)
        print('sig', b58encode(sig))

        print(sig.verify(message))


if __name__ == '__main__':
    selftest()
