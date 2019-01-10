import time
from base58 import b58decode, b58encode
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Secp256k1, Ed25519
from pyost.signature import KeyPair
from pyost.transaction import TransactionError

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    # acc_seckey = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    # acc_kp = KeyPair(Ed25519, acc_seckey)
    # acc = Account('iostsiri')
    # acc.add_key_pair(acc_kp, 'active')
    # acc.add_key_pair(acc_kp, 'owner')

    acc_seckey = b58decode(b'3weJNnPE16XDBncfZT68Jm13HQ68AqnvCjpNLZtVUV1FZyVQJBFpeP5TZhRhYTaDKjjpMoc7WE5V9mSayGTyCYN7')
    acc_kp = KeyPair(Ed25519, acc_seckey)
    acc = Account('iostsiri3')
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
