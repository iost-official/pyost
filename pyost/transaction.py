from __future__ import annotations
import json
from typing import List, Dict
from enum import Enum
from time import time_ns
from hashlib import sha3_256 as sha3
from protobuf_to_dict import protobuf_to_dict
from pprint import pformat

from pyost.rpc.pb import rpc_pb2 as pb
from pyost.signature import Signature, KeyPair
from pyost.simplenotation import SimpleNotation


class Action:
    def __init__(self, contract: str = None, abi: str = None, *args):
        self.contract: str = contract
        self.action_name: str = abi
        nobytes_args = [arg.decode('utf-8') if isinstance(arg, bytes) else arg
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

    def to_bytes(self) -> bytes:
        sn = SimpleNotation()
        sn.write_string(self.contract)
        sn.write_string(self.action_name)
        sn.write_string(self.data)
        return sn.to_bytes()


class AmountLimit:
    def __init__(self, token: str = '', value: str = ''):
        self.token: str = token
        self.value: str = value

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

    def to_bytes(self) -> bytes:
        sn = SimpleNotation()
        sn.write_string(self.token)
        sn.write_string(self.value)
        return sn.to_bytes()


class Transaction:
    class Status(Enum):
        PENDING = pb.TransactionResponse.PENDING
        PACKED = pb.TransactionResponse.PACKED
        IRREVERSIBLE = pb.TransactionResponse.IRREVERSIBLE
        UNKNOWN = -1

    def __init__(self, expiration: int = 90, delay: int = 0,
                 gas_ratio: float = 1.0, gas_limit: float = 10000.0,
                 amount_limits: List[AmountLimit] = None, actions: List[Action] = None,
                 signers: List[str] = None, publisher: str = ''):
        self.hash: bytes = None
        self.time: int = time_ns()
        self.expiration: int = 0
        self.set_expiration(expiration)
        self.gas_ratio: float = gas_ratio
        self.gas_limit: float = gas_limit
        self.delay: int = delay
        self.actions: List[Action] = actions or []
        self.amount_limits: List[AmountLimit] = amount_limits or []
        self.signers: List[str] = signers or []
        self.signatures: List[Signature] = []
        self.publisher: str = publisher
        self.publisher_signatures: List[Signature] = []
        self.referred_tx: bytes = b''
        self.tx_receipt: TxReceipt = None
        self.status: Transaction.Status = Transaction.Status.UNKNOWN

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_request_raw()))

    def add_action(self, contract: str, abi: str, *args) -> Transaction:
        self.actions.append(Action(contract, abi, *args))
        return self

    def add_signer(self, name: str, permission: str) -> Transaction:
        self.signers.append(f'{name}@{permission}')
        return self

    def add_amount_limit(self, token: str = '*', amount: str = 'unlimited') -> Transaction:
        self.amount_limits.append(AmountLimit(token, amount))
        return self

    def set_expiration(self, expiration: int) -> Transaction:
        self.expiration = self.time + expiration * int(1e9)
        return self

    def add_signature(self, kp: KeyPair) -> Transaction:
        signature = kp.sign(self._base_hash())
        self.signatures.append(signature)
        return self

    def add_publisher_signature(self, name: str, kp: KeyPair) -> Transaction:
        signature = kp.sign(self._publish_hash())
        self.publisher_signatures.append(signature)
        self.publisher = name
        self.hash = None
        return self

    def _base_hash(self) -> bytes:
        return sha3(self.to_bytes('base')).digest()

    def _publish_hash(self) -> bytes:
        return sha3(self.to_bytes('publish')).digest()

    def _hash(self) -> bytes:
        self.hash = sha3(self.to_bytes('full')).digest()
        return self.hash

    def from_raw(self, tr: pb.Transaction) -> Transaction:
        self.hash = tr.hash
        self.time = tr.time
        self.expiration = tr.expiration
        self.gas_ratio = tr.gas_ratio
        self.gas_limit = tr.gas_limit
        self.delay = tr.delay
        self.actions = [Action().from_raw(ar) for ar in tr.actions
                        ] if tr.actions is not None else []
        self.amount_limits: [AmountLimit().from_raw(al) for al in tr.amount_limit
                             ] if tr.amount_limit is not None else []
        self.signers = tr.signers
        self.signatures = []
        self.publisher = tr.publisher
        self.publisher_signatures = []
        self.referred_tx = tr.referred_tx
        self.tx_receipt = TxReceipt().from_raw(tr.tx_receipt)
        return self

    def to_request_raw(self) -> pb.TransactionRequest:
        return pb.TransactionRequest(
            time=self.time,
            expiration=self.expiration,
            gas_ratio=self.gas_ratio,
            gas_limit=self.gas_limit,
            delay=self.delay,
            actions=[a.to_raw() for a in self.actions],
            amount_limit=[al.to_raw() for al in self.amount_limits],
            signers=self.signers,
            signatures=[s.to_raw() for s in self.signatures],
            publisher=self.publisher,
            publisher_sigs=[s.to_raw() for s in self.publisher_signatures],
        )

    def to_raw(self) -> pb.Transaction:
        return pb.Transaction(
            hash=self.hash,
            time=self.time,
            expiration=self.expiration,
            gas_ratio=self.gas_ratio,
            gas_limit=self.gas_limit,
            delay=self.delay,
            actions=[a.to_raw() for a in self.actions],
            amount_limit=[al.to_raw() for al in self.amount_limits],
            signers=self.signers,
            publisher=self.publisher,
            referred_tx=self.referred_tx
        )

    def decode(self, data: bytes) -> None:
        tr = pb.Transaction()
        tr.ParseFromString(data)
        self.from_raw(tr)

    def encode(self) -> bytes:
        return self.to_raw().SerializeToString()

    def to_bytes(self, level='base') -> bytes:
        sn = SimpleNotation()
        sn.write_int64(self.time)
        sn.write_int64(self.expiration)
        sn.write_int64(int(self.gas_ratio * 100.0))
        sn.write_int64(int(self.gas_limit * 100.0))
        sn.write_int64(self.delay)
        sn.write_string_slice(self.signers)
        sn.write_bytes_slice([a.to_bytes() for a in self.actions], False)
        sn.write_bytes_slice([a.to_bytes() for a in self.amount_limits], False)
        if level == 'publish' or level == 'full':
            sn.write_bytes_slice([s.to_bytes() for s in self.signatures], False)
        if level == 'full':
            sn.write_bytes(self.referred_tx)
            sn.write_string(self.publisher)
            sn.write_bytes_slice([s.to_bytes() for s in self.publisher_signatures], False)
        return sn.to_bytes()

    # def verify_self(self) -> bool:
    #     base_hash = self._base_hash()
    #     has_signed: List[str] = []
    #
    #     for sign in self.signs:
    #         if not sign.verify(base_hash):
    #             raise PermissionError('A signature did not sign the base hash.')
    #         has_signed.append(sign.pubkey)
    #
    #     for signer in self.signers:
    #         if signer not in has_signed:
    #             raise PermissionError('A required signer has not signed yet.')
    #
    #     if self.publisher is None:
    #         raise PermissionError('A publisher is required.')
    #     # if not self.publisher.verify(self._publish_hash()):
    #     #    raise PermissionError('The publisher has not signed yet.')
    #
    #     return True


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

    def is_success(self) -> bool:
        return self.status_code == TxReceipt.StatusCode.SUCCESS

    def from_raw(self, tr: pb.TxReceipt) -> TxReceipt:
        self.tx_hash = tr.tx_hash
        self.gas_usage = tr.gas_usage
        self.ram_usage = tr.ram_usage
        self.status_code = TxReceipt.StatusCode(tr.status_code)
        self.message = tr.message
        self.returns = tr.returns
        self.receipts = [TxReceipt.Receipt().from_raw(r) for r in tr.receipts
                         ] if tr.receipts is not None else []
        return self

    def to_raw(self) -> pb.TxReceipt:
        return pb.TxReceipt(
            tx_hash=self.tx_hash,
            gas_usage=self.gas_usage,
            ram_usage=self.ram_usage,
            status_code=self.status_code.value,
            message=self.message,
            returns=self.returns,
            receipts=[r.to_raw() for r in self.receipts]
        )


class TransactionError(Exception):
    def __init__(self, message: str = 'Unknown transaction error.',
                 receipt: TxReceipt = None):
        super().__init__(message)
        self.receipt: TxReceipt = receipt
        self.status_code: TxReceipt.StatusCode = receipt.status_code if receipt is not None else TxReceipt.StatusCode.UNKNOWN_ERROR
