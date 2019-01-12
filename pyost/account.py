from __future__ import annotations
from typing import List, Dict
from protobuf_to_dict import protobuf_to_dict
from pprint import pformat

from pyost.rpc.pb import rpc_pb2 as pb
from pyost.signature import KeyPair
from pyost.transaction import Transaction


class Account:
    """An `Account` contains `KeyPair` used to sign `Transactions`.

    Args:
        name: The name of the account.

    Attributes:
        name: The name of the account, used as an id in the args of abi calls.

    Warning:
        `name` must be less than 11 characters and must be unique on the blockchain.
    """

    def __init__(self, name: str):
        self.name: str = name
        self._kps: Dict[str, KeyPair] = {}

    def __str__(self) -> str:
        return pformat(vars(self))

    def add_key_pair(self, kp: KeyPair, permission: str = 'active') -> None:
        """Assigns a KeyPair object to a given permission.
        An `Account` should have at least an ``active`` permission key.

        Args:
            kp: The `KeyPair` to add.
            permission: A permission such as ``active``, ``owner``, etc.
        """
        self._kps[permission] = kp

    def get_key_pair(self, permission: str = 'active') -> KeyPair:
        """Returns the KeyPair for a given permission.

        Args:
            permission: The permission of the KeyPair to retrieve.

        Returns:
            The KeyPair corresponding to the permission.
        """
        return self._kps[permission]

    def sign(self, tx: Transaction, permission: str = 'active') -> Transaction:
        """Signs a Transaction with a given KeyPair.
        The Signature will be added to the list of signatures of the transaction.

        Args:
            tx: The Transaction to sign, its add_signature method will be called.
            permission: The KeyPair to use to sign the Transaction.

        Returns:
            The Transaction.
        """
        return tx.add_signature(self._kps[permission])

    def sign_publish(self, tx: Transaction) -> Transaction:
        """Signs a Transaction as a publisher.
        The Signature will be added to the Transaction's publisher signatures.
        This Account's name will be assigned to the Transaction's publisher.
        The KeyPair of 'active' permission will be used to sign the Transaction.

        Args:
            tx: The Transaction to sign, its add_publisher_signature method will be called.

        Returns:
            The Transaction.
        """
        return tx.add_publisher_signature(self.name, self._kps['active'])


class FrozenBalance:
    """Contains the balance of frozen tokens.

    Attributes:
        amount: The amount of tokens.
        time: The duration the tokens are frozen.
    """
    def __init__(self):
        self.amount: float = 0.0
        self.time: int = 0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, fb: pb.FrozenBalance) -> FrozenBalance:
        """Deserializes a protobuf object to update this object's members.

        Args:
            fb: The protobuf object.

        Returns:
            Itself.
        """
        self.amount = fb.amount
        self.time = fb.time
        return self

    def to_raw(self) -> pb.FrozenBalance:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.FrozenBalance(
            amount=self.amount,
            time=self.time
        )


class TokenBalance:
    """Contains the balance of a token.

    Attributes:
        balance: The balance of the token.
        frozen_balances: A list of amount of tokens and the duration they are frozen.
    """
    def __init__(self):
        self.balance: float = 0.0
        self.frozen_balances: List[FrozenBalance] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, tb: pb.GetTokenBalanceResponse) -> TokenBalance:
        """Deserializes a protobuf object to update this object's members.

        Args:
            tb: The protobuf object.

        Returns:
            Itself.
        """
        self.balance = tb.balance
        self.frozen_balances = [FrozenBalance().from_raw(fb)
                                for fb in tb.frozen_balances
                                ] if tb.frozen_balances is not None else []
        return self

    def to_raw(self) -> pb.GetTokenBalanceResponse:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.GetTokenBalanceResponse(
            balance=self.balance,
            frozen_balances=[fb.to_raw() for fb in self.frozen_balances]
        )


class Token721Balance:
    """Contains the balance of an ERC721 token.

    Attributes:
        balance: The balance of the token.
        token_ids: The list of ids of the token.
    """
    def __init__(self):
        self.balance: int = 0
        self.token_ids: List[str] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, tb: pb.GetToken721BalanceResponse) -> Token721Balance:
        """Deserializes a protobuf object to update this object's members.

        Args:
            tb: The protobuf object.

        Returns:
            Itself.
        """
        self.balance = tb.balance
        self.token_ids = tb.tokenIDs
        return self

    def to_raw(self) -> pb.GetToken721BalanceResponse:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.GetToken721BalanceResponse(
            balance=self.balance,
            tokenIDs=self.token_ids
        )


class AccountInfo:
    """Contains information about an account.

    Attributes:
        name: The name of the account.
        balance: The balance of coins.
        gas_info: A `GasInfo` object.
        ram_info: A `RAMInfo` object.
        permissions: A mapping from `permission` KeyPair to `Permission` objects.
        groups: A mapping of `Group` objects.
        frozen_balances: A list of `FrozenBalance` objects.
    """

    class PledgeInfo:
        """Contains information about the coins pledged by an account.

        Attributes:
            pledger: The name of the account to whom the coins have been pledged.
            amount: The amount of coins pledged.
        """
        def __init__(self):
            self.pledger: str = ''
            self.amount: float = 0.0

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, pi: pb.Account.PledgeInfo) -> AccountInfo.PledgeInfo:
            """Deserializes a protobuf object to update this object's members.

            Args:
                pi: The protobuf object.

            Returns:
                Itself.
            """
            self.pledger = pi.pledger
            self.amount = pi.amount
            return self

        def to_raw(self) -> pb.Account.PledgeInfo:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Account.PledgeInfo(
                pledger=self.pledger,
                amount=self.amount
            )

    # The message defines account gas information.
    class GasInfo:
        """Contains information about the gas own by an account.

        Attributes:
            current_total: The current total amount of gas.
            transferable_gas: The amount of gas that can be transferred.
            pledge_gas: The amount of gas that has been pledged.
            increase_speed: The gas increase speed.
            limit: The gas limit.
            pledged_info: A list of `PledgeInfo` objects.
        """
        def __init__(self):
            self.current_total: float = 0.0
            self.transferable_gas: float = 0.0
            self.pledge_gas: float = 0.0
            self.increase_speed: float = 0.0
            self.limit: float = 0.0
            self.pledged_info: List[AccountInfo.PledgeInfo] = []

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, gi: pb.Account.GasInfo) -> AccountInfo.GasInfo:
            """Deserializes a protobuf object to update this object's members.

            Args:
                gi: The protobuf object.

            Returns:
                Itself.
            """
            self.current_total = gi.current_total
            self.transferable_gas = gi.transferable_gas
            self.pledge_gas = gi.pledge_gas
            self.increase_speed = gi.increase_speed
            self.limit = gi.limit
            self.pledged_info = [AccountInfo.PledgeInfo().from_raw(pi)
                                 for pi in gi.pledged_info] if gi.pledged_info is not None else []
            return self

        def to_raw(self) -> pb.Account.GasInfo:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Account.GasInfo(
                current_total=self.current_total,
                transferable_gas=self.transferable_gas,
                pledge_gas=self.pledge_gas,
                increase_speed=self.increase_speed,
                limit=self.limit,
                pledged_info=[pi.to_raw() for pi in self.pledged_info]
            )

    class RAMInfo:
        """Contains information about the RAM own by an account.

        Attributes:
            available: The amount of RAM still available.
            used: The amount of RAM that has already been used.
            total: The sum of `available` and `used`.
        """
        def __init__(self):
            self.available: int = 0
            self.used: int = 0
            self.total: int = 0

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, ri: pb.Account.RAMInfo) -> AccountInfo.RAMInfo:
            """Deserializes a protobuf object to update this object's members.

            Args:
                ri: The protobuf object.

            Returns:
                Itself.
            """
            self.available = ri.available
            self.used = ri.used
            self.total = ri.total
            return self

        def to_raw(self) -> pb.Account.RAMInfo:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Account.RAMInfo(
                available=self.available,
                used=self.used,
                total=self.total
            )

    class Item:
        """Contains information about permission item.

        Attributes:
            id: Permission name or `KeyPair` id.
            is_key_pair: Indicates whether it is a `KeyPair`.
            weight: Permission weight.
            permission: Name of the permission such as ``active``.
        """
        def __init__(self):
            self.id: str = ''
            self.is_key_pair: bool = False
            self.weight: int = 0
            self.permission: str = ''

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, i: pb.Account.Item) -> AccountInfo.Item:
            """Deserializes a protobuf object to update this object's members.

            Args:
                i: The protobuf object.

            Returns:
                Itself.
            """
            self.id = i.id
            self.is_key_pair = i.is_key_pair
            self.weight = i.weight
            self.permission = i.permission
            return self

        def to_raw(self) -> pb.Account.Item:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Account.Item(
                id=self.id,
                is_key_pair=self.is_key_pair,
                weight=self.weight,
                permission=self.permission
            )

    class Group:
        """Contains information about permission group.

        Attributes:
            name: The name of the group.
            items: A list of `Item` objects.
        """
        def __init__(self):
            self.name: str = ''
            self.items: List[AccountInfo.Item] = []

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, g: pb.Account.Group) -> AccountInfo.Group:
            """Deserializes a protobuf object to update this object's members.

            Args:
                g: The protobuf object.

            Returns:
                Itself.
            """
            self.name = g.name
            self.items = [AccountInfo.Item().from_raw(item)
                          for item in g.items] if g.items is not None else []
            return self

        def to_raw(self) -> pb.Account.Group:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Account.Group(
                name=self.name,
                items=[item.to_raw() for item in self.items]
            )

    class Permission:
        """Contains information about a permission.

        Attributes:
            name: The permission's name.
            group_names: A list of permission group names.
            items: A list of `Item` objects.
            threshold: The permission's threshold.
        """
        def __init__(self):
            self.name: str = ''
            self.group_names: List[str] = []
            self.items: List[AccountInfo.Item] = []
            self.threshold: int = 0

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, p: pb.Account.Permission) -> AccountInfo.Permission:
            """Deserializes a protobuf object to update this object's members.

            Args:
                p: The protobuf object.

            Returns:
                Itself.
            """
            self.name = p.name
            self.group_names = p.group_names
            self.items = [AccountInfo.Item().from_raw(item)
                          for item in p.items] if p.items is not None else []
            self.threshold = p.threshold
            return self

        def to_raw(self) -> pb.Account.Permission:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Account.Permission(
                name=self.name,
                group_names=self.group_names,
                items=[item.to_raw() for item in self.items],
                threshold=self.threshold
            )

    def __init__(self):
        self.name: str = ''
        self.balance: float = 0.0
        self.gas_info: AccountInfo.GasInfo = None
        self.ram_info: AccountInfo.RAMInfo = None
        self.permissions: Dict[str, AccountInfo.Permission] = {}
        self.groups: Dict[str, AccountInfo.Group] = {}
        self.frozen_balances: List[FrozenBalance] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, a: pb.Account) -> AccountInfo:
        """Deserializes a protobuf object to update this object's members.

        Args:
            a: The protobuf object.

        Returns:
            Itself.
        """
        self.name = a.name
        self.balance = a.balance
        self.gas_info = AccountInfo.GasInfo().from_raw(a.gas_info)
        self.ram_info = AccountInfo.RAMInfo().from_raw(a.ram_info)
        self.permissions = {key: AccountInfo.Permission().from_raw(val)
                            for key, val in a.permissions.items()} if a.permissions is not None else {}
        self.groups = {key: AccountInfo.Group().from_raw(val)
                       for key, val in a.groups.items()} if a.groups is not None else {}
        self.frozen_balances = [FrozenBalance().from_raw(fb)
                                for fb in a.frozen_balances] if a.frozen_balances is not None else []
        return self

    def to_raw(self) -> pb.Account:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.Account(
            name=self.name,
            balance=self.balance,
            gas_info=self.gas_info.to_raw(),
            ram_info=self.ram_info.to_raw(),
            permissions={key: val.to_raw() for key, val in self.permissions.items()},
            groups={key: val.to_raw() for key, val in self.groups.items()},
            frozen_balances=[fb.to_raw() for fb in self.frozen_balances]
        )
