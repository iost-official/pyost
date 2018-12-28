from __future__ import annotations
import json
from typing import List, Dict
from enum import Enum
from time import time_ns
from hashlib import sha3_256 as sha3
from protobuf_to_dict import protobuf_to_dict
from base58 import b58encode, b58decode

from pyost.api.rpc.pb import rpc_pb2 as pb
from pyost.signature import Signature
from pyost.account import Account


class Action():
    # message ActionRaw {
    #     string contract = 1;
    #     string actionName = 2;
    #     string data = 3;
    # }
    #
    def __init__(self, contract: str = None, abi: str = None, *args):
        self.contract: str = contract
        self.action_name: str = abi
        nobytes_args = [arg.decode('latin1') if isinstance(arg, bytes) else arg
                        for arg in args]
        self.data: str = json.dumps(nobytes_args)

    def __str__(self) -> str:
        return protobuf_to_dict(self.to_raw())
        # return f'Action(contract={self.contract} name={self.name} data={self.data}'

    def to_raw(self) -> pb.Action:
        return pb.Action(
            contract=self.contract,
            action_name=self.action_name,
            data=self.data)

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def from_raw(self, ar: pb.Action) -> Action:
        self.contract = ar.contract
        self.action_name = ar.action_name
        self.data = ar.data
        return self

    def decode(self, data: bytes) -> Action:
        ar = pb.Action()
        ar.ParseFromString(data)
        return self.from_raw(ar)


class AmountLimit():
    def __int__(self):
        self.token: str = ''
        self.value: float = 0.0

    def from_raw(self, al: pb.AmountLimit) -> AmountLimit:
        self.token = al.token
        self.value = al.value
        return self


class Transaction():
    class Status(Enum):
        PENDIND = pb.TransactionResponse.PENDING
        PACKED = pb.TransactionResponse.PACKED
        IRREVERSIBLE = pb.TransactionResponse.IRREVERSIBLE

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
    def __init__(self, actions: List[Action] = None, signers: List[str] = None,
                 expiration: int = 90, gas_ratio: float = 1, gas_limit: float = 10000,
                 delay: int = 0):
        self.status: Transaction.Status = None
        self._hash: str = None
        self.time: int = time_ns()
        self.expiration: int = self.time + expiration * 1000000000
        self.gas_ratio: float = gas_ratio
        self.gas_limit: float = gas_limit
        self.delay: int = delay
        self.actions: List[Action] = actions if actions is not None else []
        self.signers: List[str] = signers if signers is not None else []
        self.signs: List[Signature] = []
        self.publisher: str = None
        self.referred_tx: str = None
        self.amount_limit: List[AmountLimit] = []
        self.tx_receipt: TxReceipt = None

    def __str__(self):
        return str(protobuf_to_dict(self.to_raw()))

    def add_action(self, contract: str, abi: str, *args) -> Transaction:
        self.actions.append(Action(contract, abi, *args))
        return self

    def add_signer(self, pubkey: bytes) -> Transaction:
        self.signers.append(pubkey)
        return self

    def _contain_signer(self, pubkey: bytes) -> bool:
        return pubkey in self.signers

    def _base_hash(self) -> bytes:
        tr = self.to_raw(no_signs=True, no_publisher=True)
        return sha3(tr.SerializeToString()).digest()

    def _publish_hash(self) -> bytes:
        tr = self.to_raw(no_publisher=True)
        return sha3(tr.SerializeToString()).digest()

    def to_raw(self, no_signs: bool = False, no_publisher: bool = False) -> pb.Transaction:
        return pb.Transaction(
            time=self.time,
            expiration=self.expiration,
            gas_ratio=self.gas_ratio,
            gas_limit=self.gas_limit,
            delay=self.delay,
            actions=[action.to_raw() for action in self.actions if
                     action is not None] if self.actions is not None else [],
            signers=[b58decode(signer) for signer in self.signers if
                     signer is not None] if self.signers is not None else [],
            signs=[sign.to_raw() for sign in self.signs if sign is not None] if not no_signs else [],
            publisher=self.publisher if not no_publisher else None
        )

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def from_raw(self, tr: pb.Transaction, status: Status = None) -> Transaction:
        self.status = status
        self._hash = None
        self.time = tr.time
        self.expiration = tr.expiration
        self.gas_ratio = tr.gas_ratio
        self.gas_limit = tr.gas_limit
        self.delay = tr.delay
        self.actions = [Action().from_raw(ar) for ar in tr.actions] if tr.actions is not None else []
        self.signers = [b58encode(signer) for signer in tr.signers] if tr.signers is not None else []
        self.signs = [Signature().from_raw(sr) for sr in tr.signs] if tr.signs is not None else []
        self.publisher = tr.publisher
        return self

    def decode(self, data: bytes) -> Transaction:
        tr = pb.Transaction()
        tr.ParseFromString(data)
        return self.from_raw(tr)

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

    def sign_content(self, account: Account) -> Transaction:
        if not self._contain_signer(account.pubkey):
            raise PermissionError('This account is not in the signers list.')

        sig = account.sign(self._base_hash())
        assert self.verify_signer(sig), 'The signature is invalid.'

        self.signs.append(sig)
        return self

    def sign(self, account: Account) -> Transaction:
        self.publisher = account.sign(self._publish_hash())
        self._hash = None
        return self


def sign_tx_content(tx: Transaction, account: Account) -> Signature:
    if not tx._contain_signer(account.pubkey):
        raise PermissionError('This account is not in the transaction\'s signers list.')
    return account.sign(tx._base_hash())


def sign_tx(tx: Transaction, account: Account, *signs: Signature) -> Transaction:
    tx.signs = [*tx.signs, *signs]
    tx.publisher = account.sign(tx._publish_hash())
    tx.hash = None
    return tx


class TxReceipt():
    class StatusCode(Enum):
        SUCCESS = pb.TxReceipt.SUCCESS
        GAS_RUN_OUT = pb.TxReceipt.GAS_RUN_OUT
        BALANCE_NOT_ENOUGH = pb.TxReceipt.BALANCE_NOT_ENOUGH
        WRONG_PARAMETER = pb.TxReceipt.WRONG_PARAMETER
        RUNTIME_ERROR = pb.TxReceipt.RUNTIME_ERROR
        TIMEOUT = pb.TxReceipt.TIMEOUT
        WRONG_TX_FORMAT = pb.TxReceipt.WRONG_TX_FORMAT
        DUPLICATE_SET_CODE = pb.TxReceipt.DUPLICATE_SET_CODE
        UNKNOWN_ERROR = pb.TxReceipt.UNKNOWN_ERROR

    class Receipt():
        def __int__(self):
            self.func_name: str = ''
            self.content: str = ''

        def from_raw(self, receipt: pb.TxReceipt.Receipt) -> TxReceipt.Receipt:
            self.func_name = receipt.func_name
            self.content = receipt.content
            return self

    def __int__(self):
        self.tx_hash: str = ''
        self.gas_usage: float = 0.0
        self.ram_usage: Dict[str, int] = {}
        self.status_code: TxReceipt.StatusCode = TxReceipt.StatusCode.UNKNOWN_ERROR
        self.message: str = ''
        self.returns: List[str] = []
        self.receipts: List[TxReceipt.Receipt] = []

    def from_raw(self, tr: pb.TxReceipt) -> TxReceipt:
        self.tx_hash = tr.tx_hash
        self.gas_usage = tr.gas_usage
        self.ram_usage = tr.ram_usage
        self.status_code = tr.status_code
        self.message = tr.message
        self.returns = tr.returns
        self.receipts = tr.receipts
        return self


if __name__ == '__main__':
    receipt = TxReceipt()
    print(TxReceipt.StatusCode.BALANCE_NOT_ENOUGH.value)
    # tr = pb.Transaction(time=time_ns(), actions=[pb.Action(), pb.Action()],
    #            publisher=pb.Signature(algorithm=1, sig=b'ddfadsgadg'))
    # s = tr.SerializeToString()
    # print(tr)
    # newtr = pb.Transaction()
    # newtr.ParseFromString(s)
    # print(newtr)
