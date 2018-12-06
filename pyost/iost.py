import grpc

from pyost.api.rpc import apis_pb2_grpc, apis_pb2
from google.protobuf import empty_pb2
from protobuf_to_dict import protobuf_to_dict

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
        height_res = self._stub.GetHeight(empty_pb2.Empty())
        return height_res.height

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
        tx_res = self._stub.GetTxByHash(apis_pb2.HashReq(hash=tx_hash))
        return (protobuf_to_dict(tx_res.txRaw), tx_res.hash)

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
        tx_receipt_res = self._stub.GetTxReceiptByHash(apis_pb2.HashReq(hash=receipt_hash))
        return (protobuf_to_dict(tx_receipt_res.txReceiptRaw), tx_receipt_res.hash)

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
        tx_receipt_res = self._stub.GetTxReceiptByTxHash(apis_pb2.HashReq(hash=tx_hash))
        return (protobuf_to_dict(tx_receipt_res.txReceiptRaw), tx_receipt_res.hash)

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
    def get_block_by_hash(self, hash, complete=False):
        res = self._stub.GetBlockByHash(hash, complete)
        return res

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
    #
    def get_block_by_num(self, num, complete):
        res = self._stub.getBlockByNum(num, complete)
        return res

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
    #
    # message GetBalanceRes {
    # 	// the queried balance
    # 	int64 balance=1;
    # }
    #
    def get_balance(self, id, use_longest_chain):
        res = self._stub.GetBalance(id, use_longest_chain)
        return res

    # // get the Net ID
    # rpc GetNetID (google.protobuf.Empty) returns (GetNetIDRes) {
    #    option (google.api.http) = {
    #        get: "/getNetID"
    #    };
    # }
    # message GetNetIDRes {
    # 	string ID=1;
    # }
    #
    def get_net_id(self):
        res = self._stub.GetNetID(empty_pb2.Empty())
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
    #
    # message GetStateRes {
    # 	string value=1;
    # }
    #
    def get_state(self, key):
        res = self._stub.GetState(key)
        return res

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
    #
    # message SendRawTxRes {
    # 	// the hash of the received transaction
    # 	string hash=1;
    # }
    #
    def send_raw_tx(self, tx):
        res = self._stub.SendRawTx(tx)
        return res

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
    #
    # message GasRes {
    # 	uint64 gas=1;
    # }
    #
    def estimate_gas(self, tx):
        res = self._stub.EstimateGas(tx)
        return res

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
    #
    # message SubscribeRes {
    # 	event.Event ev=1;
    # }
    #
    def subscribe(self, req):
        res = self._stub.Subscribe(req)
        return res

