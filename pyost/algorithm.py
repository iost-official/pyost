from abc import ABC, abstractmethod
import ed25519
import ecdsa


class Algorithm(ABC):
    SECP256K1 = 0
    ED25519 = 1

    @abstractmethod
    def __int__(self) -> int:
        pass

    @abstractmethod
    def sign(self, message: bytes, seckey: bytes) -> bytes:
        pass

    @abstractmethod
    def verify(self, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        pass

    @abstractmethod
    def get_pubkey(self, seckey: bytes) -> bytes:
        pass

    @abstractmethod
    def gen_seckey(self) -> bytes:
        pass


def create_algorithm(algo: int = Algorithm.SECP256K1) -> Algorithm:
    if algo == Algorithm.ED25519:
        return Ed25519()
    elif algo == Algorithm.SECP256K1:
        return Secp256k1()
    else:
        return Secp256k1()


class Ed25519(Algorithm):
    def __int__(self) -> int:
        return Algorithm.ED25519

    def sign(self, message: bytes, seckey: bytes) -> bytes:
        sk = ed25519.SigningKey(seckey)
        return sk.sign(message)

    def verify(self, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        vk = ed25519.VerifyingKey(pubkey)
        return vk.verify(sig, message)

    def get_pubkey(self, seckey: bytes) -> bytes:
        sk = ed25519.SigningKey(seckey)
        return sk.get_verifying_key().to_bytes()

    def gen_seckey(self) -> bytes:
        sk, vk = ed25519.create_keypair()
        return sk.to_bytes()


class Secp256k1(Algorithm):
    def __int__(self) -> int:
        return Algorithm.SECP256K1

    def sign(self, message: bytes, seckey: bytes) -> bytes:
        sk = ecdsa.SigningKey.from_string(seckey, ecdsa.SECP256k1)
        return sk.sign(message)

    def verify(self, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        vk = ecdsa.VerifyingKey.from_string(pubkey, ecdsa.SECP256k1)
        return vk.verify(sig, message)

    def get_pubkey(self, seckey: bytes) -> bytes:
        sk = ecdsa.SigningKey.from_string(seckey)
        return sk.get_verifying_key()

    def gen_seckey(self) -> bytes:
        sk = ecdsa.SigningKey.generate(ecdsa.SECP256k1)
        return sk.to_string()


if __name__ == '__main__':
    algo1 = create_algorithm(Algorithm.SECP256K1)
    print(type(algo1), int(algo1))
    algo2 = create_algorithm(Algorithm.ED25519)
    print(type(algo2), int(algo2))
