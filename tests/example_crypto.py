from hashlib import sha3_256 as sha3
from base58 import b58decode
from base64 import b64encode

from pyost.algorithm import Ed25519, Secp256k1
from pyost.signature import Signature, KeyPair

if __name__ == '__main__':
    text = b'hello'
    info = sha3(text).digest()
    print(info.hex())

    seckey = b'1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB'
    kp = KeyPair(Ed25519, seckey)
    print(kp.algo_cls.__int__())
    print(b58decode(kp.seckey).hex())
    print(b58decode(kp.pubkey).hex())
    print(kp.id)

    sig = kp.sign(info)
    print(b58decode(sig.pubkey).hex())
    print(b58decode(sig.sig).hex())
    print(b64encode(b58decode(sig.pubkey)))
    print(b64encode(b58decode(sig.sig)))
