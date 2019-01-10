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

    print('Account Info:')
    print(iost.get_account_info(acc1.name))

    print('\nToken Balance:')
    print(iost.get_token_balance(acc1.name))

    print('\nToken 721 Balance:')
    print(iost.get_token721_balance(acc1.name, 'iost'))
