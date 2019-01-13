from base58 import b58decode
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Secp256k1, Ed25519
from pyost.signature import KeyPair
from pyost.transaction import TransactionError

if __name__ == '__main__':
    iost = IOST('localhost:30002')

    acc_seckey = b58decode(b'1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB')
    acc_kp = KeyPair(Ed25519, acc_seckey)
    acc = Account('admin')
    acc.add_key_pair(acc_kp, 'active')
    acc.add_key_pair(acc_kp, 'owner')

    print('Account Info:')
    print(iost.get_account_info(acc.name))

    print('\nToken Balance:')
    print(iost.get_token_balance(acc.name))

    print('\nToken 721 Balance:')
    print(iost.get_token721_balance(acc.name, 'iost'))

    tx = iost.create_call_tx('token.iost', 'supply', 'iost')
    acc.sign_publish(tx)
    try:
        receipt = iost.send_and_wait_tx(tx)
        print(f'IOST token balance: {receipt.returns[0]}')
    except TransactionError as e:
        print(f'Transaction error {e.status_code}: {e}')
