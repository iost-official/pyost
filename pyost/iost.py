import grpc

from pyost.api.rpc import apis_pb2_grpc, apis_pb2
from pyost.api.core.event import event_pb2
from google.protobuf.empty_pb2 import Empty
from protobuf_to_dict import protobuf_to_dict
import protobuf_to_dict as ptd


class IOST():
    """
    This class provides API access to the IOST blockchain.
    """

    def __init__(self, url: str, timeout: int = 10):
        """
        Connects to a node.

        Args:
            url (str): Node's IP address and port number.
            timeout (int): Number of seconds to wait when querying the node until timing out.
        """
        self._channel = grpc.insecure_channel(url)
        self._stub = None
        self._timeout = timeout
        try:
            grpc.channel_ready_future(self._channel).result(timeout=self._timeout)
        except grpc.FutureTimeoutError as e:
            raise ConnectionError('Error connecting to server') from e
        else:
            self._stub = apis_pb2_grpc.ApisStub(self._channel)

    # // get the current height of the blockchain
    # rpc GetHeight (google.protobuf.Empty) returns (HeightRes) {
    #    option (google.api.http) = {
    #        get: "/getHeight"
    #    };
    # }
    # message HeightRes {
    # 	// the height of the blockchain
    # 	int64 height=1;
    # }
    def get_height(self) -> int:
        """
        Gets the current height of the blockchain.

        Note:
            REST API: "/getHeight"

        Returns:
            The height of the blockchain.
        """
        res = self._stub.GetHeight(Empty())
        return res.height

    # // get the tx by hash
    # rpc GetTxByHash (HashReq) returns (txRes) {
    #    option (google.api.http) = {
    #        get: "/getTxByHash/{hash}"
    #    };
    # }
    # message HashReq {
    # 	string hash=1;
    # }
    # message txRes {
    # 	//the queried transaction
    # 	tx.TxRaw txRaw = 1;
    # 	bytes hash = 2;
    # }
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
    # message ActionRaw {
    #     string contract = 1;
    #     string actionName = 2;
    #     string data = 3;
    # }
    # message SignatureRaw {
    #     int32 algorithm = 1;
    #     bytes sig = 2;
    #     bytes pubKey = 3;
    # }
    def get_tx_by_hash(self, tx_hash: str) -> (dict, bytes):
        """
        Gets a transaction by its hash value.

        Note:
            REST API: "/getTxByHash/{hash}"

        Args:
            tx_hash (str): The base58 hash string of the transaction.

        Returns:
            (dict, bytes): A tuple containing the transaction content as a dict
                and its hash as bytes. The dict has the following format::

                {
                    'time': int,
                    'expiration': int,
                    'gasLimit': int,
                    'gasPrice': 1,
                    'actions': [{
                        'contract': string,
                        'actionName': string,
                        'data': string
                    }],
                    'signers': bytes,
                    'signs': [{
                        'algorithm': int,
                        'sig': bytes,
                        'pubKey':  bytes
                    }],
                    'publisher': {
                        'algorithm': int,
                        'sig': bytes,
                        'pubKey': bytes
                    }
                }
        """
        req = apis_pb2.HashReq(hash=tx_hash)
        res = self._stub.GetTxByHash(req)
        print(ptd.get_field_names_and_options(res))
        return (protobuf_to_dict(res.txRaw), res.hash)

    # // get receipt by hash
    # rpc GetTxReceiptByHash(HashReq) returns (txReceiptRes) {
    #    option (google.api.http) = {
    #        get: "/getTxReceiptByHash/{hash}"
    #    };
    # }
    # message HashReq {
    # 	string hash=1;
    # }
    # message txReceiptRes {
    # 	tx.TxReceiptRaw txReceiptRaw = 1;
    # 	bytes hash = 2;
    # }
    # message TxReceiptRaw {
    #     bytes txHash = 1;
    #     int64 gasUsage = 2;
    #     StatusRaw status = 3;
    #     int32 succActionNum = 4;
    #     repeated ReceiptRaw receipts = 5;
    # }
    # message StatusRaw {
    #     int32 code = 1;
    #     string message = 2;
    # }
    # message ReceiptRaw {
    #     int32 type = 1;
    #     string content = 2;
    # }
    def get_tx_receipt_by_hash(self, receipt_hash: str) -> (dict, bytes):
        """
        Gets a transaction receipt by its receipt hash value.

        Note:
            REST API: "/getTxReceiptByHash/{hash}"

        Args:
            receipt_hash (str): The base58 hash string of the transaction receipt.

        Returns:
            (dict, bytes): A tuple containing the receipt content as a dict
                and its hash as bytes. The dict has the following format::

                {
                    'txHash': bytes,
                    'gasUsage': int,
                    'status': {
                        'code': int,
                        'message': string
                    },
                    'succActionNum': int,
                    'receipts': [{
                        'type': int,
                        'content: string
                    }]
                }
        """
        req = apis_pb2.HashReq(hash=receipt_hash)
        res = self._stub.GetTxReceiptByHash(req)
        return (protobuf_to_dict(res.txReceiptRaw), res.hash)

    # // get receipt by txhash
    # rpc GetTxReceiptByTxHash(HashReq) returns (txReceiptRes) {
    #    option (google.api.http) = {
    #        get: "/getTxReceiptByTxHash/{hash}"
    #    };
    # }
    # message HashReq {
    # 	string hash=1;
    # }
    # message txReceiptRes {
    # 	tx.TxReceiptRaw txReceiptRaw = 1;
    # 	bytes hash = 2;
    # }
    def get_tx_receipt_by_tx_hash(self, tx_hash: str) -> (dict, bytes):
        """
        Gets a transaction receipt by its transaction hash value.

        Note:
            REST API: "/getTxReceiptByTxHash/{hash}"

        Args:
            receipt_hash (str): The base58 hash string of the transaction.

        Returns:
            (dict, bytes): A tuple containing the receipt content as a dict
            and its hash as bytes. The dict has the following format::

                {
                    'txHash': bytes,
                    'gasUsage': int,
                    'status': {
                        'code': int,
                        'message': string
                    },
                    'succActionNum': int,
                    'receipts': [{
                        'type': int,
                        'content: string
                    }]
                }
        """
        req = apis_pb2.HashReq(hash=tx_hash)
        res = self._stub.GetTxReceiptByTxHash(req)
        return (protobuf_to_dict(res.txReceiptRaw), res.hash)

    # // get the block by hash
    # rpc GetBlockByHash (BlockByHashReq) returns (BlockInfo) {
    #    option (google.api.http) = {
    #        get: "/getBlockByHash/{hash}/{complete}"
    #    };
    # }
    # message BlockByHashReq {
    # 	string hash=1;
    # 	// complete means return the whole block or just blockhead+txhash_list
    # 	bool complete=2;
    # }
    # message BlockInfo {
    # 	block.BlockHead head = 1;
    # 	bytes hash = 2;
    # 	repeated tx.TxRaw txs = 3;
    # 	repeated bytes txhash= 4 ;
    # 	repeated tx.TxReceiptRaw receipts = 5;
    # 	repeated bytes receiptHash = 6;
    # }
    # message BlockHead {
    #     int64 version = 1;
    #     bytes parentHash = 2;
    #     bytes txsHash = 3;
    #     bytes merkleHash = 4;
    #     bytes info = 5;
    #     int64 number = 6;
    #     string witness = 7;
    #     int64 time = 8;
    # }
    # TODO: where blockraw is used? when complete=Fase?
    # message BlockRaw {
    #     BlockHead head = 1;
    #     bytes sign = 2;
    #     repeated bytes txs = 3;
    #     repeated bytes receipts = 4;
    # }
    def get_block_by_hash(self, block_hash: str, complete: bool = False) -> dict:
        """
        Gets a block by its hash.

        Note:
            REST API: "/getBlockByHash/{hash}/{complete}"

        Args:
            block_hash: The base58 hash string of the block.
            complete: If True, returns the whole block, otherwise
                returns the head and the list of transaction and receipt hashes.

        Returns:
            dict: The whole block if `complete` is True,
                otherwise the head and the list of transactions and receipts.

            When `complete` is False, the dict has the following format::

                {
                    'head': {
                        #'version': int,
                        #'parentHash': bytes,
                        'txsHash': bytes,
                        'merkleHash': bytes,
                        #'info': bytes,
                        #'number': int,
                        'witness': string,
                        #'time': int
                    },
                    'hash': bytes,
                    'txhash': [ bytes ],
                    'receiptHash': [ bytes ]
                }

            When `complete` is True, the dict has the following format::

                {
                    'head': {
                        #'version': int,
                        #'parentHash': bytes,
                        'txsHash': bytes,
                        'merkleHash': bytes,
                        #'info': bytes,
                        #'number': int,
                        'witness': string,
                        #'time': int
                    },
                    'hash': bytes,
                    'txs': [ TxRaw (see return type of ``get_tx_by_hash``) ],
                    'receipts': [ TxReceiptRaw (see return type of ``get_tx_receipt_by_hash``) ]
                }

        """
        req = apis_pb2.BlockByHashReq(hash=block_hash, complete=complete)
        res = self._stub.GetBlockByHash(req)
        return protobuf_to_dict(res)

    # // get the block by number
    # rpc getBlockByNum (BlockByNumReq) returns (BlockInfo) {
    #    option (google.api.http) = {
    #        get: "/getBlockByNum/{num}/{complete}"
    #    };
    # }
    # message BlockByNumReq {
    # 	int64 num=1;
    # 	// complete means return the whole block or just blockhead+txhash_list
    # 	bool complete=2;
    # }
    # message BlockInfo {
    # 	block.BlockHead head = 1;
    # 	bytes hash = 2;
    # 	repeated tx.TxRaw txs = 3;
    # 	repeated bytes txhash= 4 ;
    # 	repeated tx.TxReceiptRaw receipts = 5;
    # 	repeated bytes receiptHash = 6;
    # }
    # message BlockHead {
    #     int64 version = 1;
    #     bytes parentHash = 2;
    #     bytes txsHash = 3;
    #     bytes merkleHash = 4;
    #     bytes info = 5;
    #     int64 number = 6;
    #     string witness = 7;
    #     int64 time = 8;
    # }
    def get_block_by_num(self, block_num: int, complete: bool = False) -> dict:
        """
        Gets a block by its number.

        Note:
            REST API: "/getBlockByNum/{num}/{complete}"

        Args:
            block_num: The number of the block.
            complete: If True, returns the whole block,
                otherwise returns the head and the list of transaction hashes.

        Returns:
            dict: The whole block if `complete` is True,
                otherwise the head and the list of transactions.

            When `complete` is False, the dict has the following format::

                {
                    'head': {
                        #'version': int,
                        #'parentHash': bytes,
                        'txsHash': bytes,
                        'merkleHash': bytes,
                        #'info': bytes,
                        #'number': int,
                        'witness': string,
                        #'time': int
                    },
                    'hash': bytes,
                    'txhash': [ bytes ]
                }

            When `complete` is True, the dict has the following format::

                {
                    'head': {
                        #'version': int,
                        #'parentHash': bytes,
                        'txsHash': bytes,
                        'merkleHash': bytes,
                        #'info': bytes,
                        #'number': int,
                        'witness': string,
                        #'time': int
                    },
                    'hash': bytes,
                    'txs': [ TxRaw (see return type of ``get_tx_by_hash``) ]
                }

        """
        req = apis_pb2.BlockByNumReq(num=block_num, complete=complete)
        res = self._stub.getBlockByNum(req)
        return protobuf_to_dict(res)

    # // get the balance of some account by account ID
    # rpc GetBalance (GetBalanceReq) returns (GetBalanceRes) {
    #    option (google.api.http) = {
    #        get: "/getBalance/{ID}/{useLongestChain}"
    #    };
    # }
    # message GetBalanceReq {
    # 	string ID=1;
    # 	// useLongestChain means whether geting the balance also from pending blocks(in the longest chain)
    # 	bool useLongestChain = 2;
    # }
    # message GetBalanceRes {
    # 	// the queried balance
    # 	int64 balance=1;
    # }
    def get_balance(self, account_id: str, use_longest_chain: bool = True) -> int:
        """
        Gets the balance of an account by its id.

        Note:
            REST API: "/getBalance/{ID}/{useLongestChain}"

        Args:
            account_id (str): The ID of the account.
            use_longest_chain (bool): If True, also gets balance from pending blocks
                (in the longest chain)

        Returns:
            int: the balance of the account (units?).
        """
        req = apis_pb2.GetBalanceReq(ID=account_id, useLongestChain=use_longest_chain)
        res = self._stub.GetBalance(req)
        return res.balance

    # // get the Net ID
    # rpc GetNetID (google.protobuf.Empty) returns (GetNetIDRes) {
    #    option (google.api.http) = {
    #        get: "/getNetID"
    #    };
    # }
    # message GetNetIDRes {
    # 	string ID=1;
    # }
    def get_net_id(self) -> str:
        """
        Gets the ID of the node.

        Note:
            REST API: "/getNetID"

        Returns:
            The ID of the node as a base58 hash string.
        """
        res = self._stub.GetNetID(Empty())
        return res.ID

    # // get the value of the corresponding key in stateDB
    # rpc GetState (GetStateReq) returns (GetStateRes) {
    #    option (google.api.http) = {
    #        get: "/getState/{key}"
    #    };
    # }
    # message GetStateReq {
    # 	string key=1;
    # 	// get the value from StateDB,field is needed if StateDB[key] is a map.(we get StateDB[key][field] in this case)
    # 	string field = 2;
    # }
    # message GetStateRes {
    # 	string value=1;
    # }
    def get_state(self, key: str, field: str = None) -> str:
        """
        Gets the value of a key in the StateDB.

        Note:
            REST API: "/getState/{key}"

        Args:
            key (str): The key.
            field (str): Required if `key` is a map.

        Returns:
            str: StateDB[`key`] or StateDB[`key`][`field`] if `key` is a map.
        """
        req = apis_pb2.GetStateReq(key=key, field=field)
        res = self._stub.GetState(req)
        return res.value

    # // receive encoded tx
    # rpc SendRawTx (RawTxReq) returns (SendRawTxRes) {
    #    option (google.api.http) = {
    #        post: "/sendRawTx"
    #        body: "*"
    #    };
    # }
    # message RawTxReq {
    # 	// the rawdata of a tx
    # 	bytes data=1;
    # }
    # message SendRawTxRes {
    # 	// the hash of the received transaction
    # 	string hash=1;
    # }
    # TODO: need to replace data with a tx.TxRaw? (or take raw_tx a dict and convert to proto)
    def send_raw_tx(self, raw_tx: bytes) -> str:
        req = apis_pb2.RawTxReq(data=raw_tx)
        res = self._stub.SendRawTx(req)
        return res.hash

    # // not supported yet
    # rpc EstimateGas (RawTxReq) returns (GasRes) {
    #    option (google.api.http) = {
    #        post: "/estimateGas"
    #        body: "*"
    #    };
    # }
    # message RawTxReq {
    # 	// the rawdata of a tx
    # 	bytes data=1;
    # }
    # message GasRes {
    # 	uint64 gas=1;
    # }
    # TODO: need to replace data with a tx.TxRaw?
    def estimate_gas(self, raw_tx: bytes) -> int:
        req = apis_pb2.RawTxReq(data=raw_tx)
        res = self._stub.EstimateGas(req)
        return res.gas

    # // subscribe an event
    # rpc Subscribe (SubscribeReq) returns (stream SubscribeRes) {
    #    option (google.api.http) = {
    #        post: "/subscribe"
    #        body: "*"
    #    };
    # }
    # message SubscribeReq {
    # 	repeated event.Event.Topic topics=1;
    # }
    # message Event {
    #     enum Topic {
    #         TransactionResult = 0;
    #         ContractEvent = 1;
    #         ContractUserEvent = 2;
    #         ContractSystemEvent = 3;
    #     }
    #     Topic topic = 1;
    #     string data = 2;
    #     int64 time = 3;
    # }
    # message SubscribeRes {
    # 	event.Event ev=1;
    # }
    # TODO: event_topic is a list of enum (need to pass an iterator?)
    # TODO: if topics is a scalar, transform it into a 1 element list
    # TODO: check that each topic is a valid Enum value
    def subscribe(self, topics: [int]) -> dict:
        print(ptd.get_field_names_and_options(event_pb2.Event))
        req = apis_pb2.SubscribeReq(topics=topics)
        res = self._stub.Subscribe(req)
        return protobuf_to_dict(res.ev)
