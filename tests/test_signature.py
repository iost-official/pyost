from unittest import main, TestCase
from hashlib import sha256
import hashlib
from base58 import b58decode, b58encode
from pyost.signature import Signature
from pyost.algorithm import Algorithm, Secp256k1


class TestSignature(TestCase):
    def test_encode_decode(self):
        info = sha256(b'hello').digest()
        seckey = sha256(b'seckey').digest()
        pubkey = Secp256k1.get_pubkey(seckey)
        sig = Signature(Secp256k1, info, seckey)
        self.assertEqual(sig.pubkey, pubkey)
        self.assertTrue(sig.verify(info))

        bsig = sig.encode()
        sig2 = Signature()
        sig2.decode(bsig)
        self.assertEqual(b58encode(sig2.pubkey), b58encode(sig.pubkey))
        self.assertEqual(b58encode(sig2.sig), b58encode(sig.sig))
        self.assertEqual(sig.algorithm, sig2.algorithm)


class TestSign(TestCase):
    def setUp(self):
        self.test_data = 'c6e193266883a500c6e51a117e012d96ad113d5f21f42b28eb648be92a78f92f'
        self.privkey = bytes.fromhex(self.test_data)
        self.pubkey = Secp256k1.get_pubkey(self.privkey)

    def test_sha256(self):
        sha = 'd4daf0546cb71d90688b45488a8fa000b0821ec14b73677b2fb7788739228c8b'
        self.assertEqual(sha256(self.privkey).hexdigest(), sha)

    def test_get_pubkey(self):
        pub = '0314bf901a6640033ea07b39c6b3acb675fc0af6a6ab526f378216085a93e5c7a2'
        self.assertEqual(self.pubkey.hex(), pub)

    def test_hash160(self):
        hash = '9c1185a5c5e9fc54612808977ee8f548b2258d31'
        m = hashlib.new('ripemd160')
        m.update(sha256(Secp256k1.get_pubkey(self.privkey)).digest())
        self.assertEqual(m.hexdigest(), hash)

    def test_sign_and_verify(self):
        info = sha256(bytearray([1,2,3,4])).digest()
        sig = Secp256k1.sign(info, self.privkey)
        self.assertTrue(Secp256k1.verify(info, self.pubkey, sig))
        self.assertFalse(Secp256k1.verify(info, self.pubkey, bytearray([5,6,7,8])))
