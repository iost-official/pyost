import grpc
import time
from typing import List, Type
from collections import Iterable
from base58 import b58encode

from pyost.rpc.pb import rpc_pb2 as pb, rpc_pb2_grpc
from pyost.blockchain import Block, NodeInfo, ChainInfo, RAMInfo, GasRatio
from pyost.account import Account, AccountInfo, TokenBalance, Token721Balance
from pyost.transaction import Transaction, TxReceipt, TransactionError, Action
from pyost.contract import Contract
from pyost.signature import KeyPair
from pyost.algorithm import Algorithm, Ed25519
from pyost.event import Event, SubscribeRequest


class IOST:
    """Connects to an IOST node and provides access to the blockchain's API via RPC calls.

    Attributes:
        url: The URL of the node including port number, such as ``localhost:30002``.
        timeout: How many seconds to wait before raising a ConnectionError when attempting to establish a connection.
        gas_ratio: The gas ratio, default is 1.0.
        gas_limit: The maximum amount of gas that can be used to execute a transaction.
        delay: When to execute the transaction, default 0 means now.
        expiration: When the transaction expires, in seconds from now.
        default_limit: The limit of amount of coins, default ``unlimited``.
        publisher: The `Account` that will be used by default to sign transaction that have no publisher.

    Raises:
        ConnectionError: If the connection cannot be established before `timeout` seconds.
    """

    def __init__(self, url: str, timeout: int = 10,
                 gas_ratio: float = 1.0, gas_limit: float = 10000.0,
                 delay: int = 0, expiration: int = 90, default_limit='unlimited',
                 wait_time: int = 3, wait_max_retry: int = 10,
                 publisher: Account = None,
                 chain_id: int = 1024):
        self.timeout: int = timeout
        self.gas_ratio: float = gas_ratio
        self.gas_limit: float = gas_limit
        self.delay: int = delay
        self.expiration: int = expiration
        self.default_limit: str = default_limit
        self.wait_time: int = wait_time
        self.wait_max_retry: int = wait_max_retry
        self.publisher: Account = publisher
        self.chain_id: int = chain_id
        self._channel = grpc.insecure_channel(url)
        self._stub = None

        try:
            grpc.channel_ready_future(self._channel).result(timeout=self.timeout)
        except grpc.FutureTimeoutError as e:
            raise ConnectionError('Error connecting to server') from e
        else:
            self._stub = rpc_pb2_grpc.ApiServiceStub(self._channel)

    def get_node_info(self) -> NodeInfo:
        """Gets information about the node.

        Note::
            REST API: GET "/getNodeInfo"

        Returns:
            A `NodeInfo` object.
        """
        res: pb.NodeInfoResponse = self._stub.GetNodeInfo(pb.EmptyRequest())
        return NodeInfo().from_raw(res)

    def get_chain_info(self) -> ChainInfo:
        """Gets information about the blockchain.

        Note:
            REST API: GET "/getChainInfo"

        Returns:
            A `ChainInfo` object.
        """
        res: pb.ChainInfoResponse = self._stub.GetChainInfo(pb.EmptyRequest())
        return ChainInfo().from_raw(res)

    def get_ram_info(self) -> RAMInfo:
        """Gets information about the RAM on the blockchain.

        Note:
            REST API: GET "/getRAMInfo"

        Returns:
            A `RAMInfo` object.
        """

        res: pb.RAMInfoResponse = self._stub.GetRAMInfo(pb.EmptyRequest())
        return RAMInfo().from_raw(res)

    def get_tx_by_hash(self, tx_hash: str) -> Transaction:
        """Gets a `Transaction` by its hash value.

        Note:
            REST API: GET "/getTxByHash/{hash}"

        Args:
            tx_hash: The base58 hash string of the transaction.

        Returns:
            A `Transaction` deserialized from `pb.Transaction`.
                The status attribute is set with the status code of `pb.TransactionResponse`.
        """
        req = pb.TxHashRequest(hash=tx_hash)
        res: pb.TransactionResponse = self._stub.GetTxByHash(req)
        tx = Transaction().from_raw(res.transaction)
        tx.status = Transaction.Status(res.status)
        return tx

    def get_tx_receipt_by_tx_hash(self, tx_hash: str) -> TxReceipt:
        """Gets a transaction receipt by its transaction's hash value.

        Note:
            REST API: GET "/getTxReceiptByTxHash/{hash}"

        Args:
            tx_hash: The base58 hash string of the transaction.

        Returns:
            TxReceipt: a `TxReceipt` deserialized from `pb.TxReceipt`.
        """
        req = pb.TxHashRequest(hash=tx_hash)
        tr: pb.TxReceipt = self._stub.GetTxReceiptByTxHash(req)
        return TxReceipt().from_raw(tr)

    def get_block_by_hash(self, block_hash: str, complete: bool = False) -> Block:
        """Gets a block by its hash value.

        Note:
            REST API: GET "/getBlockByHash/{hash}/{complete}"

        Args:
            block_hash: The base58 hash string of the block.
            complete: If True, returns the whole block, otherwise
                returns only the list of transaction and receipt hashes.

        Returns:
            Block: A `Block` object that contains a list of `Transactions` if `complete` is True.
        """
        req = pb.GetBlockByHashRequest(hash=block_hash, complete=complete)
        res: pb.BlockResponse = self._stub.GetBlockByHash(req)
        return Block().from_raw(res.block, res.status)

    def get_block_by_num(self, block_num: int, complete: bool = False) -> Block:
        """Gets a block by its number.

        Note:
            REST API: GET "/getBlockByNumber/{number}/{complete}"

        Args:
            block_num: The number of the block.
            complete: If True, returns the whole block, otherwise
                returns only the list of transaction and receipt hashes.

        Returns:
            Block: A `Block` object that contains a list of `Transactions` if `complete` is True.
        """
        req = pb.GetBlockByNumberRequest(number=block_num, complete=complete)
        res: pb.BlockResponse = self._stub.GetBlockByNumber(req)
        return Block().from_raw(res.block, res.status)

    def get_account_info(self, account_name: str, by_longest_chain: bool = False) -> AccountInfo:
        """Gets information about an account.

        Note:
            REST API: GET "/getAccount/{name}/{by_longest_chain}"

        Args:
            account_name: The name of the account.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            An `AccountInfo` object.
        """
        req = pb.GetAccountRequest(name=account_name, by_longest_chain=by_longest_chain)
        acc: pb.Account = self._stub.GetAccount(req)
        return AccountInfo().from_raw(acc)

    def get_token_balance(self, account_name: str, token: str = 'iost', by_longest_chain: bool = False) -> TokenBalance:
        """Gets an account's token balance.

        Note:
            REST API: GET "/getTokenBalance/{account}/{token}/{by_longest_chain}"

        Args:
            account_name: The name of the account.
            token: The name of the token, default ``iost``.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            A `TokenBalance` object.
        """
        req = pb.GetTokenBalanceRequest(account=account_name, token=token, by_longest_chain=by_longest_chain)
        res: pb.GetTokenBalanceResponse = self._stub.GetTokenBalance(req)
        return TokenBalance().from_raw(res)

    def get_balance(self, account_name: str, token: str = 'iost', by_longest_chain: bool = False) -> float:
        """Helper function for `get_token_balance`.

        Note:
            REST API: GET "/getTokenBalance/{account}/{token}/{by_longest_chain}"

        Args:
            account_name: The name of the account.
            token: The name of the token, default ``iost``.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            The token balance of the account (`TokenBalance` object's `balance` field).
        """
        return self.get_token_balance(account_name, token, by_longest_chain).balance

    def get_token721_balance(self, account_name: str, token: str, by_longest_chain: bool = False) -> Token721Balance:
        """Gets an account's ERC721 token balance.

        Note:
            REST API: GET "/getToken721Balance/{account}/{token}/{by_longest_chain}"

        Args:
            account_name: The name of the account.
            token: The name of the token.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            A `Token721Balance` object.
        """
        req = pb.GetTokenBalanceRequest(account=account_name, token=token, by_longest_chain=by_longest_chain)
        res: pb.GetToken721BalanceResponse = self._stub.GetToken721Balance(req)
        return Token721Balance().from_raw(res)

    def get_token721_metadata(self, token: str, token_id: str, by_longest_chain: bool = False) -> str:
        """Gets an ERC721 token's metadata.

        Note:
            REST API: GET "/getToken721Metadata/{token}/{token_id}/{by_longest_chain}"

        Args:
            token: The name of the token.
            token_id: The id of the token.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            The metadata of the token as a string.
        """
        req = pb.GetToken721InfoRequest(token=token, token_id=token_id, by_longest_chain=by_longest_chain)
        res: pb.GetToken721MetadataResponse = self._stub.GetToken721Metadata(req)
        return res.metadata

    def get_token721_owner(self, token: str, token_id: str, by_longest_chain: bool = False) -> str:
        """Gets an ERC721 token owner's name.

        Note:
            REST API: GET "/getToken721Owner/{token}/{token_id}/{by_longest_chain}"

        Args:
            token: The name of the token.
            token_id: The id of the token.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            The token owner's name.
        """
        req = pb.GetToken721InfoRequest(token=token, token_id=token_id, by_longest_chain=by_longest_chain)
        res: pb.GetToken721OwnerResponse = self._stub.GetToken721Owner(req)
        return res.owner

    def get_gas_ratio(self) -> GasRatio:
        """Gets the gas ratio used on the blockchain.

        Note:
            REST API: GET "/getGasRatio"

        Returns:
            A `GasRatio` object.
        """
        res: pb.GasRatioResponse = self._stub.GetGasRatio(pb.EmptyRequest())
        return GasRatio().from_raw(res)

    def get_contract(self, id: str, by_longest_chain: bool = False) -> Contract:
        """Gets information about a contract.

        Note:
            REST API: GET "/getContract/{id}/{by_longest_chain}"

        Args:
            id: The contract id.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            A `Contract` object.
        """
        req = pb.GetContractRequest(id=id, by_longest_chain=by_longest_chain)
        res: pb.Contract = self._stub.GetContract(req)
        return Contract().from_raw(res)

    def get_contract_storage(self, id: str, key: str, field: str = '', by_longest_chain: bool = False) -> str:
        """Gets a contract's stored data from the ``StateDB``.

        Note:
            REST API: POST "/getContractStorage"
            body: "*"

        Args:
            id: The contract id.
            key: The key of the value to retrieve.
            field: If `StateDB[key]` is a map, returns `StateDB[key][field]`.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            `StateDB[key]` or `StateDB[key][field]` as a string.
        """
        req = pb.GetContractStorageRequest(id=id, key=key, field=field, by_longest_chain=by_longest_chain)
        res: pb.GetContractStorageResponse = self._stub.GetContractStorage(req)
        return res.data

    def get_contract_storage_fields(self, id: str, fields: str = '', by_longest_chain: bool = False) -> str:
        """Gets a contract's data from the ``StateDB``.

        Note:
            REST API: POST "/getContractStorageFields"
            body: "*"

        Args:
            id: The contract id.
            fields: List of fields to retrieve.
            by_longest_chain: If True, gets data from the longest chain's head block or last irreversible block.

        Returns:
            A string.
        """
        req = pb.GetContractStorageFieldsRequest(id=id, fields=fields, by_longest_chain=by_longest_chain)
        res: pb.GetContractStorageFieldsResponse = self._stub.GetContractStorageFields(req)
        return res.data

    def send_tx(self, tx: Transaction) -> str:
        """Sends a `Transaction` serialized as a `TransactionRequest`.
        If the `Transaction` has no publisher set, signs it with the default `publisher`.

        Notes:
            REST API: POST "/sendTx" (tx in the body)

        Args:
            tx: The `Transaction` to serialize.

        Returns:
            The hash value of the `Transaction` received by the node.
        """
        if tx.publisher == '':
            if self.publisher is None:
                raise ValueError('No publisher has signed the transaction.')
            self.publisher.sign_publish(tx)

        res: pb.SendTransactionResponse = self._stub.SendTransaction(tx.to_request_raw())
        return res.hash

    def exec_tx(self, tx: Transaction) -> TxReceipt:
        """Executes a `Transaction` serialized as a `TransactionRequest`.
        If the `Transaction` has no publisher set, signs it with the default `publisher`.

        Note:
            REST API: POST "/execTx" (tx in the body)

        Args:
            tx: The `Transaction` to serialize.

        Returns:
            The receipt of the transaction as a `TxReceipt` object.
        """
        if tx.publisher is None:
            if self.publisher is None:
                raise ValueError('No publisher has signed the transaction.')
            self.publisher.sign_publish(tx)

        tr: pb.TxReceipt = self._stub.ExecTransaction(tx.to_request_raw())
        return TxReceipt().from_raw(tr)

    def send_and_wait_tx(self, tx: Transaction) -> TxReceipt:
        """Helper functions that combines `send_tx` and `wait_tx`.

        Args:
            tx: The `Transaction` to send.

        Returns:
            The receipt of the `Transaction` as a `TxReceipt` object.

        Raises:
            TransactionError: If Transaction.Status is unknown or if TxReceipt.StatusCode is not SUCCESS.
            TimeoutError: If TxReceipt.StatusCode is TIMEOUT
                or no transaction can be found after `wait_time` x `wait_max_retry` have passed.
        """
        return self.wait_tx(self.send_tx(tx))

    def wait_tx(self, tx_hash: str, wait_time: int = None, max_retry: int = None, verbose=False) -> TxReceipt:
        """Polls for a Transaction's receipt by calling `get_tx_by_hash` and `get_tx_receipt_by_tx_hash`.

        Args:
            tx_hash: The hash value of the `Transaction` to poll.
            wait_time: The number of seconds to sleep between two trials, by default it is the class member `wait_time`.
            max_retry: The number of trials to attempt before raising a TimeoutError, by default it is the class member `wait_max_retry`.
            verbose: If True, displays log messages for each attempt.

        Returns:
            The receipt of the `Transaction` as a `TxReceipt` object.

        Raises:
            TransactionError: If Transaction.Status is unknown or if TxReceipt.StatusCode is not SUCCESS.
            TimeoutError: If TxReceipt.StatusCode is TIMEOUT
                or no transaction can be found after `wait_time` x `wait_max_retry` have passed.
        """
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
    def subscribe(self, topics: List[Event.Topic], contract_id: str = '') -> Iterable:
        """Subscribes to a list of topics.

        Args:
            topics: A list of `Event.Topic` to listen to.
            contract_id: A filter to only listen to the events of a particular contract.

        Yields:
            Returns the `Events` one by one.

        Example:
            >>> for event in iost.subscribe(topics, contract_id):
            >>>     print(event)
        """
        sr = SubscribeRequest(topics, contract_id)
        for res in self._stub.Subscribe(sr.to_raw()):
            yield Event().from_raw(res.event)

    def create_tx(self, actions: List[Action] = None) -> Transaction:
        """Creates a `Transaction` with default values from this class members.

        Args:
            actions: A list of `Actions`.

        Returns:
            A `Transaction` object.
        """
        tx = Transaction(gas_limit=self.gas_limit, gas_ratio=self.gas_ratio,
                         expiration=self.expiration, delay=self.delay, actions=actions,
                         chain_id=self.chain_id)
        tx.add_amount_limit('*', self.default_limit)
        return tx

    def create_call_tx(self, contract: str, abi: str, *args) -> Transaction:
        """Creates a `Transaction` that contains an `Action` to call an abi.

        Args:
            contract: The name of the contract.
            abi: The name of the abi to call.
            *args: The arguments to pass to the abi.

        Returns:
            A `Transaction` object.
        """
        return self.create_tx(actions=[Action(contract, abi, *args)])

    def create_publish_tx(self, contract: Contract) -> Transaction:
        """Creates a `Transaction` that contains an `Action` to publish a contract.

        Args:
            contract: The contract to be published.

        Returns:
            A `Transaction` object.
        """
        return self.create_call_tx('system.iost', 'setCode', contract.to_json())

    def create_transfer_tx(self, token: str, from_name: str, to_name: str, amount: float, memo='') -> Transaction:
        """Creates a `Transaction` that contains an `Action` to transfer tokens between accounts.

        Args:
            token: The name of the token.
            from_name: The account name to send tokens from.
            to_name: The account name to send tokens to.
            amount: The amount of tokens to send.
            memo: A text to add to the transaction.

        Returns:
            A `Transaction` object.
        """
        tx = self.create_call_tx('token.iost', 'transfer', token, from_name, to_name, str(amount), memo)
        tx.add_amount_limit('iost', str(amount))
        return tx

    def create_new_account_tx(self, new_name: str, creator_name: str,
                              owner_key: str, active_key: str,
                              initial_ram: int = 0, initial_gas_pledge: float = 11.0,
                              initial_coins: float = 0.0) -> Transaction:
        """Creates a `Transaction` that contains a list of `Actions` to create an account,
            pledge tokens, buy RAM and transfer coins to the new account.

        Args:
            new_name: The name of the account to create.
            creator_name: The name of the account that will pledge tokens to the new account.
            owner_key: The id of the ``owner`` `KeyPair` of the new account.
            active_key: The id of the ``active`` `KeyPair` of the new account.
            initial_ram: The amount of RAM to buy for the new account.
            initial_gas_pledge: The amount of tokens to pledge for the new account.
            initial_coins: The amount of coins to transfer to the new account.

        Returns:
            A `Transaction` object.
        """
        tx = self.create_tx()
        tx.add_action('auth.iost', 'signUp', new_name, owner_key, active_key)
        if initial_ram > 0:
            tx.add_action('ram.iost', 'buy', creator_name, new_name, initial_ram)
        if initial_gas_pledge <= 10.0:
            raise ValueError('minimum gas pledge is 10.0')
        tx.add_action('gas.iost', 'pledge', creator_name, new_name, str(initial_gas_pledge - 10.0))
        if initial_coins > 0.0:
            tx.add_action('token.iost', 'transfer', 'iost', creator_name, new_name, str(initial_coins), '')
        return tx

    def call(self, contract: str, abi: str, *args) -> TxReceipt:
        """Helper function that combines `create_transfer_tx` and `send_and_wait_tx`.
        Creates a `Transaction` that contains an `Action` to call an abi, then send it.

        Args:
            contract: The name of the contract.
            abi: The name of the abi to call.
            *args: The arguments to pass to the abi.

        Returns:
            The receipt of the `Transaction` as a `TxReceipt` object.

        Raises:
            TransactionError: If Transaction.Status is unknown or if TxReceipt.StatusCode is not SUCCESS.
            TimeoutError: If TxReceipt.StatusCode is TIMEOUT
                or no transaction can be found after `wait_time` x `wait_max_retry` have passed.
        """
        tx = self.create_call_tx(contract, abi, *args)
        return self.send_and_wait_tx(tx)

    def publish(self, contract: Contract) -> TxReceipt:
        """Creates a `Transaction` that contains an `Action` to publish a contract, then sends it.

        Args:
            contract: The contract to be published.

        Returns:
            The receipt of the `Transaction` as a `TxReceipt` object.

        Raises:
            TransactionError: If Transaction.Status is unknown or if TxReceipt.StatusCode is not SUCCESS.
            TimeoutError: If TxReceipt.StatusCode is TIMEOUT
                or no transaction can be found after `wait_time` x `wait_max_retry` have passed.
        """
        tx = self.create_publish_tx(contract)
        return self.send_and_wait_tx(tx)

    def transfer(self, token: str, from_name: str, to_name: str, amount: int, memo='') -> TxReceipt:
        """Helper function that combines `create_transfer_tx` and `send_and_wait_tx`.
        Creates a `Transaction` that contains an `Action` to transfer tokens between accounts, then sends it.

        Args:
            token: The name of the token.
            from_name: The account name to send tokens from.
            to_name: The account name to send tokens to.
            amount: The amount of tokens to send.
            memo: A text to add to the transaction.

        Returns:
            The receipt of the `Transaction` as a `TxReceipt` object.

        Raises:
            TransactionError: If Transaction.Status is unknown or if TxReceipt.StatusCode is not SUCCESS.
            TimeoutError: If TxReceipt.StatusCode is TIMEOUT
                or no transaction can be found after `wait_time` x `wait_max_retry` have passed.
        """
        tx = self.create_transfer_tx(token, from_name, to_name, amount, memo)
        return self.send_and_wait_tx(tx)

    def new_account(self, new_name: str, creator_name: str,
                    initial_ram: int = 0, initial_gas_pledge: float = 11.0,
                    initial_coins: float = 0.0, algo_cls: Type[Algorithm] = Ed25519) -> Account:
        """Helper function that combines `KeyPair` and `Account` creation then calls to `create_new_account_tx` and `send_and_wait_tx`.

        Creates an `Account` with new ``owner`` and ``active`` `KeyPair`, then
            creates a `Transaction` that contains a list of `Actions` to create an account,
            pledge tokens, buy RAM and transfer coins to the new account, and finally sends it.

        Args:
            new_name: The name of the account to create.
            creator_name: The name of the account that will pledge tokens to the new account.
            initial_ram: The amount of RAM to buy for the new account.
            initial_gas_pledge: The amount of tokens to pledge for the new account.
            initial_coins: The amount of coins to transfer to the new account.
            algo_cls: The class type of the `Algorithm` to use to generate the `KeyPair`.

        Returns:
            A `Account` object.

        Raises:
            TransactionError: If Transaction.Status is unknown or if TxReceipt.StatusCode is not SUCCESS.
            TimeoutError: If TxReceipt.StatusCode is TIMEOUT
                or no transaction can be found after `wait_time` x `wait_max_retry` have passed.
        """
        account = Account(new_name)
        kp = KeyPair(algo_cls)
        account.add_key_pair(kp, 'owner')
        account.add_key_pair(kp, 'active')

        tx = self.create_new_account_tx(new_name, creator_name,
                                        b58encode(account.get_key_pair('owner').pubkey),
                                        b58encode(account.get_key_pair('active').pubkey),
                                        initial_ram, initial_gas_pledge, initial_coins)
        self.send_and_wait_tx(tx)
        return account
