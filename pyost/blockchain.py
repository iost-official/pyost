from __future__ import annotations
from typing import List
from enum import Enum
from protobuf_to_dict import protobuf_to_dict
from pprint import pformat

from pyost.rpc.pb import rpc_pb2 as pb
from pyost.transaction import Transaction


class NodeInfo:
    """Contains information about a node.

    Attributes:
        build_time: Date and time when the node was built.
        git_hash: A base58 hash string.
        mode: Mode such as ``ModeNormal``.
        network: A `NetworkInfo` object.
    """

    class NetworkInfo:
        """Contains information about a network.

        Attributes:
            id: The base58 string id of the node.
            peer_count: The number of peers.
            peer_info: A list of `PeerInfo` objects.
        """

        class PeerInfo:
            """Contains information about a node's peer.

            Attributes:
                id: The base58 string id of the peer.
                addr: The IP address of the peer.
            """

            def __init__(self):
                self.id: str = ''
                self.addr: str = ''

            def __str__(self) -> str:
                return str(protobuf_to_dict(self.to_raw()))

            def from_raw(self, pi: pb.PeerInfo) -> NodeInfo.NetworkInfo.PeerInfo:
                """Deserializes a protobuf object to update this object's members.

                Args:
                    pi: The protobuf object.

                Returns:
                    Itself.
                """
                self.id = pi.id
                self.addr = pi.addr
                return self

            def to_raw(self) -> pb.PeerInfo:
                """Serializes this object's members to a protobuf object.

                Returns:
                    A protobuf object.
                """
                return pb.PeerInfo(
                    id=self.id,
                    addr=self.addr
                )

        def __init__(self):
            self.id: str = ''
            self.peer_count: int = 0
            self.peer_info: List[NodeInfo.NetworkInfo.PeerInfo] = []

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, ni: pb.NetworkInfo) -> NodeInfo.NetworkInfo:
            """Deserializes a protobuf object to update this object's members.

            Args:
                ni: The protobuf object.

            Returns:
                Itself.
            """
            self.id = ni.id
            self.peer_count = ni.peer_count
            self.peer_info = [NodeInfo.NetworkInfo.PeerInfo().from_raw(info)
                              for info in ni.peer_info]
            return self

        def to_raw(self) -> pb.NetworkInfo:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.NetworkInfo(
                id=self.id,
                peer_count=self.peer_count,
                peer_info=[pi.to_raw() for pi in self.peer_info]
            )

    def __init__(self):
        self.build_time: str = ''
        self.git_hash: str = ''
        self.mode: str = ''
        self.network: NodeInfo.NetworkInfo = None

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, ni: pb.NodeInfoResponse) -> NodeInfo:
        """Deserializes a protobuf object to update this object's members.

        Args:
            ni: The protobuf object.

        Returns:
            Itself.
        """
        self.build_time = ni.build_time
        self.git_hash = ni.git_hash
        self.mode = ni.mode
        self.network = NodeInfo.NetworkInfo().from_raw(ni.network)
        return self

    def to_raw(self) -> pb.NodeInfoResponse:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.NodeInfoResponse(
            build_time=self.build_time,
            git_hash=self.git_hash,
            mode=self.mode,
            network=self.network.to_raw() if self.network is not None else None
        )


class ChainInfo:
    """Contains information about the blockchain.

    Attributes:
        net_name: The name of the network, such as ``mainnet``, ``debugnet`` or ``testnet``.
        protocol_version: The IOST protocol version.
        head_block: The height of the head block.
        head_block_hash: The base58 hash string of the head block.
        lib_block: The last irreversible block number.
        lib_block_hash: The base58 hash string of the last irreversible block number.
        witness_list: The list of current witnesses IOST ids.
    """

    def __init__(self):
        self.net_name: str = ''
        self.protocol_version: str = ''
        self.head_block: int = 0
        self.head_block_hash: str = ''
        self.lib_block: int = 0
        self.lib_block_hash: str = ''
        self.witness_list: List[str] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, ci: pb.ChainInfoResponse) -> ChainInfo:
        """Deserializes a protobuf object to update this object's members.

        Args:
            ci: The protobuf object.

        Returns:
            Itself.
        """
        self.net_name = ci.net_name
        self.protocol_version = ci.protocol_version
        self.head_block = ci.head_block
        self.head_block_hash = ci.head_block_hash
        self.lib_block = ci.lib_block
        self.lib_block_hash = ci.lib_block_hash
        self.witness_list = ci.witness_list
        return self

    def to_raw(self) -> pb.ChainInfoResponse:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.ChainInfoResponse(
            net_name=self.net_name,
            protocol_version=self.protocol_version,
            head_block=self.head_block,
            head_block_hash=self.head_block_hash,
            lib_block=self.lib_block,
            lib_block_hash=self.lib_block_hash,
            witness_list=self.witness_list
        )


class RAMInfo:
    """Contains information about the blockchain's RAM.

    Attributes:
        used_ram: How many bytes have been used.
        available_ram: How many bytes have not been used yet.
        total_ram: Total bytes of RAM.
        sell_price: User can sell ``NUM`` bytes RAM to system to get ``NUM * sell_price`` IOSTs.
        buy_price: User can spend approximately ``NUM * buy_price`` IOSTs for ``NUM`` bytes RAM.
    """

    def __init__(self):
        self.used_ram: int = 0
        self.available_ram: int = 0
        self.total_ram: int = 0
        self.sell_price: float = 0.0
        self.buy_price: float = 0.0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, ri: pb.RAMInfoResponse) -> RAMInfo:
        """Deserializes a protobuf object to update this object's members.

        Args:
            ri: The protobuf object.

        Returns:
            Itself.
        """
        self.used_ram = ri.used_ram
        self.available_ram = ri.available_ram
        self.total_ram = ri.total_ram
        self.sell_price = ri.sell_price
        self.buy_price = ri.buy_price
        return self

    def to_raw(self) -> pb.RAMInfoResponse:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.RAMInfoResponse(
            used_ram=self.used_ram,
            available_ram=self.available_ram,
            total_ram=self.total_ram,
            sell_price=self.sell_price,
            buy_price=self.buy_price
        )


class GasRatio:
    """Contains information about the blockchain's gas ratios.

    Attributes:
        lowest_gas_ratio: Lowest gas ratio in head block.
        median_gas_ratio: Median gas ratio in head block.
    """

    def __init__(self):
        self.lowest_gas_ratio: float = 0.0
        self.median_gas_ratio: float = 0.0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, gr: pb.GasRatioResponse) -> GasRatio:
        """Deserializes a protobuf object to update this object's members.

        Args:
            gr: The protobuf object.

        Returns:
            Itself.
        """
        self.lowest_gas_ratio = gr.lowest_gas_ratio
        self.median_gas_ratio = gr.median_gas_ratio
        return self

    def to_raw(self) -> pb.GasRatioResponse:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.GasRatioResponse(
            lowest_gas_ratio=self.lowest_gas_ratio,
            median_gas_ratio=self.median_gas_ratio
        )


class Block:
    """Contains details about a block.

    Attributes:
        status: The status of the block, ``PENDING`` or ``IRREVERSIBLE``.
        hash: The base58 hash string of the block.
        version: The protocol version of the block.
        parent_hash: The base58 hash string of the block's parent.
        tx_merkle_hash: The base58 hash string of the Merkle tree of transactions.
        tx_receipt_merkle_hash: The base58 hash string of the Merkle tree of transaction receipts.
        number: The number of the block.
        witness: The IOST id of the block's witness.
        time: The time the block was created.
        gas_usage: The amount of gas consumed by the block.
        tx_count: The number of transactions in the block.
        info: A `Info` object.
        transactions: The list of `Transactions`.
    """

    class Status(Enum):
        """Indicates the status of a block."""
        PENDING = pb.BlockResponse.PENDING  #: Indicates that the block is pending to be processed.
        IRREVERSIBLE = pb.BlockResponse.IRREVERSIBLE  #: Indicates that the block has been processed.
        UNKNOWN = -1  #: Indicates an unknown error.

    class Info:
        """Contains information about a block.

        Attributes:
            mode: Mode.
            thread: Thread.
            batch_index: List of indices.
        """

        def __init__(self):
            self.mode: int = 0
            self.thread: int = 0
            self.batch_index: List[int] = []

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, ri: pb.Block.Info) -> Block.Info:
            """Deserializes a protobuf object to update this object's members.

            Args:
                ri: The protobuf object.

            Returns:
                Itself.
            """
            self.mode = ri.mode
            self.thread = ri.thread
            self.batch_index = ri.batch_index
            return self

        def to_raw(self) -> pb.Block.Info:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Block.Info(
                mode=self.mode,
                thread=self.thread,
                batch_index=self.batch_index
            )

    def __init__(self):
        self.status: Block.Status = Block.Status.UNKNOWN
        self.hash: str = ''
        self.version: int = 0
        self.parent_hash: str = ''
        self.tx_merkle_hash: str = ''
        self.tx_receipt_merkle_hash: str = ''
        self.number: int = 0
        self.witness: str = ''
        self.time: int = 0
        self.gas_usage: float = 0.0
        self.tx_count: int = 0
        self.info: Block.Info = None
        self.transactions: List[Transaction] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, rb: pb.Block, status: Status = Status.UNKNOWN) -> Block:
        """Deserializes a protobuf object to update this object's members.

        Args:
            rb: The protobuf object.
            status: The status of the `Block`.

        Returns:
            Itself.
        """
        self.status = status
        self.hash = rb.hash
        self.version = rb.version
        self.parent_hash = rb.parent_hash
        self.tx_merkle_hash = rb.tx_merkle_hash
        self.tx_receipt_merkle_hash = rb.tx_receipt_merkle_hash
        self.number = rb.number
        self.witness = rb.witness
        self.time = rb.time
        self.gas_usage = rb.gas_usage
        self.tx_count = rb.tx_count
        self.info = Block.Info().from_raw(rb.info)
        self.transactions = [Transaction().from_raw(tx) for tx in rb.transactions
                             ] if rb.transactions is not None else []
        return self

    def to_raw(self) -> pb.Block:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.Block(
            hash=self.hash,
            version=self.version,
            parent_hash=self.parent_hash,
            tx_merkle_hash=self.tx_merkle_hash,
            tx_receipt_merkle_hash=self.tx_receipt_merkle_hash,
            number=self.number,
            witness=self.witness,
            time=self.time,
            gas_usage=self.gas_usage,
            tx_count=self.tx_count,
            info=self.info.to_raw() if self.info is not None else None,
            transactions=[tx.to_raw() for tx in self.transactions]
        )
