import grpc
import time
from typing import List, Type

from pyost.api.rpc.pb import rpc_pb2 as pb, rpc_pb2_grpc
from pyost.blockchain import Block, NodeInfo, ChainInfo, RAMInfo, GasRatio
from pyost.account import Account, AccountInfo, TokenBalance, Token721Balance
from pyost.transaction import Transaction, TxReceipt, TransactionError, Action
from pyost.contract import Contract
from pyost.signature import KeyPair
from pyost.algorithm import Algorithm, Ed25519
from pyost.event import Event, SubscribeRequest


class IOST:
    """
    This class provides API access to the IOST blockchain.
    """

    def __init__(self, url: str, timeout: int = 10,
                 gas_ratio: float = 1.0, gas_limit: float = 10000.0,
                 delay: int = 0, expiration: int = 90, default_limit='unlimited',
                 wait_time: int = 3, wait_max_retry: int = 10,
                 publisher: Account = None):
        """
        Connects to a node.

        Args:
            url (str): Node's IP address and port number.
            timeout (int): Number of seconds to wait when querying the node until timing out.
        """
        self.timeout: int = timeout
        self.gas_ratio: float = gas_ratio
        self.gas_limit: float = gas_limit
        self.delay: int = delay
        self.expiration: int = expiration
        self.default_limit: str = default_limit
        self.wait_time: int = wait_time
        self.wait_max_retry: int = wait_max_retry
        self.publisher: Account = publisher
        self._channel = grpc.insecure_channel(url)
        self._stub = None

        try:
            grpc.channel_ready_future(self._channel).result(timeout=self.timeout)
        except grpc.FutureTimeoutError as e:
            raise ConnectionError('Error connecting to server') from e
        else:
            self._stub = rpc_pb2_grpc.ApiServiceStub(self._channel)

    #             get: "/getNodeInfo"
    def get_node_info(self) -> NodeInfo:
        res: pb.NodeInfoResponse = self._stub.GetNodeInfo(pb.EmptyRequest())
        return NodeInfo().from_raw(res)

    #             get: "/getChainInfo"
    def get_chain_info(self) -> ChainInfo:
        res: pb.ChainInfoResponse = self._stub.GetChainInfo(pb.EmptyRequest())
        return ChainInfo().from_raw(res)

    #             get: "/getRAMInfo"
    def get_ram_info(self) -> RAMInfo:
        res: pb.RAMInfoResponse = self._stub.GetRAMInfo(pb.EmptyRequest())
        return RAMInfo().from_raw(res)

    def get_tx_by_hash(self, tx_hash: str) -> Transaction:
        """
        Gets a transaction by its hash value.

        Note:
            REST API: "/getTxByHash/{hash}"

        Args:
            tx_hash (str): The base58 hash string of the transaction.

        Returns:
            Transaction: a Transaction deserialized from pb.Transaction.
                the status attribute is set with the status code of pb.TransactionResponse.
        """
        req = pb.TxHashRequest(hash=tx_hash)
        res: pb.TransactionResponse = self._stub.GetTxByHash(req)
        tx = Transaction().from_raw(res.transaction)
        tx.status = Transaction.Status(res.status)
        return tx

    def get_tx_receipt_by_tx_hash(self, tx_hash: str) -> TxReceipt:
        """
        Gets a transaction receipt by its transaction hash value.

        Note:
            REST API: "/getTxReceiptByTxHash/{hash}"

        Args:
            tx_hash (str): The base58 hash string of the transaction.

        Returns:
            TxReceipt: a TxReceipt deserialized from pb.TxReceipt.
        """
        req = pb.TxHashRequest(hash=tx_hash)
        tr: pb.TxReceipt = self._stub.GetTxReceiptByTxHash(req)
        return TxReceipt().from_raw(tr)

    def get_block_by_hash(self, block_hash: str, complete: bool = False) -> Block:
        """
        Gets a block by its hash.

        Note:
            REST API: "/getBlockByHash/{hash}/{complete}"

        Args:
            block_hash: The base58 hash string of the block.
            complete: If True, returns the whole block, otherwise
                returns the head and the list of transaction and receipt hashes.

        Returns:
            Block: Contains a list of `transactions` if `complete` is True.
        """
        req = pb.GetBlockByHashRequest(hash=block_hash, complete=complete)
        res: pb.BlockResponse = self._stub.GetBlockByHash(req)
        return Block().from_raw(res.block, res.status)

    def get_block_by_num(self, block_num: int, complete: bool = False) -> Block:
        """
        Gets a block by its number.

        Note:
            REST API: "/getBlockByNumber/{number}/{complete}"

        Args:
            block_num: The number of the block.
            complete: If True, returns the whole block,
                otherwise returns the head and the list of transaction hashes.

        Returns:
            Block: Contains a list of `transactions` if `complete` is True.
        """
        req = pb.GetBlockByNumberRequest(number=block_num, complete=complete)
        res: pb.BlockResponse = self._stub.GetBlockByNumber(req)
        return Block().from_raw(res.block, res.status)

    # get: "/getAccount/{name}/{by_longest_chain}"
    def get_account_info(self, account_name: str, by_longest_chain: bool = False) -> AccountInfo:
        req = pb.GetAccountRequest(name=account_name, by_longest_chain=by_longest_chain)
        acc: pb.Account = self._stub.GetAccount(req)
        return AccountInfo().from_raw(acc)

    # get: "/getTokenBalance/{account}/{token}/{by_longest_chain}"
    def get_token_balance(self, account_name: str, token: str = 'iost', by_longest_chain: bool = False) -> TokenBalance:
        req = pb.GetTokenBalanceRequest(account=account_name, token=token, by_longest_chain=by_longest_chain)
        res: pb.GetTokenBalanceResponse = self._stub.GetTokenBalance(req)
        return TokenBalance().from_raw(res)

    def get_balance(self, account_name: str, token: str = 'iost', by_longest_chain: bool = False) -> float:
        return self.get_token_balance(account_name, token, by_longest_chain).balance

    # get: "/getToken721Balance/{account}/{token}/{by_longest_chain}"
    def get_token721_balance(self, account_name: str, token: str, by_longest_chain: bool = False) -> Token721Balance:
        req = pb.GetTokenBalanceRequest(account=account_name, token=token, by_longest_chain=by_longest_chain)
        res: pb.GetToken721BalanceResponse = self._stub.GetToken721Balance(req)
        return Token721Balance().from_raw(res)

    # get: "/getToken721Metadata/{token}/{token_id}/{by_longest_chain}"
    def get_token721_metadata(self, token: str, token_id: str, by_longest_chain: bool = False) -> str:
        req = pb.GetToken721InfoRequest(token=token, token_id=token_id, by_longest_chain=by_longest_chain)
        res: pb.GetToken721MetadataResponse = self._stub.GetToken721Metadata(req)
        return res.metadata

    # get: "/getToken721Owner/{token}/{token_id}/{by_longest_chain}"
    def get_token721_owner(self, token: str, token_id: str, by_longest_chain: bool = False) -> str:
        req = pb.GetToken721InfoRequest(token=token, token_id=token_id, by_longest_chain=by_longest_chain)
        res: pb.GetToken721OwnerResponse = self._stub.GetToken721Owner(req)
        return res.owner

    # get: "/getGasRatio"
    def get_gas_ratio(self) -> GasRatio:
        res: pb.GasRatioResponse = self._stub.GetGasRatio(pb.EmptyRequest())
        return GasRatio().from_raw(res)

    # get: "/getContract/{id}/{by_longest_chain}"
    def get_contract(self, id: str, by_longest_chain: bool = False) -> Contract:
        req = pb.GetContractRequest(id=id, by_longest_chain=by_longest_chain)
        res: pb.Contract = self._stub.GetContract(req)
        return Contract().from_raw(res)

    # post: "/getContractStorage"
    # body: "*"
    # return StateDB[key]
    # field needed if StateDB[key] is a map => StateDB[key][field]
    def get_contract_storage(self, id: str, key: str, field: str = '', by_longest_chain: bool = False) -> str:
        req = pb.GetContractStorageRequest(id=id, key=key, field=field, by_longest_chain=by_longest_chain)
        res: pb.GetContractStorageResponse = self._stub.GetContractStorage(req)
        return res.data

    # post: "/getContractStorageFields"
    # body: "*"
    def get_contract_storage_fields(self, id: str, fields: str = '', by_longest_chain: bool = False) -> str:
        req = pb.GetContractStorageFieldsRequest(id=id, fields=fields, by_longest_chain=by_longest_chain)
        res: pb.GetContractStorageFieldsResponse = self._stub.GetContractStorageFields(req)
        return res.data

    def send_tx(self, tx: Transaction) -> str:
        """
        Sends a Transaction encoded as a TransactionRequest.
        If the tx has no publisher set, signs the tx with the default publisher.

        Notes:
            REST API: POST "/sendTx" (tx in the body)

        Args:
            tx (Transaction): The transaction to serialize.

        Returns:
            str: The hash of the received transaction.
        """
        if tx.publisher == '':
            if self.publisher is None:
                raise ValueError('No publisher has signed the transaction.')
            self.publisher.sign_publish(tx)

        res: pb.SendTransactionResponse = self._stub.SendTransaction(tx.to_request_raw())
        return res.hash

    #     // execute transaction
    #     rpc ExecTransaction (TransactionRequest) returns (TxReceipt) {
    #         option (google.api.http) = {
    #             post: "/execTx"
    #             body: "*"
    #         };
    #     }
    #
    def exec_tx(self, tx: Transaction) -> TxReceipt:
        """
        Executes a Transaction encoded as a TransactionRequest.
        If the tx has no publisher set, signs the tx with the default publisher.

        Notes:
            REST API: POST "/execTx" (tx in the body)

        Args:
            tx (Transaction): The transaction to serialize.

        Returns:
            TxReceipt: The receipt of the transaction.
        """
        if tx.publisher is None:
            if self.publisher is None:
                raise ValueError('No publisher has signed the transaction.')
            self.publisher.sign_publish(tx)

        tr: pb.TxReceipt = self._stub.ExecTransaction(tx.to_request_raw())
        return TxReceipt().from_raw(tr)

    def send_and_wait_tx(self, tx: Transaction) -> TxReceipt:
        return self.wait_tx(self.send_tx(tx))

    def wait_tx(self, tx_hash: str, wait_time: int = None, max_retry: int = None, verbose=False) -> TxReceipt:
        wait_time = wait_time or self.wait_time
        max_retry = max_retry or self.wait_max_retry
        receipt = None
        tx = None

        for retry in range(max_retry):
            time.sleep(wait_time)
            try:
                tx = self.get_tx_by_hash(tx_hash)
            except Exception as e:
                if verbose:
                    print(e)

            if tx is not None:
                if tx.status == Transaction.Status.PENDING:
                    if verbose:
                        print('PENDING...')
                elif tx.status == Transaction.Status.PACKED or tx.status == Transaction.Status.IRREVERSIBLE:
                    if verbose:
                        print(tx.status.name)
                else:
                    raise TransactionError(f'Unknown transaction status: {tx.status.value}.')

            try:
                receipt = self.get_tx_receipt_by_tx_hash(tx_hash)
            except Exception as e:
                if verbose:
                    print(e)

            if receipt is not None:
                if verbose:
                    print(receipt)
                if receipt.status_code == TxReceipt.StatusCode.TIMEOUT:
                    raise TimeoutError(receipt.message)
                elif receipt.status_code != TxReceipt.StatusCode.SUCCESS:
                    raise TransactionError(receipt.message, receipt)
                else:
                    return receipt

        raise TimeoutError(f'Receipt cannot be found before {max_retry} trials.')

    # post: "/subscribe"
    def subscribe(self, topics: List[Event.Topic], contract_id: str = ''):
        sr = SubscribeRequest(topics, contract_id)
        for res in self._stub.Subscribe(sr.to_raw()):
            yield Event().from_raw(res.event)

    def create_tx(self, actions: List[Action] = None) -> Transaction:
        tx = Transaction(gas_limit=self.gas_limit, gas_ratio=self.gas_ratio,
                         expiration=self.expiration, delay=self.delay, actions=actions)
        tx.add_amount_limit('*', self.default_limit)
        return tx

    def create_call_tx(self, contract: str, abi: str, *args) -> Transaction:
        return self.create_tx(actions=[Action(contract, abi, *args)])

    def create_transfer_tx(self, token: str, from_name: str, to_name: str, amount: float, memo='') -> Transaction:
        tx = self.create_call_tx('token.iost', 'transfer', token, from_name, to_name, str(amount), memo)
        tx.add_amount_limit('iost', str(amount))
        return tx

    def create_new_account_tx(self, new_name: str, creator_name: str,
                              owner_kpid: str, active_kpdid: str,
                              initial_ram: int = 0, initial_gas_pledge: float = 11.0,
                              initial_coins: float = 0.0) -> Transaction:
        tx = self.create_tx()
        tx.add_action('auth.iost', 'SignUp', new_name, owner_kpid, active_kpdid)
        if initial_ram > 0:
            tx.add_action('ram.iost', 'buy', creator_name, new_name, initial_ram)
        if initial_gas_pledge <= 10.0:
            raise ValueError('minimum gas pledge is 10.0')
        tx.add_action('gas.iost', 'pledge', creator_name, new_name, str(initial_gas_pledge - 10.0))
        if initial_coins > 0.0:
            tx.add_action('token.iost', 'transfer', 'iost', creator_name, new_name, str(initial_coins), '')
        return tx

    def call(self, contract: str, abi: str, *args) -> TxReceipt:
        tx = self.create_call_tx(contract, abi, *args)
        return self.send_and_wait_tx(tx)

    def transfer(self, token: str, from_name: str, to_name: str, amount: int, memo='') -> TxReceipt:
        tx = self.create_transfer_tx(token, from_name, to_name, amount, memo)
        return self.send_and_wait_tx(tx)

    def new_account(self, new_name: str, creator_name: str,
                    initial_ram: int = 0, initial_gas_pledge: float = 11.0,
                    initial_coins: float = 0.0, algo_cls: Type[Algorithm] = Ed25519) -> Account:
        account = Account(new_name)
        kp = KeyPair(algo_cls)
        account.add_key_pair(kp, 'owner')
        account.add_key_pair(kp, 'active')

        tx = self.create_new_account_tx(new_name, creator_name,
                                        account.get_key_pair('owner').id, account.get_key_pair('active').id,
                                        initial_ram, initial_gas_pledge, initial_coins)
        self.send_and_wait_tx(tx)
        return account
