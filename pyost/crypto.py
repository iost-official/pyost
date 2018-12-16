from pyost.api.crypto import signature_pb2
import ed25519


class Algorithm():
    def __init__(self):
        self.pubkey: ed25519.SigningKey = None

    def sign(self, message: bytes, seckey: bytes) -> bytes:
        pass

    def verify(self, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        pass

    def get_pubkey(self, seckey: bytes) -> bytes:
        pass

    def gen_seckey(self) -> bytes:
        pass


class Ed25519(Algorithm):
    def sign(self, message: bytes, seckey: bytes) -> bytes:
        signingkey = ed25519.SigningKey(seckey)
        return signingkey.sign(message)

    def verify(self, message: bytes, pubkey: bytes, sig: bytes) -> bool:
        verifykey = ed25519.VerifyingKey(pubkey)
        return verifykey.verify(sig, message)

    def get_pubkey(self, seckey: bytes) -> bytes:
        return self.pubkey.to_bytes()

    def gen_seckey(self) -> bytes:
        seckey, self.pubkey = ed25519.create_keypair()
        return seckey.to_bytes()


class Signature():
    def __init__(self, algo: Algorithm, info: bytes, privkey: bytes):
        self.algo = algo
        self.sig = algo.sign(info, privkey)
        self.pubkey = algo.get_pubkey(privkey)
