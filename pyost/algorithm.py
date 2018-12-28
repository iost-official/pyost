from abc import ABC, abstractmethod
import ed25519
import ecdsa
from base58 import b58encode, b58decode
import hashlib
from pyost.api.rpc.pb.rpc_pb2 import Signature


class Algorithm(ABC):
    ID = Signature.UNKNOWN
    NAME = 'UNKNOWN'

    @classmethod
    def get_algorithm_by_id(cls, id: int):
        if id == Ed25519.ID:
            return Ed25519
        elif id == Secp256k1.ID:
            return Secp256k1
        else:
            raise ValueError(f'no algorithm correspond to id {id}')

    @classmethod
    def get_algorithm_by_name(cls, name: str):
        if name == Ed25519.NAME:
            return Ed25519
        elif name == Secp256k1.NAME:
            return Secp256k1
        else:
            raise ValueError(f'no algorithm correspond to name {str}')

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
    ID = Signature.SECP256K1
    NAME = 'secp256k1'

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
        return vk.verify(sig, message)

    @classmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        return sk.get_verifying_key().to_string()

    @classmethod
    def gen_seckey(cls) -> bytes:
        sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
        return sk.to_string()


class Ed25519(Algorithm):
    ID = Signature.ED25519
    NAME = 'ed25519'

    @classmethod
    def __int__(cls) -> int:
        return Ed25519.ID

    @classmethod
    def __str__(cls) -> str:
        return Ed25519.NAME

    @classmethod
    def sign(cls, message: bytes, seckey: bytes) -> bytes:
        sk = ed25519.SigningKey(b58decode(seckey))
        return sk.sign(message)

    @classmethod
    def verify(cls, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        vk = ed25519.VerifyingKey(b58decode(pubkey))
        try:
            vk.verify(sig, message)
        except ed25519.BadSignatureError:
            return False
        return True

    @classmethod
    def get_pubkey(cls, seckey: bytes) -> bytes:
        sk = ed25519.SigningKey(b58decode(seckey))
        return b58encode(sk.get_verifying_key().to_bytes())

    @classmethod
    def gen_seckey(cls) -> bytes:
        sk, vk = ed25519.create_keypair()
        return b58encode(sk.to_bytes())


from base58 import b58encode, b58decode



def selftest():
    algo = Ed25519
    message = b"crypto libraries should always test themselves at powerup"
    seckey = algo.gen_seckey()
    print('sk', seckey)
    pubkey = algo.get_pubkey(seckey)
    print('vk', pubkey)

    seckey2 = algo.gen_seckey()
    print('sk2', seckey2)
    pubkey2 = algo.get_pubkey(seckey2)
    print('vk2', pubkey2)

    #sk = ed25519.SigningKey(seckey)
    #return sk.sign(message)
    sig = algo.sign(message, seckey)
    print('sig', sig)
    algo.verify(message, pubkey2, sig)


if __name__ == '__main__':
    selftest()