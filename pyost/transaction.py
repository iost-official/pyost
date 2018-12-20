from typing import List, Dict
from time import time_ns
from hashlib import sha3_256 as sha3
from protobuf_to_dict import protobuf_to_dict

from pyost.api.core.tx.tx_pb2 import TxRaw, ActionRaw
from pyost.api.crypto.signature_pb2 import SignatureRaw
from pyost.signature import Signature
from pyost.account import Account


class Action():
    # message ActionRaw {
    #     string contract = 1;
    #     string actionName = 2;
    #     string data = 3;
    # }
    #
    def __init__(self, contract: str = None, action_name: str = None, data: str = None):
        self.contract: str = contract
        self.action_name: str = action_name
        self.data: str = data

    def __str__(self) -> str:
        return protobuf_to_dict(self.to_raw())
        # return f'Action(contract={self.contract} name={self.name} data={self.data}'

    def to_raw(self) -> ActionRaw:
        return ActionRaw(
            contract=self.contract,
            actionName=self.action_name,
            data=self.data)

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def from_raw(self, ar: ActionRaw) -> None:
        self.contract = ar.contract
        self.action_name = ar.actionName
        self.data = ar.data

    def decode(self, data: bytes) -> None:
        ar = ActionRaw()
        ar.ParseFromString(data)
        self.from_raw(ar)


class Transaction():
    # message TxRaw {
    #     int64 time = 1;
    #     int64 expiration = 2;
    #     int64 gasLimit = 3;
    #     int64 gasPrice = 4;
    #     repeated ActionRaw actions = 5;
    #     repeated bytes signers = 6;
    #     repeated crypto.SignatureRaw signs = 7;
    #     crypto.SignatureRaw publisher = 8;
    # }
    def __init__(self, actions: List[Action] = None, signers: List[bytes] = None,
                 gas_limit: int = 1000, gas_price: int = 1, expiration: int = 0):
        self._hash: bytes = None
        self.time: int = time_ns()
        self.expiration: int = expiration
        self.gas_limit: int = gas_limit
        self.gas_price: int = gas_price
        self.actions: List[Action] = actions
        self.signers: List[bytes] = signers
        self.signs: List[Signature] = []
        self.publisher: Signature = None

    def __str__(self):
        return str(protobuf_to_dict(self.to_raw()))

    def _contain_signer(self, pubkey: bytes) -> bool:
        return pubkey in self.signers

    def _base_hash(self) -> bytes:
        tr = self.to_raw(no_signs=True, no_publisher=True)
        return sha3(tr.SerializeToString()).digest()

    def _publish_hash(self) -> bytes:
        tr = self.to_raw(no_publisher=True)
        return sha3(tr.SerializeToString()).digest()

    def to_raw(self, no_signs: bool = False, no_publisher: bool = False) -> TxRaw:
        return TxRaw(
            time=self.time,
            expiration=self.expiration,
            gasLimit=self.gas_limit,
            gasPrice=self.gas_price,
            actions=[action.to_raw() for action in self.actions],
            signers=self.signers,
            signs=[] if no_signs else [sign.to_raw() for sign in self.signs],
            publisher=None if no_publisher or self.publisher is None
            else self.publisher.to_raw())

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def from_raw(self, tr: TxRaw) -> None:
        self._hash = None
        self.time = tr.time
        self.expiration = tr.expiration
        self.gas_limit = tr.gas_limit
        self.gas_price = tr.gas_price
        self.actions = [Action().from_raw(ar) for ar in tr.actions]
        self.signers = tr.signers
        self.signs = [Signature().from_raw(sr) for sr in tr.signs]
        self.publisher = Signature().from_raw(tr.publisher) if tr.publisher is not None else None

    def decode(self, data: bytes) -> None:
        tr = TxRaw()
        tr.ParseFromString(data)
        self.from_raw(tr)

    def hash(self) -> bytes:
        if self._hash is None:
            self._hash = sha3(self.encode()).digest()
        return self._hash

    def verify_self(self) -> bool:
        base_hash = self._base_hash()
        has_signed: List[bytes] = []

        for sign in self.signs:
            if not sign.verify(base_hash):
                raise PermissionError('A signature did not sign the base hash.')
            has_signed.append(sign.pubkey)

        for signer in self.signers:
            if signer not in has_signed:
                raise PermissionError('A required signer has not signed yet.')

        if self.publisher is None:
            raise PermissionError('A publisher is required.')
        if not self.publisher.verify(self._publish_hash()):
            raise PermissionError('The publisher has not signed yet.')

        return True

    def verify_signer(self, sig: Signature) -> bool:
        return sig.verify(self._base_hash())


def sign_tx_content(tx: Transaction, account: Account) -> Signature:
    if not tx._contain_signer(account.pubkey):
        raise PermissionError('This account is not in the transaction\'s signers list.')
    return account.sign(tx._base_hash())


def sign_tx(tx: Transaction, account: Account, *signs: Signature) -> Transaction:
    tx.signs = [*tx.signs, *signs]
    tx.publisher = account.sign(tx._publish_hash())
    tx.hash = None
    return tx


if __name__ == '__main__':
    tr = TxRaw(time=time_ns(), actions=[ActionRaw(), ActionRaw()],
               publisher=SignatureRaw(algorithm=1, sig=b'ddfadsgadg'))
    s = tr.SerializeToString()
    print(tr)
    newtr = TxRaw()
    newtr.ParseFromString(s)
    print(newtr)
