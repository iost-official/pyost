import time
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519, KeyPair

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    acc1_seckey = b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3'
    acc1_kp = KeyPair(Ed25519, acc1_seckey)
    acc1 = Account('iostsiri')
    acc1.add_key_pair(acc1_kp, 'active')
    acc1.add_key_pair(acc1_kp, 'owner')
    print(f'Account 1: {acc1}')
    print(f'Account 1 balance: {iost.get_balance(acc1.name)}')

    acc2_kp = KeyPair(Ed25519)

    tx = iost.new_account('iostsiri2', acc1.name, acc2_kp.id, acc2_kp.id, 1024, 1000)
    acc1.sign(tx, 'owner')
    acc1.sign_publish(tx)

    print('Signed transaction:')
    print(tx)

    tx_hash = iost.send_tx(tx)
    print(f'tx_hash={tx_hash}')

    while True:
        receipt = iost.get_tx_receipt_by_tx_hash(tx_hash)
        print(receipt)
        time.sleep(5)
