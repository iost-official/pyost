from hashlib import sha3_256 as sha3
from base58 import b58decode, b58encode
from base64 import b64decode, b64encode

from pyost.algorithm import KeyPair, Ed25519
from pyost.signature import Signature

# console.log("======= test of hash");
# const hash = new SHA3(256);
# hash.update('hello');
# const info = hash.digest("binary");
# console.log("hash of hello >", info);
# hash of hello > <Buffer 33 38 be 69 4f 50 c5 f3 38 81 49 86 cd f0 68 64 53 a8 88 b8 4f 42 4d 79 2a f4 b9 20 23 98 f3 92>


# const seckey = Base58.decode('1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB');
# const edKP = new KeyPair(seckey, Algo.Ed25519);
# console.log(edKP);
#
# let sig = new Signature(info, edKP);
# console.log("pub >", sig.pubkey);
# console.log("sig >", sig.sig);
# console.log(sig.toJSON());

# KeyPair {
#   t: 2,
#   seckey:
#    <Buffer 00 bb 1f 7c 09 55 13 a4 7d 63 de e0 2c c9 4a 6a 1f f1 22 b7 be e1 04 ad df dd 99 55 6b 5b 91 45 57 31 ad eb 5d 1a 80 7e c9 c4 38 25 38 9e 5e df f7 04 ... 14 more bytes>,
#   pubkey:
#    <Buffer 57 31 ad eb 5d 1a 80 7e c9 c4 38 25 38 9e 5e df f7 04 12 e4 64 3a 94 62 9a 65 2a f1 bf cf 2f 08>,
#   id: 'IOSTfQFocqDn7VrKV7vvPqhAQGyeFU9XMYo5SNn5yQbdbzC75wM7C' }
# pub > <Buffer 57 31 ad eb 5d 1a 80 7e c9 c4 38 25 38 9e 5e df f7 04 12 e4 64 3a 94 62 9a 65 2a f1 bf cf 2f 08>
# sig > <Buffer eb 43 6f 1a f8 50 2d 45 4f 8b ce a4 72 ba c4 01 5f 78 27 d7 f9 04 27 ce 22 78 7f 14 bf 98 b8 3d 2c 2b 4d 1b 30 3a d4 20 1b 15 26 a1 a2 69 f0 69 dc bf ... 14 more bytes>
# { algorithm: 'ED25519',
#   public_key: 'VzGt610agH7JxDglOJ5e3/cEEuRkOpRimmUq8b/PLwg=',
#   signature:
#    '60NvGvhQLUVPi86kcrrEAV94J9f5BCfOInh/FL+YuD0sK00bMDrUIBsVJqGiafBp3L8oh6Y2eZuOczrNL9dTCA==' }


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

    sig = Signature(info, kp)
    print(b58decode(sig.pubkey).hex())
    print(b58decode(sig.sig).hex())
    print(b64encode(b58decode(sig.pubkey)))
    print(b64encode(b58decode(sig.sig)))
