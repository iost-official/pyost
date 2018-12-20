from base58 import b58encode, b58decode
from typing import Type

from pyost.algorithm import Algorithm, Secp256k1, Ed25519
from pyost.signature import Signature
from pyost.crc32 import parity


class Account():
    def __init__(self, seckey: bytes or None, algo: Type[Algorithm] = Ed25519):
        if seckey is None:
            seckey = algo.gen_seckey()

        if (len(seckey) != 32 and isinstance(algo, Secp256k1)) \
                or (len(seckey) != 64 and isinstance(algo, Ed25519)):
            raise ValueError('seckey length error')

        self.algorithm: Type[Algorithm] = algo
        self.seckey: bytes = seckey
        self.pubkey: bytes = algo.get_pubkey(seckey)
        self.id: str = get_id_by_pubkey(self.pubkey)

    def sign(self, info: bytes) -> Signature:
        return Signature(self.algorithm, info, self.seckey)


def get_id_by_pubkey(pubkey: bytes) -> str:
    return 'IOST' + b58encode(pubkey + parity(pubkey)).hex()


def get_pubkey_by_id(id: str) -> bytes:
    b = b58decode(id[4:])
    return b[:-4]

# class Account():
#     def __init__(self, id):
#         self._id = id
#         self._key_id = {}
#         self._key_pair = {}
#
#     def add_key_pair(self, kp, permission=''):
#         if permission == '':
#             if kp.id not in self._key_id:
#                 raise KeyError(f'Key {kp.id} does not exist.')
#             permission = self._key_id[kp.id]
#         self._key_pair[permission] = kp
#
#     def get_id(self):
#         return self._id
#
#     def get_key_pair(self, permission):
#         return self._key_pair[permission]
#
#     def sign(self, tx, permission):
#         tx.add_sign(self._key_pair[permission])
#
#     def sign_tx(self, tx):
#         tx.add_publish_sign(self._id, self._key_pair['active'])
