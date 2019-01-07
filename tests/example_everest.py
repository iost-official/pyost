import time
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Secp256k1, Ed25519
from pyost.signature import KeyPair
from base58 import b58decode, b58encode

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    acc1_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    acc1_kp = KeyPair(Ed25519, acc1_seckey)
    acc1 = Account('iostsiri')
    acc1.add_key_pair(acc1_kp, 'active')
    acc1.add_key_pair(acc1_kp, 'owner')
    print(f'Account 1:\n{iost.get_account_info(acc1.name)}')

    acc2_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    acc2_kp = KeyPair(Ed25519, acc1_seckey)
    acc2 = Account('iostsiri')
    acc2.add_key_pair(acc2_kp, 'active')
    acc2.add_key_pair(acc2_kp, 'owner')
    # print(f'Account 2:\n{iost.get_account(acc2)}')

    tx = iost.create_transfer_tx('iost', acc1.name, acc2.name, 1)
    acc1.sign_publish(tx)
    print(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.send_and_wait_tx(tx)
        print(f'Receipt status: {receipt.status_code}')
        print(receipt)

        print('Transaction:')
        print(iost.get_tx_by_hash(receipt.tx_hash))
    except TimeoutError as e:
        print(e)
    except RuntimeError as e:
        print(e)
