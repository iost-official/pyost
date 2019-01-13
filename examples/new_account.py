from base58 import b58decode, b58encode
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair
from pyost.transaction import TransactionError

if __name__ == '__main__':
    iost = IOST('localhost:30002')

    admin_seckey = b58decode(b'1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB')
    admin_kp = KeyPair(Ed25519, admin_seckey)
    admin = Account('producer01')
    admin.add_key_pair(admin_kp, 'active')
    admin.add_key_pair(admin_kp, 'owner')
    print(f'Admin:\n{iost.get_account_info(admin.name)}')

    # Create key pair for the new account
    acc2_kp = KeyPair(Ed25519)
    print('Do not forget to store the new account secret key:')
    print(b58encode(acc2_kp.seckey))
    acc2 = Account('testacc1')
    acc2.add_key_pair(acc2_kp, 'active')
    acc2.add_key_pair(acc2_kp, 'owner')

    tx = iost.create_new_account_tx(acc2.name, admin.name,
                                    b58encode(acc2_kp.pubkey),
                                    b58encode(acc2_kp.pubkey), 0, 100.0, 100.0)
    tx.gas_limit = 1000000.0
    admin.sign_publish(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.send_and_wait_tx(tx)
        print(receipt)
        print(iost.get_tx_by_hash(receipt.tx_hash))
    except TransactionError as e:
        print(f'Transaction error {e.status_code}: {e}')
    except TimeoutError as e:
        print(f'Timeout error: {e}')
