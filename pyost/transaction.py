from typing import List
from time import time_ns

from pyost.api.core.tx import tx_pb2


class Action():
    def __init__(self, contract: str, name: str, data: str):
        self.contract = contract
        self.name = name
        self.data = data

    def encode(self) -> bytes:
        ar = tx_pb2.ActionRaw(contract=self.contract, actionName=self.name, data=self.data)
        return ar.SerializeToString()

    def decode(self, data: bytes) -> None:
        ar = tx_pb2.ActionRaw()
        ar.ParseFromString(data)
        self.contract = ar.contract
        self.name = ar.actionName
        self.data = ar.data

class Transaction():
    def __init__(self, actions: List[Action] = None, signers: List[bytes] = None,
                 gas_limit: int = 1000, gas_price: int = 1, expiration: int = 0):
        self.hash = None
        self.time = time_ns()
        self.expiration = expiration
        self.gas_limit = gas_limit
        self.gas_price = gas_price
        self.actions = actions
        self.signers = signers
        self.signs = []
        self.publisher = Signature()

    # message ActionRaw {
    #     string contract = 1;
    #     string actionName = 2;
    #     string data = 3;
    # }
    #
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

    def encode(self) -> bytes:
        tx = tx_pb2.TxRaw(time=self.now)
        return tx.SerializeToString()

# class Tx {
#     constructor(gasRatio, gasLimit) {
#         this.gasRatio = gasRatio;
#         this.gasLimit = parseInt(gasLimit);
#         this.actions = [];
#         this.signers = [];
#         this.signs = [];
#         this.publisher = "";
#         this.publisher_sigs = [];
#         this.amount_limit = [];
#     }
#
#     addSigner(name, permission) {
#         this.signers.push(name+"@"+permission)
#     }
#
#     addLimit(token, amount) {
#         this.amount_limit.push({
#             token: token,
#             value: amount,
#         })
#     }
#
#     addAction(contract, abi, args) {
#         this.actions.push({
#             contract: contract,
#             actionName: abi,
#             data: args,
#         })
#     }
#
#     setTime(expirationInSecound, delay) {
#         let date = new Date();
#         this.time = date.getTime() * 1e6;
#         this.expiration = this.time + expirationInSecound * 1e9;
#         this.delay = delay;
#     }
#
#     _base_hash() {
#         const hash = sha3.SHA3(256);
#         hash.update(this._bytes(0));
#         return hash.digest("binary");
#     }
#
#     addSign(kp) {
#         const sig = new Signature(this._base_hash(), kp);
#         this.signs.push(sig)
#     }
#
#     _publish_hash() {
#         const hash = sha3.SHA3(256);
#         hash.update(this._bytes(1));
#         return hash.digest("binary");
#     }
#
#     addPublishSign(publisher, kp) {
#         this.publisher = publisher;
#         const info = this._publish_hash();
#         const sig = new Signature(info, kp);
#         this.publisher_sigs.push(sig)
#     }
#
#     _bytes(n) {
#         let c = new Codec();
#         c.pushInt64(this.time);
#         c.pushInt64(this.expiration);
#         c.pushInt64(parseInt(this.gasRatio*100));
#         c.pushInt64(this.gasLimit*100);
#         c.pushInt64(this.delay);
#         c.arrayStart();
#         for (let i = 0; i < this.signers.length; i++) {
#             c.pushString(this.signers[i])
#         }
#         c.arrayEnd();
#         c.arrayStart();
#         for (let i = 0; i < this.actions.length; i++) {
#             let c2 = new Codec();
#             c2.pushString(this.actions[i].contract);
#             c2.pushString(this.actions[i].actionName);
#             c2.pushString(this.actions[i].data);
#             c.pushBytes(c2._buf)
#         }
#         c.arrayEnd();
#         c.arrayStart();
#         for (let i = 0; i < this.amount_limit.length; i++) {
#             let c2 = new Codec();
#             c2.pushString(this.amount_limit[i].token);
#             c2.pushString(this.amount_limit[i].value+"");
#             c.pushBytes(c2._buf)
#         }
#         c.arrayEnd();
#
#         if (n > 0) {
#             c.arrayStart();
#             for (let i = 0; i < this.signs.length; i++) {
#                 c.pushBytes(this.signs[i]._bytes())
#             }
#             c.arrayEnd();
#         }
#
#         if (n > 1) {
#             // todo
#         }
#         return c._buf
#     }
# }
