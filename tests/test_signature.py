from unittest import main, TestCase
from hashlib import sha3_256 as sha3
from base58 import b58decode, b58encode
from base64 import b64decode, b64encode
from pyost.signature import Signature, KeyPair
from pyost.algorithm import Algorithm, Secp256k1


class TestSignature(TestCase):
    def test_encode_decode(self):
        info = sha3(b'hello').digest()
        seckey = sha3(b'seckey').digest()
        kp = KeyPair(Secp256k1, seckey)
        sig = Signature(info, kp)
        self.assertEqual(sig.pubkey, kp.pubkey)
        self.assertTrue(sig.verify(info))

        bsig = sig.encode()
        sig2 = Signature()
        sig2.decode(bsig)
        self.assertEqual(sig2.pubkey, sig.pubkey)
        self.assertEqual(sig2.sig, sig.sig)
        self.assertEqual(sig.algo_cls, sig2.algo_cls)


class TestSign(TestCase):
    def setUp(self):
        self.test_data = 'c6e193266883a500c6e51a117e012d96ad113d5f21f42b28eb648be92a78f92f'
        self.privkey = bytes.fromhex(self.test_data)
        self.pubkey = Secp256k1.get_pubkey(self.privkey)

    def test_sha256(self):
        sha = 'f420b28b56ce97e52adf4778a72b622c3e91115445026cf6e641459ec478dae8'
        self.assertEqual(sha, sha3(self.privkey).hexdigest())

    def test_get_pubkey(self):
        pub = '0314bf901a6640033ea07b39c6b3acb675fc0af6a6ab526f378216085a93e5c7a2'
        self.assertEqual(pub, Secp256k1.get_compressed_pubkey(self.privkey).hex())

    def test_sign_and_verify(self):
        info = sha3(bytearray([1, 2, 3, 4])).digest()
        sig = Secp256k1.sign(info, self.privkey)
        self.assertTrue(Secp256k1.verify(info, self.pubkey, sig))
        self.assertFalse(Secp256k1.verify(info, self.pubkey, bytearray([5, 6, 7, 8]*16)))
