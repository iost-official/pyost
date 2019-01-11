from __future__ import annotations
from typing import List
from enum import Enum
from protobuf_to_dict import protobuf_to_dict
from pprint import pformat

from pyost.rpc.pb import rpc_pb2 as pb
from pyost.transaction import Transaction


class NodeInfo:
    class NetworkInfo:
        class PeerInfo:
            def __init__(self):
                self.id: str = ''
                self.addr: str = ''

            def __str__(self) -> str:
                return str(protobuf_to_dict(self.to_raw()))

            def from_raw(self, pi: pb.PeerInfo) -> NodeInfo.NetworkInfo.PeerInfo:
                self.id = pi.id
                self.addr = pi.addr
                return self

            def to_raw(self) -> pb.PeerInfo:
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
            self.id = ni.id
            self.peer_count = ni.peer_count
            self.peer_info = [NodeInfo.NetworkInfo.PeerInfo().from_raw(info)
                              for info in ni.peer_info]
            return self

        def to_raw(self) -> pb.NetworkInfo:
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
        self.build_time = ni.build_time
        self.git_hash = ni.git_hash
        self.mode = ni.mode
        self.network = NodeInfo.NetworkInfo().from_raw(ni.network)
        return self

    def to_raw(self) -> pb.NodeInfoResponse:
        return pb.NodeInfoResponse(
            build_time=self.build_time,
            git_hash=self.git_hash,
            mode=self.mode,
            network=self.network.to_raw() if self.network is not None else None
        )


class ChainInfo:
    def __init__(self):
        # the name of network, such mainnet or testnet
        self.net_name: str = ''
        # the iost protocol version
        self.protocol_version: str = ''
        # head block height
        self.head_block: int = 0
        # head block hash
        self.head_block_hash: str = ''
        # last irreversible block number
        self.lib_block: int = 0
        # last irreversible block hash
        self.lib_block_hash: str = ''
        # the current witness list
        self.witness_list: List[str] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, ci: pb.ChainInfoResponse) -> ChainInfo:
        self.net_name = ci.net_name
        self.protocol_version = ci.protocol_version
        self.head_block = ci.head_block
        self.head_block_hash = ci.head_block_hash
        self.lib_block = ci.lib_block
        self.lib_block_hash = ci.lib_block_hash
        self.witness_list = ci.witness_list
        return self

    def to_raw(self) -> pb.ChainInfoResponse:
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
    def __init__(self):
        # how many bytes have been used
        self.used_ram: int = 0
        # how many bytes have not been used
        self.available_ram: int = 0
        # total ram byte
        self.total_ram: int = 0
        # User can sell NUM bytes RAM to system to get `NUM * sell_price` IOSTs
        self.sell_price: float = 0.0
        # User can spend approximate `NUM * buy_price` IOSTs for NUM bytes RAM
        self.buy_price: float = 0.0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, ri: pb.RAMInfoResponse) -> RAMInfo:
        self.used_ram = ri.used_ram
        self.available_ram = ri.available_ram
        self.total_ram = ri.total_ram
        self.sell_price = ri.sell_price
        self.buy_price = ri.buy_price
        return self

    def to_raw(self) -> pb.RAMInfoResponse:
        return pb.RAMInfoResponse(
            used_ram=self.used_ram,
            available_ram=self.available_ram,
            total_ram=self.total_ram,
            sell_price=self.sell_price,
            buy_price=self.buy_price
        )


class GasRatio:
    def __init__(self):
        # lowest gas ratio in head block
        self.lowest_gas_ratio: float = 0.0
        # median gas ratio in head block
        self.median_gas_ratio: float = 0.0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, gr: pb.GasRatioResponse) -> GasRatio:
        self.lowest_gas_ratio = gr.lowest_gas_ratio
        self.median_gas_ratio = gr.median_gas_ratio
        return self

    def to_raw(self) -> pb.GasRatioResponse:
        return pb.GasRatioResponse(
            lowest_gas_ratio=self.lowest_gas_ratio,
            median_gas_ratio=self.median_gas_ratio
        )


class Block:
    class Status(Enum):
        PENDING = pb.BlockResponse.PENDING
        IRREVERSIBLE = pb.BlockResponse.IRREVERSIBLE
        UNKNOWN = -1

    class Info:
        def __init__(self):
            self.mode: int = 0
            self.thread: int = 0
            self.batch_index: List[int] = []

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, ri: pb.Block.Info) -> Block.Info:
            self.mode = ri.mode
            self.thread = ri.thread
            self.batch_index = ri.batch_index
            return self

        def to_raw(self) -> pb.Block.Info:
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
