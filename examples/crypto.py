from hashlib import sha3_256 as sha3
from base64 import b64encode

from pyost.algorithm import Ed25519, Secp256k1
from pyost.signature import KeyPair

if __name__ == '__main__':
    text = b'hello'
    info = sha3(text).digest()
    print(info.hex())

    for algo in [Ed25519, Secp256k1]:
        kp = KeyPair(algo)
        print(kp.algo_cls.__int__())
        print(kp.seckey.hex())
        print(kp.pubkey.hex())

        sig = kp.sign(info)
        print(sig.pubkey.hex())
        print(sig.sig.hex())
        print(b64encode(sig.pubkey))
        print(b64encode(sig.sig))
