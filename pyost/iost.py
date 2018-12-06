import grpc

from pyost.api.rpc import apis_pb2_grpc, apis_pb2
from pyost.api.core.event import event_pb2
from google.protobuf.empty_pb2 import Empty
from protobuf_to_dict import protobuf_to_dict
import protobuf_to_dict as ptd


class IOST():
    def __init__(self, url, timeout=10):
        self._channel = grpc.insecure_channel(url)
        self._stub = None
        self._timeout = timeout
        try:
            grpc.channel_ready_future(self._channel).result(timeout=self._timeout)
        except grpc.FutureTimeoutError as e:
            raise ConnectionError('Error connecting to server') from e
        else:
            self._stub = apis_pb2_grpc.ApisStub(self._channel)

    # TODO: raise error if params don't match the type of protos
    # TODO: by typing params or using assert?
    # rpc GetHeight (google.protobuf.Empty) returns (HeightRes) {
    #    option (google.api.http) = {
    #        get: "/getHeight"
    #    };
    # }
    # message HeightRes {
    # 	// the height of the blockchain
    # 	int64 height=1;
    # }
    def get_height(self):
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
    def get_tx_by_hash(self, tx_hash):
        req = apis_pb2.HashReq(hash=tx_hash)
        res = self._stub.GetTxByHash(req)
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
    def get_tx_receipt_by_hash(self, receipt_hash):
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
    def get_tx_receipt_by_tx_hash(self, tx_hash):
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
    def get_block_by_hash(self, block_hash, complete=False):
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
    def get_block_by_num(self, block_num, complete=False):
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
    def get_balance(self, account_id, use_longest_chain=False):
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
    def get_net_id(self):
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
    def get_state(self, key, field=None):
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
    def send_raw_tx(self, raw_tx):
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
    def estimate_gas(self, raw_tx):
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
    def subscribe(self, topics):
        print(ptd.get_field_names_and_options(event_pb2.Event))
        req = apis_pb2.SubscribeReq(topics=topics)
        res = self._stub.Subscribe(req)
        return protobuf_to_dict(res.ev)
