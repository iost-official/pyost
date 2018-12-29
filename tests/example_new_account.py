from pyost.iost import IOST
from pyost.account import Account, get_id_by_pubkey, get_pubkey_by_id
from pyost.transaction import Transaction
from pyost import algorithm
from time import sleep

if __name__ == '__main__':
    pubkey = 'FMR2ZmpYjTD6kJWeqEAP69VDzRXF8uNSQLaN7FTyLJZ1'
    id = get_id_by_pubkey(pubkey)
    pubkey_from_id = get_pubkey_by_id(id)
    print(id)
    print(pubkey_from_id)

    iost = IOST('192.168.99.100:30002')

    node_seckey = '1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB'
    node_account = Account(node_seckey, algorithm.Ed25519)

    account = Account()
    tx = iost.new_account('account1', 'Siri', node_account.id, node_account.id, 1024, 10)
    node_account.sign_tx(tx)
    tx.verify_self()
    tx_res = iost.send_tx(tx)
    print(f'Transaction status: {tx_res.status}')

    sleep(5)
    try:
        tx_res = iost.get_tx_by_hash(tx.hash)
        print(tx_res)
    except Exception as err:
        print(err)

    print(f'Account balance: {iost.get_balance(account.id)}')
