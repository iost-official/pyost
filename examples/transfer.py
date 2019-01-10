import time
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Secp256k1, Ed25519
from pyost.signature import KeyPair
from pyost.transaction import TransactionError
from base58 import b58decode, b58encode


def print_balance(account_name: str):
    account = iost.get_account_info(account_name)
    print(
        f'{account.name}: balance={account.balance} gas={account.gas_info.current_total} ram={account.ram_info.available}')


if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    acc1_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    acc1_kp = KeyPair(Ed25519, acc1_seckey)
    acc1 = Account('iostsiri')
    acc1.add_key_pair(acc1_kp, 'active')
    acc1.add_key_pair(acc1_kp, 'owner')
    print_balance(acc1.name)

    acc2_seckey = b58decode(b'3weJNnPE16XDBncfZT68Jm13HQ68AqnvCjpNLZtVUV1FZyVQJBFpeP5TZhRhYTaDKjjpMoc7WE5V9mSayGTyCYN7')
    acc2_kp = KeyPair(Ed25519, acc2_seckey)
    acc2 = Account('iostsiri3')
    acc2.add_key_pair(acc2_kp, 'active')
    acc2.add_key_pair(acc2_kp, 'owner')
    print_balance(acc2.name)

    tx = iost.create_transfer_tx('iost', acc1.name, acc2.name, 1)
    acc1.sign_publish(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.send_and_wait_tx(tx)
        print(receipt)
    except TransactionError as e:
        print(f'Transaction error {e.status_code}: {e}')
    except TimeoutError as e:
        print(f'Timeout error: {e}')

    print_balance(acc1.name)
    print_balance(acc2.name)
