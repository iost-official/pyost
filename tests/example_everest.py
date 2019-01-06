import time
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Secp256k1, Ed25519
from pyost.signature import KeyPair
from base58 import b58decode

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    acc1_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    acc1_kp = KeyPair(Ed25519, acc1_seckey)
    acc1 = Account('iostsiri')
    acc1.add_key_pair(acc1_kp, 'active')
    acc1.add_key_pair(acc1_kp, 'owner')
    # print(acc1_kp)
    # print(f'Account 1:\n{iost.get_account(acc1.name)}')

    acc2_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    acc2_kp = KeyPair(Ed25519, acc1_seckey)
    acc2 = Account('iostsiri')
    acc2.add_key_pair(acc2_kp, 'active')
    acc2.add_key_pair(acc2_kp, 'owner')
    print(f'Account 2:\n{iost.get_account(acc2.name)}')

    tx = iost.transfer('iost', acc1.name, acc2.name, '1')
    #print(tx.to_bytes(level='publish'))
    #tx.add_signer('iostsiri', 'active')
    #acc1.sign(tx)
    acc1.sign_publish(tx)

    print('Signed transaction:')
    print(tx)

    tx_hash = iost.send_tx(tx)
    print(f'tx_hash={tx_hash}')

    while True:
        receipt = iost.get_tx_receipt_by_tx_hash(tx_hash)
        print(receipt)
        time.sleep(5)
