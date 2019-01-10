import time
from base58 import b58decode, b58encode
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair
from pyost.transaction import TransactionError

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    acc_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    acc_kp = KeyPair(Ed25519, acc_seckey)
    acc = Account('iostsiri')
    acc.add_key_pair(acc_kp, 'active')
    acc.add_key_pair(acc_kp, 'owner')

    # acc_seckey = b58decode(b'3weJNnPE16XDBncfZT68Jm13HQ68AqnvCjpNLZtVUV1FZyVQJBFpeP5TZhRhYTaDKjjpMoc7WE5V9mSayGTyCYN7')
    # acc_kp = KeyPair(Ed25519, acc_seckey)
    # acc = Account('iostsiri3')
    # acc.add_key_pair(acc_kp, 'active')
    # acc.add_key_pair(acc_kp, 'owner')

    print(f'Account RAM: {iost.get_account_info(acc.name).ram_info.available}')

    print(f'RAM price: {iost.get_ram_info().buy_price}')
    tx = iost.create_call_tx('ram.iost', 'buy', acc.name, acc.name, 50000)
    tx.gas_limit = 1000000
    acc.sign_publish(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.send_and_wait_tx(tx)
        print(receipt)
    except TimeoutError as e:
        print(f'ERROR: {e}')
    except RuntimeError as e:
        print(f'ERROR: {e}')

    print(f'Account RAM: {iost.get_account_info(acc.name).ram_info.available}')
