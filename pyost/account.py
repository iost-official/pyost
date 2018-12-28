from __future__ import annotations
from base58 import b58encode, b58decode
from typing import Type, List, Dict

from pyost.api.rpc.pb import rpc_pb2 as pb
from pyost.algorithm import Algorithm, Secp256k1, Ed25519
from pyost.signature import Signature
from pyost.crc32 import parity


class Account():
    def __init__(self, seckey: bytes = None, algo: Type[Algorithm] = Ed25519):
        if seckey is None:
            seckey = algo.gen_seckey()

        if (len(seckey) != 32 and isinstance(algo, Secp256k1)) \
                or (len(seckey) != 64 and isinstance(algo, Ed25519)):
            raise ValueError('seckey length error')

        self.algorithm: Type[Algorithm] = algo
        self.seckey: bytes = seckey
        self.pubkey: bytes = algo.get_pubkey(seckey)
        self.id: bytes = get_id_by_pubkey(self.pubkey)

    def __str__(self) -> str:
        return f'Account(id={self.id} algo={self.algorithm} seckey={len(self.seckey)}b pubkey={len(self.pubkey)}b'

    def sign_tx_content(self, tx) -> None:
        tx.sign_content(self)

    def sign_tx(self, tx) -> None:
        tx.sign(self)

    def sign(self, info: bytes) -> Signature:
        return Signature(self.algorithm, info, self.seckey)


def get_id_by_pubkey(pubkey: bytes) -> bytes:
    deckey = b58decode(pubkey)
    return b'IOST' + b58encode(deckey + parity(deckey))


def get_pubkey_by_id(id: bytes) -> bytes:
    b = b58decode(id[4:])
    return b58encode(b[:-4])


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


class FrozenBalance():
    def __init__(self):
        self.amount: float = 0.0
        self.time: int = 0

    def from_raw(self, fb: pb.FrozenBalance) -> FrozenBalance:
        self.amount = fb.amount
        self.time = fb.time
        return self


class AccountInfo():
    # The message defines account pledged coin information.
    class PledgeInfo():
        def __init__(self):
            # the account who pledges
            self.pledger: str = ''
            # pledged amount
            self.amount: float = 0.0

        def from_raw(self, pi: pb.Account.PledgeInfo) -> AccountInfo.PledgeInfo:
            self.pledger = pi.pledger
            self.amount = pi.amount
            return self

    # The message defines account gas information.
    class GasInfo():
        def __init__(self):
            # current total gas amount
            self.current_total: float = 0.0
            self.transferable_gas: float = 0.0
            self.pledge_gas: float = 0.0
            # gas increase speed
            self.increase_speed: float = 0.0
            # gas limit
            self.limit: float = 0.0
            # pledge information
            self.pledged_info: List[AccountInfo.PledgeInfo] = []

        def from_raw(self, gi: pb.Account.GasInfo) -> AccountInfo.GasInfo:
            self.current_total = gi.current_total
            self.transferable_gas = gi.transferable_gas
            self.pledge_gas = gi.pledge_gas
            self.increase_speed = gi.increase_speed
            self.limit = gi.limit
            self.pledged_info = [AccountInfo.PledgeInfo().from_raw(pi)
                                 for pi in gi.pledged_info] if gi.pledged_info is not None else []
            return self

    class RAMInfo():
        def __init__(self):
            # available ram bytes
            self.available: int = 0

        def from_raw(self, ri: pb.Account.RAMInfo) -> AccountInfo.RAMInfo:
            self.available = ri.available
            return self

    # The message defines permission item.
    class Item():
        def __init__(self):
            # permission name or key pair id
            self.id: str = ''
            # whether it's a key pair
            self.is_key_pair: bool = False
            # permission weight
            self.weight: int = 0
            # permission
            self.permission: str = ''

        def from_raw(self, i: pb.Account.Item) -> AccountInfo.Item:
            self.id = i.id
            self.is_key_pair = i.is_key_pair
            self.weight = i.weight
            self.permission = i.permission
            return self

    # The message defines a permission group.
    class Group():
        def __init__(self):
            # group name
            self.name: str = ''
            # permission items
            self.items: List[AccountInfo.Item] = []

        def from_raw(self, g: pb.Account.Group) -> AccountInfo.Group:
            self.name = g.name
            self.items = [AccountInfo.Item().from_raw(item)
                          for item in p.items] if p.items is not None else []
            return self

    # The message defines the permission struct.
    class Permission():
        def __init__(self):
            # permission name
            self.name: str = ''
            # permission groups
            self.groups: List[str] = []
            # permission items
            self.items: List[AccountInfo.Item] = []
            # permission threshold
            self.threshold: int = 0

        def from_raw(self, p: pb.Account.Permission) -> AccountInfo.Permission:
            self.name = p.name
            self.groups = p.groups
            self.items = [AccountInfo.Item().from_raw(item)
                          for item in p.items] if p.items is not None else []
            self.threshold = p.threshold
            return self

    def __init__(self):
        self.name: str = ''
        self.balance: float = 0.0
        # gas information
        self.gas_info: AccountInfo.GasInfo = None
        # ram information
        self.ram_info: AccountInfo.RAMInfo = None
        # account permission
        self.permissions: Dict[str, AccountInfo.Permission] = {}
        # account groups
        self.groups: Dict[str, AccountInfo.Group] = {}
        # frozen balance information
        self.frozen_balances: List[FrozenBalance] = []

    def from_raw(self, a: pb.Account) -> AccountInfo:
        self.name = a.name
        self.balance = a.balance
        self.gas_info = AccountInfo.GasInfo().from_raw(a.gas_info)
        self.ram_info = AccountInfo.RAMInfo().from_raw(a.ram_info)
        self.permissions = {key: AccountInfo.Permission().from_raw(val)
                            for key, val in a.permissions} if a.permissions is not None else {}
        self.groups = {key: AccountInfo.Group().from_raw(val)
                       for key, val in a.groups} if a.groups is not None else {}
        self.frozen_balances = [FrozenBalance().from_raw(fb)
                                for fb in a.frozen_balances] if a.frozen_balances is not None else []
        return self
