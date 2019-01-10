import time
from base58 import b58decode, b58encode
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair
from pyost.transaction import TransactionError

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    # Existing account that will pledge for the new account
    acc1_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    acc1_kp = KeyPair(Ed25519, acc1_seckey)
    acc1 = Account('iostsiri')
    acc1.add_key_pair(acc1_kp, 'active')
    acc1.add_key_pair(acc1_kp, 'owner')
    print(f'Account 1:\n{iost.get_account_info(acc1.name)}')

    # Create key pair for the new account
    acc2_kp = KeyPair(Ed25519)
    print('Do not forget to store the new account secret key:')
    print(b58encode(acc2_kp.seckey))
    acc2 = Account('iostsiri3')
    acc2.add_key_pair(acc2_kp, 'active')
    acc2.add_key_pair(acc2_kp, 'owner')

    tx = iost.create_new_account_tx(acc2.name, acc1.name,
                                    acc2_kp.id, acc2_kp.id, 0, 100.0, 100.0)
    tx.gas_limit = 1000000.0
    acc1.sign_publish(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.send_and_wait_tx(tx)
        print(receipt)
        print(iost.get_tx_by_hash(receipt.tx_hash))
    except TransactionError as e:
        print(f'Transaction error {e.status_code}: {e}')
    except TimeoutError as e:
        print(f'Timeout error: {e}')
