import grpc
import json
from base58 import b58decode, b58encode
from google.protobuf.empty_pb2 import Empty
from protobuf_to_dict import protobuf_to_dict
import protobuf_to_dict as ptd

from pyost.api.rpc import apis_pb2_grpc, apis_pb2
from pyost.api.core.event import event_pb2
from pyost.transaction import Transaction


class IOST():
    """
    This class provides API access to the IOST blockchain.
    """

    def __init__(self, url: str, timeout: int = 10,
                 gas_ratio: int = 1, gas_limit: int = 1000,
                 delay: int = 0, expiration: int = 90):
        """
        Connects to a node.

        Args:
            url (str): Node's IP address and port number.
            timeout (int): Number of seconds to wait when querying the node until timing out.
        """
        self.timeout = timeout
        self.gas_ratio = gas_ratio
        self.gas_limit = gas_limit
        self.delay = delay
        self.expiration = expiration
        self._channel = grpc.insecure_channel(url)
        self._stub = None

        try:
            grpc.channel_ready_future(self._channel).result(timeout=self.timeout)
        except grpc.FutureTimeoutError as e:
            raise ConnectionError('Error connecting to server') from e
        else:
            self._stub = apis_pb2_grpc.ApisStub(self._channel)

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

    def _parse_tx_raw(self, tx_raw) -> dict:
        """
        Converts a TxRaw proto object to a dict and encodes hashes to base58 string.

        Args:
            tx_raw (tx_pb2.TxRaw or dict): the TxRaw proto object to convert.

        Returns:
            dict: See ``get_tx_by_hash`` for the format.
        """
        tx = protobuf_to_dict(tx_raw) if not isinstance(tx_raw, dict) else tx_raw.copy()

        if 'signers ' in tx:
            tx['signers'] = [b58encode(signer) for signer in tx['signers']]
        if 'signs' in tx:
            tx['signs'] = [{
                'algorithm': sign['algorithm'],
                'sig': b58encode(sign['sig']),
                'pubKey': b58encode(sign['pubKey'])
            } for sign in tx['signs']]
        if 'publisher' in tx:
            tx['publisher']['sig'] = b58encode(tx['publisher']['sig'])
            tx['publisher']['pubKey'] = b58encode(tx['publisher']['pubKey'])

        return tx

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
                    'signers': [ bytes ],
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
        tx = self._parse_tx_raw(res.txRaw)
        return (tx, b58encode(res.hash))

    def _parse_receipt_raw(self, receipt_raw) -> dict:
        """
        Converts a TxReceiptRaw proto object to a dict and encodes hashes to base58 string.

        Args:
            receipt_raw (tx_pb2.TxReceiptRaw or dict): the TxReceiptRaw proto object to convert.

        Returns:
            dict: See ``get_tx_receipt_by_hash`` for the format.
        """
        receipt = protobuf_to_dict(receipt_raw) if not isinstance(receipt_raw, dict) else receipt_raw.copy()
        receipt['txHash'] = b58encode(receipt['txHash'])
        return receipt

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
        receipt = self._parse_receipt_raw(res.txReceiptRaw)
        return (receipt, b58encode(res.hash))

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
        receipt = self._parse_receipt_raw(res.txReceiptRaw)
        return (receipt, b58encode(res.hash))

    def _parse_block_info(self, block_info) -> dict:
        """
        Converts a BlockInfo proto object to a dict and encodes hashes to base58 string.

        Args:
            block_info (apis_pb2.BlockInfo or dict): the BlockInfo proto object to convert.

        Returns:
            dict: See ``get_block_by_hash`` for the format.
        """
        block = protobuf_to_dict(block_info) if not isinstance(block_info, dict) else block_info.copy()

        for hash in ['parentHash', 'txsHash' 'merkleHash']:
            if hash in block['head']:
                block['head'][hash] = b58encode(block['head'][hash])
        block['hash'] = b58encode(block['hash'])
        if 'txhash ' in block:
            block['txhash'] = [b58encode(tx) for tx in block['txhash']]
        if 'receiptHash ' in block:
            block['receiptHash'] = [b58encode(receipt) for receipt in block['receiptHash']]
        if 'txs' in block:
            block['txs'] = [self._parse_tx_raw(tx) for tx in block['txs']]
        if 'receipts' in block:
            block['receipts'] = [self._parse_receipt_raw(receipt) for receipt in block['receipts']]

        return block

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
            dict: Contains `txs` and `receipts` if `complete` is True,
                or only `txhash` and `receiptHash` if `complete` is False::

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
                    'txs': [ TxRaw (see return type of ``get_tx_by_hash``) ],
                    'receipts': [ TxReceiptRaw (see return type of ``get_tx_receipt_by_hash``) ]
                }
        """
        req = apis_pb2.BlockByHashReq(hash=block_hash, complete=complete)
        res = self._stub.GetBlockByHash(req)
        return self._parse_block_info(res)

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
            dict: Contains `txs` and `receipts` if `complete` is True,
                or only `txhash` and `receiptHash` if `complete` is False::

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
                    'txs': [ TxRaw (see return type of ``get_tx_by_hash``) ],
                    'receipts': [ TxReceiptRaw (see return type of ``get_tx_receipt_by_hash``) ]
                }
        """
        req = apis_pb2.BlockByNumReq(num=block_num, complete=complete)
        res = self._stub.getBlockByNum(req)
        return self._parse_block_info(res)

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

    def send_tx(self, tx: Transaction) -> str:
        """
        Sends a Transaction encoded as a TxRaw.

        Notes:
            REST API: POST "/sendRawTx" (tx in the body)

        Args:
            tx (Transaction): The transaction to serialize.

        Returns:
            str: The hash of the received transaction.
        """
        req = apis_pb2.RawTxReq(data=tx.encode())
        res = self._stub.SendRawTx(req)
        return res.hash

    def estimate_gas(self, tx: Transaction) -> int:
        """
        Estimates the gas required to send a Transaction.

        Notes:
            NOT SUPPORTED YET
            REST API: POST "/estimateGas" (tx in the body)

        Args:
            tx (Transaction): A Transaction that will be serialized to a TxRaw..

        Returns:
            str: The amount of gas required to execute a Transaction..
        """
        req = apis_pb2.RawTxReq(data=tx.encode())
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

    def call(self, contract, abi, args):
        tx = Transaction(self.gas_ratio, self.gas_limit, self.delay)
        tx.add_action(contract, abi, json.dumps(args))
        tx.set_time(90, 0)
        return tx

    def transfer(self, token, from_, to, amount, memo=''):
        return self.call('token.iost', 'Transfer', [token, from_, to, amount, memo])

    def new_account(self, name, creator, owner_key, active_key,
                    initial_ram, initial_gas_pledge):
        tx = Transaction(self.gas_ratio, self.gas_limit, self.delay)
        tx.add_action('auth.iost', 'SignUp', json.dumps([name, owner_key, active_key]))
        tx.add_action('ram.iost', 'buy', json.dumps([creator, name, initial_ram]))
        tx.add_action('gas.iost', 'pledge', json.dumps([creator, name, initial_gas_pledge + '']))
        tx.set_time(90, 0)
        return tx
