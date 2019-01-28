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
from pyost.simpleencoder import SimpleEncoder


class Action:
    """Describes a call to an ABI function.

    Args:
        contract: The contract id to call.
        abi: The name of the function to call.
        *args: The list of arguments to pass to the function.

    Attributes:
        contract: The contract id to call.
        abi: The name of the function to call.
        data: A JSONified string of the arguments list.
    """

    def __init__(self, contract: str = None, abi: str = None, *args):
        self.contract: str = contract
        self.action_name: str = abi
        nobytes_args = [arg.decode('utf-8') if isinstance(arg, bytes) else arg
                        for arg in args]
        self.data: str = json.dumps(nobytes_args)

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, ar: pb.Action) -> Action:
        """Deserializes a protobuf object to update this object's members.

        Args:
            ar: The protobuf object.

        Returns:
            Itself.
        """
        self.contract = ar.contract
        self.action_name = ar.action_name
        self.data = ar.data
        return self

    def to_raw(self) -> pb.Action:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.Action(
            contract=self.contract,
            action_name=self.action_name,
            data=self.data)

    def to_bytes(self) -> bytes:
        """Serializes this object to bytes, used to calculate the hash of a `Transaction`.

        Returns:
            A binary representation of this object.
        """
        se = SimpleEncoder()
        se.write_string(self.contract)
        se.write_string(self.action_name)
        se.write_string(self.data)
        return se.to_bytes()


class AmountLimit:
    """Describes the amount limit for a given token.

    Args:
        token: The token name.
        value: The amount limit as a string, ``unlimited`` is a valid value.

    Attributes:
        token: The token name.
        value: The amount limit as a string, ``unlimited`` is a valid value.
    """

    def __init__(self, token: str = '', value: str = ''):
        self.token: str = token
        self.value: str = value

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, al: pb.AmountLimit) -> AmountLimit:
        """Deserializes a protobuf object to update this object's members.

        Args:
            al: The protobuf object.

        Returns:
            Itself.
        """
        self.token = al.token
        self.value = al.value
        return self

    def to_raw(self) -> pb.AmountLimit:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.AmountLimit(
            token=self.token,
            value=self.value,
        )

    def to_bytes(self) -> bytes:
        """Serializes this object to bytes, used to calculate the hash of a `Transaction`.

        Returns:
            A binary representation of this object.
        """
        se = SimpleEncoder()
        se.write_string(self.token)
        se.write_string(self.value)
        return se.to_bytes()


class Transaction:
    """Describes a transaction.
    Normal usage is to add `Action`s (ABI calls) and `Signature`s (from the signers and publisher)
    then send it via the blockchain's API by calling `IOST.send_tx` method.

    Args:
        expiration: When the transaction expires, in seconds from now.
        delay: When to execute the transaction, default 0 means now.
        gas_ratio: The gas ratio, default is 1.0.
        gas_limit: The maximum amount of gas that can be used to execute a transaction.
        amount_limits: A list of `AmountLimit` to set the maximum amount by token.
        actions: A list of `Action`, i.e. ABI calls.
        signers: A list of signers' name and permission written in the format ``name@permission``.
        publisher: The name of the publisher's account.
        chain_id: The chain id.

    Attributes:
        hash: The binary hash of the full transaction including publisher's signature.
        time: The time in nanoseconds when the `Transaction` object was created.
        expiration: When the transaction expires, in seconds from now.
        delay: When to execute the transaction, default 0 means now.
        gas_ratio: The gas ratio, default is 1.0.
        gas_limit: The maximum amount of gas that can be used to execute a transaction.
        amount_limits: A list of `AmountLimit` to set the maximum amount by token.
        actions: A list of `Action`, i.e. ABI calls.
        signers: A list of signers' name and permission written in the format ``name@permission``.
        signatures: A list of `Signature` corresponding to the list of `signers`.
        publisher: The name of the publisher's account.
        publisher_signatures: A list of `Signature` added by the `publisher`.
        chain_id: The chain id.
        referred_tx: The binary hash of the referred transaction.
        tx_receipt: The receipt of the `Transaction` as a `TxReceipt` object.
        status: The status of the `Transaction` such as ``PENDING`` or ``PACKED``.
    """

    class Status(Enum):
        """Status of the `Transaction`."""
        PENDING = pb.TransactionResponse.PENDING  #: Transaction pending.
        PACKED = pb.TransactionResponse.PACKED  #: Transaction packed in a block.
        IRREVERSIBLE = pb.TransactionResponse.IRREVERSIBLE  #: Transaction has been processed.
        UNKNOWN = -1  #: Unknown status.

    def __init__(self, expiration: int = 90, delay: int = 0,
                 gas_ratio: float = 1.0, gas_limit: float = 10000.0,
                 amount_limits: List[AmountLimit] = None, actions: List[Action] = None,
                 signers: List[str] = None, publisher: str = '', chain_id: int = 1024):
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
        self.chain_id: int = chain_id
        self.referred_tx: bytes = b''
        self.tx_receipt: TxReceipt = None
        self.status: Transaction.Status = Transaction.Status.UNKNOWN

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_request_raw()))

    def add_action(self, contract: str, abi: str, *args) -> Transaction:
        """Adds an `Action` (i.e. an ABI call) to the list of `Action`.

        Args:
            contract: The contract id to call.
            abi: The name of the function to call.
            *args: The list of arguments to pass to the function.

        Returns:
            Itself.
        """
        self.actions.append(Action(contract, abi, *args))
        return self

    def add_signer(self, name: str, permission: str) -> Transaction:
        """Adds a signer's name and permission to the list of `signers` in the format ``name@permission``.

        Args:
            name: The name of the signer.
            permission: The permission such as ``active`` or ``owner``.

        Returns:
            Itself.
        """
        self.signers.append(f'{name}@{permission}')
        return self

    def add_amount_limit(self, token: str = '*', amount: str = 'unlimited') -> Transaction:
        """Adds an `AmountLimit` to the list of `AmountLimit`.

        Args:
            token: The token name.
            amount: The amount limit as a string, ``unlimited`` is a valid value.

        Returns:
            Itself.
        """
        self.amount_limits.append(AmountLimit(token, amount))
        return self

    def set_expiration(self, expiration: int) -> Transaction:
        """Sets the expiration time in seconds from the `time` field.

        Args:
            expiration: Number of seconds since the `time` of this `Transaction`.

        Returns:
            Itself.
        """
        self.expiration = self.time + expiration * int(1e9)
        return self

    def add_signature(self, kp: KeyPair) -> Transaction:
        """Signs the base hash of the `Transaction` and adds the `Signature` to the list of `signatures`.

        Args:
            kp: The `KeyPair` used to sign the base hash of this `Transaction`.

        Returns:
            Itself.
        """
        signature = kp.sign(self._base_hash())
        self.signatures.append(signature)
        return self

    def add_publisher_signature(self, name: str, kp: KeyPair) -> Transaction:
        """Signs the publish hash of the `Transaction` and adds the `Signature` to the list of `publisher_signatures`.
        The publish hash includes the list of `signers` and their `signatures`.

        Args:
            name: The name of the publisher, will set the `publisher` field with its value.
            kp: The `KeyPair` used to sign the publish hash of this `Transaction`.

        Returns:
            Itself.
        """
        signature = kp.sign(self._publish_hash())
        self.publisher_signatures.append(signature)
        self.publisher = name
        self.hash = None
        return self

    def _base_hash(self) -> bytes:
        """Calculates the base hash of this `Transaction`.

        Returns:
            A binary hash value.
        """
        return sha3(self.to_bytes('base')).digest()

    def _publish_hash(self) -> bytes:
        """Calculates the publish hash of this `Transaction` (includes `signers` and `signatures`).

        Returns:
            A binary hash value.
        """
        return sha3(self.to_bytes('publish')).digest()

    def _hash(self) -> bytes:
        """Calculates the full hash of this `Transaction` (includes `publisher` and `publisher_signatures`).

        Returns:
            A binary hash value.
        """
        self.hash = sha3(self.to_bytes('full')).digest()
        return self.hash

    def from_raw(self, tr: pb.Transaction) -> Transaction:
        """Deserializes a protobuf object to update this object's members.

        Args:
            tr: The protobuf object.

        Returns:
            Itself.
        """
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
        self.chain_id = tr.chain_id
        self.referred_tx = tr.referred_tx
        self.tx_receipt = TxReceipt().from_raw(tr.tx_receipt)
        return self

    def to_request_raw(self) -> pb.TransactionRequest:
        """Serializes this object's members to a protobuf object.
        This is used by IOST.send_tx to send the `TransactionRequest` via the API.

        Returns:
            A protobuf object.
        """
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
            chain_id=self.chain_id,
        )

    def to_raw(self) -> pb.Transaction:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
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
            referred_tx=self.referred_tx,
            chain_id=self.chain_id,
        )

    def to_bytes(self, level='base') -> bytes:
        """Serializes this object to bytes, used to calculate the hash of a `Transaction`.

        Args:
            level: If ``base``, only calculates the base hash of the `Transaction`.
                If ``publish``, also includes the list of `signatures`.
                If ``full``, also includes the `publisher` and its `publisher_signatures`.

        Returns:
            A binary representation of this object.
        """
        se = SimpleEncoder()
        se.write_int64(self.time)
        se.write_int64(self.expiration)
        se.write_int64(int(self.gas_ratio * 100.0))
        se.write_int64(int(self.gas_limit * 100.0))
        se.write_int64(self.delay)
        se.write_int32(self.chain_id)
        se.write_int32(0)
        se.write_string_slice(self.signers)
        se.write_bytes_slice([a.to_bytes() for a in self.actions])
        se.write_bytes_slice([a.to_bytes() for a in self.amount_limits])
        if level == 'publish' or level == 'full':
            se.write_bytes_slice([s.to_bytes() for s in self.signatures])
        if level == 'full':
            se.write_bytes(self.referred_tx)
            se.write_string(self.publisher)
            se.write_bytes_slice([s.to_bytes() for s in self.publisher_signatures])
        return se.to_bytes()


class TxReceipt:
    """Describes the receipt of a `Transaction`.

    Attributes:
        tx_hash: The base58 hash string of the `Transaction`.
        gas_usage: The amount of gas consumed by the `Transaction`.
        ram_usage: The amount of RAM consumed by the `Transaction`.
        status_code: The `StatusCode` of the `Transaction`'s receipt.
        message: The error message corresponding to the `status_code`.
        returns: A list of values returned by the executed ABI calls listed as `Action`.
        receipts: A list of `Receipt` objects.
    """

    class StatusCode(Enum):
        """Indicates the status of the `Transaction`."""
        SUCCESS = pb.TxReceipt.SUCCESS  #: If no error.
        GAS_RUN_OUT = pb.TxReceipt.GAS_RUN_OUT  #: If gas amount was not enough to execute the `Transaction`.
        BALANCE_NOT_ENOUGH = pb.TxReceipt.BALANCE_NOT_ENOUGH  #: If token balance was not enough to execute the `Transaction`.
        WRONG_PARAMETER = pb.TxReceipt.WRONG_PARAMETER  #: If there is an error in the args of one of the `Action`.
        RUNTIME_ERROR = pb.TxReceipt.RUNTIME_ERROR  #: If there was an error when processing the `Transaction`.
        TIMEOUT = pb.TxReceipt.TIMEOUT  #: If the process timeout before the `Transaction` could be processed.
        WRONG_TX_FORMAT = pb.TxReceipt.WRONG_TX_FORMAT  #: If the `Transaction` format is incorrect.
        DUPLICATE_SET_CODE = pb.TxReceipt.DUPLICATE_SET_CODE  #: If the smart contract's id already exist.
        UNKNOWN_ERROR = pb.TxReceipt.UNKNOWN_ERROR  #: None of the above.

    class Receipt:
        """Describes a function call's receipt.

        Attributes:
            func_name: The name of the function.
            content: The content.
        """

        def __init__(self):
            self.func_name: str = ''
            self.content: str = ''

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, tr: pb.TxReceipt.Receipt) -> TxReceipt.Receipt:
            """Deserializes a protobuf object to update this object's members.

            Args:
                tr: The protobuf object.

            Returns:
                Itself.
            """
            self.func_name = tr.func_name
            self.content = tr.content
            return self

        def to_raw(self) -> pb.TxReceipt.Receipt:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
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
        """Returns if the `status_code` is ``SUCCESS``.

        Returns:
            ``True`` if `status_code` is ``SUCCESS``.
        """
        return self.status_code == TxReceipt.StatusCode.SUCCESS

    def from_raw(self, tr: pb.TxReceipt) -> TxReceipt:
        """Deserializes a protobuf object to update this object's members.

        Args:
            tr: The protobuf object.

        Returns:
            Itself.
        """
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
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
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
    """Raised by IOST.wait_tx to indicates an error when processing a `Transaction`.

    Args:
        message: The error message.
        receipt: The `TxReceipt` of the `Transaction`.

    Attributes:
        receipt: The `TxReceipt` of the `Transaction`.
        status_code: If the `TxReceipt` was passed, contains its `status_code` value.
    """

    def __init__(self, message: str = 'Unknown transaction error.',
                 receipt: TxReceipt = None):
        super().__init__(message)
        self.receipt: TxReceipt = receipt
        self.status_code: TxReceipt.StatusCode = receipt.status_code if receipt is not None else TxReceipt.StatusCode.UNKNOWN_ERROR
