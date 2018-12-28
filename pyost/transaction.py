from __future__ import annotations
import json
from typing import List, Dict
from enum import Enum
from time import time_ns
from hashlib import sha3_256 as sha3
from protobuf_to_dict import protobuf_to_dict
from base58 import b58encode, b58decode
from pprint import pformat

from pyost.api.rpc.pb import rpc_pb2 as pb
from pyost.signature import Signature
import pyost.account


class Action:
    def __init__(self, contract: str = None, abi: str = None, *args):
        self.contract: str = contract
        self.action_name: str = abi
        nobytes_args = [arg.decode('latin1') if isinstance(arg, bytes) else arg
                        for arg in args]
        self.data: str = json.dumps(nobytes_args)

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, ar: pb.Action) -> Action:
        self.contract = ar.contract
        self.action_name = ar.action_name
        self.data = ar.data
        return self

    def to_raw(self) -> pb.Action:
        return pb.Action(
            contract=self.contract,
            action_name=self.action_name,
            data=self.data)


class AmountLimit:
    def __init__(self):
        self.token: str = ''
        self.value: float = 0.0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, al: pb.AmountLimit) -> AmountLimit:
        self.token = al.token
        self.value = al.value
        return self

    def to_raw(self) -> pb.AmountLimit:
        return pb.AmountLimit(
            token=self.token,
            value=self.value,
        )


class Transaction:
    class Status(Enum):
        PENDING = pb.TransactionResponse.PENDIND
        PACKED = pb.TransactionResponse.PACKED
        IRREVERSIBLE = pb.TransactionResponse.IRREVERSIBLE

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
        self.amount_limit: List[AmountLimit] = []
        self.signers: List[str] = signers if signers is not None else []
        self.signs: List[Signature] = []
        self.publisher: str = None
        self.publisher_signs: List[Signature] = []
        self.referred_tx: str = None
        self.tx_receipt: TxReceipt = None

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def add_action(self, contract: str, abi: str, *args) -> Transaction:
        self.actions.append(Action(contract, abi, *args))
        return self

    def add_signer(self, pubkey: str) -> Transaction:
        self.signers.append(pubkey)
        return self

    def _base_hash(self) -> str:
        tr = self.to_raw(no_signs=True, no_publisher=True)
        return sha3(tr.SerializeToString()).digest()

    def _publish_hash(self) -> str:
        tr = self.to_raw(no_publisher=True)
        return sha3(tr.SerializeToString()).digest()

    def from_raw(self, tr: pb.Transaction, status: Status = None) -> Transaction:
        self.status = status
        self._hash = tr.hash
        self.time = tr.time
        self.expiration = tr.expiration
        self.gas_ratio = tr.gas_ratio
        self.gas_limit = tr.gas_limit
        self.delay = tr.delay
        self.actions = [Action().from_raw(ar) for ar in tr.actions
                        ] if tr.actions is not None else []
        self.amount_limit: [AmountLimit().from_raw(al) for al in tr.amount_limit
                            ] if tr.amount_limit is not None else []
        self.signers = [b58encode(signer) for signer in tr.signers
                        ] if tr.signers is not None else []
        self.signs = []
        self.publisher = tr.publisher
        self.publisher_signs = []
        self.referred_tx = tr.referred_fx
        self.tx_receipt = TxReceipt().from_raw(tr.tx_receipt)
        return self

    def to_raw(self, no_signs: bool = False, no_publisher: bool = False) -> pb.TransactionRequest:
        return pb.TransactionRequest(
            time=self.time,
            expiration=self.expiration,
            gas_ratio=self.gas_ratio,
            gas_limit=self.gas_limit,
            delay=self.delay,
            actions=[a.to_raw() for a in self.actions
                     ] if self.actions is not None else [],
            amount_limit=[al.to_raw() for al in self.amount_limit
                          ] if self.amount_limit is not None else [],
            signers=[b58decode(s) for s in self.signers
                     ] if self.signers is not None else [],
            signatures=[s.to_raw() for s in self.signs
                        ] if not no_signs and self.signs is not None else [],
            publisher=self.publisher if not no_publisher else None,
            # publisher_sigs=[s.to_raw() for s in self.publisher_sigs
            #                ] if not no_publisher and self.publisher_sigs is not None else []
        )

    def hash(self) -> str:
        if self._hash is None:
            self._hash = sha3(self.to_raw().SerializeToString()).digest()
        return self._hash

    def verify_self(self) -> bool:
        base_hash = self._base_hash()
        has_signed: List[str] = []

        for sign in self.signs:
            if not sign.verify(base_hash):
                raise PermissionError('A signature did not sign the base hash.')
            has_signed.append(sign.pubkey)

        for signer in self.signers:
            if signer not in has_signed:
                raise PermissionError('A required signer has not signed yet.')

        if self.publisher is None:
            raise PermissionError('A publisher is required.')
        # if not self.publisher.verify(self._publish_hash()):
        #    raise PermissionError('The publisher has not signed yet.')

        return True

    def verify_signer(self, sig: Signature) -> bool:
        return sig.verify(self._base_hash())

    def add_sign(self, account: pyost.account.Account) -> Transaction:
        if account.pubkey not in self.signers:
            raise PermissionError('This account is not in the signers list.')

        sig = account.sign(self._base_hash())
        assert self.verify_signer(sig), 'The signature is invalid.'

        self.signs.append(sig)
        return self

    def add_publisher_sign(self, account: pyost.account.Account) -> Transaction:
        sig = account.sign(self._publish_hash())
        assert self.verify_signer(sig), 'The signature is invalid.'

        self.publisher_signs.append(account.sign(self._publish_hash()))
        self.publisher = account.id
        self._hash = None
        return self


class TxReceipt:
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

    class Receipt:
        def __init__(self):
            self.func_name: str = ''
            self.content: str = ''

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, tr: pb.TxReceipt.Receipt) -> TxReceipt.Receipt:
            self.func_name = tr.func_name
            self.content = tr.content
            return self

        def to_raw(self) -> pb.TxReceipt.Receipt:
            return pb.TxReceipt.Receipt(
                func_name=self.func_name,
                content=self.content
            )

    def __init__(self):
        self.tx_hash: str = ''
        self.gas_usage: float = 0.0
        self.ram_usage: Dict[str, int] = {}
        self.status_code: TxReceipt.StatusCode = TxReceipt.StatusCode.UNKNOWN_ERROR
        self.message: str = ''
        self.returns: List[str] = []
        self.receipts: List[TxReceipt.Receipt] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, tr: pb.TxReceipt) -> TxReceipt:
        self.tx_hash = tr.tx_hash
        self.gas_usage = tr.gas_usage
        self.ram_usage = tr.ram_usage
        self.status_code = tr.status_code
        self.message = tr.message
        self.returns = tr.returns
        self.receipts = [TxReceipt.Receipt().from_raw(r) for r in tr.receipts]
        return self

    def to_raw(self) -> pb.TxReceipt:
        return pb.TxReceipt(
            tx_hash=self.tx_hash,
            gas_usage=self.gas_usage,
            ram_usage=self.ram_usage,
            status_code=self.status_code,
            message=self.message,
            returns=self.returns,
            receipts=[r.to_raw() for r in self.receipts] if self.receipts is not None else []
        )


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
