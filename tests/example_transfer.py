from pyost.iost import IOST
from pyost.account import Account
from pyost.transaction import Transaction
from pyost import algorithm
from time import sleep

if __name__ == '__main__':
    iost = IOST('192.168.99.100:30002')

    node_seckey = '1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB'
    node_account = Account(node_seckey, algorithm.Ed25519)
    print(f'Node pubkey: {node_account.pubkey}')
    print(f'Node balance: {iost.get_balance(node_account.id)}')

    seckey1 = '3gLThtqcsJS4zgtXkfUksY9XM6pUXSM3mC6fZb9PkHURg171gsrpLXBtapme7Kwx24xi6qkE55CZaH7iBa5kWjNC'
    account1 = Account(seckey1, algorithm.Ed25519)
    print(f'Account 1 pubkey: {account1.pubkey}')
    print(f'Account 1 balance: {iost.get_balance(account1.pubkey)}')

    seckey2 = '3vFoZPT1c3FSNVa9qrYMa2SQyxNQ8dfLSySNSzWokZQb4U1HToW1qUL3XzhpDE66MnjeUGwSDrYDJYgDFUary4Mb'
    account2 = Account(seckey2, algorithm.Ed25519)
    print(f'Account 2 pubkey: {account2.pubkey}')
    print(f'Account 2 balance: {iost.get_balance(account2.pubkey)}')

    tx = iost.transfer(account1.pubkey, account1.pubkey, 1)
    tx.gas_limit = 1
    tx.gas_price = 1
    #tx.add_signer(account1.pubkey)
    #account1.sign_tx_content(tx)
    account1.sign_tx(tx)
    tx.verify_self()

    tx_res = iost.send_tx(tx)
    print(f'Transaction status: {tx_res.status}')

    sleep(5)
    try:
        tx_res = iost.get_tx_by_hash(tx_res._hash)
        print(tx_res)
    except Exception as err:
        print(err)

    print(f'Account 1 balance: {iost.get_balance(account1.pubkey)}')
    print(f'Account 2 balance: {iost.get_balance(account2.pubkey)}')
