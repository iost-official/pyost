import time
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Secp256k1, Ed25519
from pyost.signature import KeyPair
from base58 import b58decode, b58encode
from pyost.transaction import TransactionError, TxReceipt

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002', gas_limit=2000000.0, default_limit='1000')

    admin_seckey = b58decode(
        b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    admin_kp = KeyPair(Ed25519, admin_seckey)
    admin = Account('iostsiri')
    admin.add_key_pair(admin_kp, 'active')
    admin.add_key_pair(admin_kp, 'owner')

    account_seckey = b58decode(b'3weJNnPE16XDBncfZT68Jm13HQ68AqnvCjpNLZtVUV1FZyVQJBFpeP5TZhRhYTaDKjjpMoc7WE5V9mSayGTyCYN7')
    account_kp = KeyPair(Ed25519, account_seckey)
    account = Account('iostsiri3')
    account.add_key_pair(account_kp, 'active')
    account.add_key_pair(account_kp, 'owner')

    # Create token
    token_sym = 't' + str(int(time.time() * 1000000))[-4:]
    tx = iost.create_call_tx('token.iost', 'create', token_sym, admin.name, 21000000,
                             {"fullName": "bit coin", "decimal": 9})
    admin.sign_publish(tx)
    print('creating token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
    except TransactionError as e:
        print(e)
        exit(1)

    ob_admin = iost.get_balance(admin.name, token_sym)
    ob0 = iost.get_balance(account.name, token_sym)

    # Issue token
    tx = iost.create_call_tx('token.iost', 'issue', token_sym, account.name, '99.1')
    admin.sign_publish(tx)
    print('issuing token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
    except TransactionError as e:
        print(e)
        exit(1)

    nb_admin = iost.get_balance(admin.name, token_sym)
    nb0 = iost.get_balance(account.name, token_sym)
    assert nb_admin == ob_admin
    assert nb0 == ob0 + 99.1

    # Transfer token
    ob_admin = iost.get_balance(admin.name, token_sym)
    ob0 = iost.get_balance(account.name, token_sym)

    tx = iost.create_transfer_tx(token_sym, account.name, admin.name, 55.000000001)
    account.sign_publish(tx)
    print('transferring token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
    except TransactionError as e:
        print(e)
        exit(1)

    nb_admin = iost.get_balance(admin.name, token_sym)
    nb0 = iost.get_balance(account.name, token_sym)
    assert nb_admin == ob_admin + 55.000000001
    assert nb0 == ob0 - 55.000000001

    # Transfer freeze
    ob_admin = iost.get_token_balance(admin.name, token_sym)
    ob0 = iost.get_token_balance(account.name, token_sym)

    tx = iost.create_call_tx('token.iost', 'transferFreeze',
                             token_sym, admin.name, account.name, '5',
                             int((time.time() + 5000) * 1e6), '')
    admin.sign_publish(tx)
    print('transfer-freezing token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
    except TransactionError as e:
        print(e)
        exit(1)

    nb_admin = iost.get_token_balance(admin.name, token_sym)
    nb0 = iost.get_token_balance(account.name, token_sym)
    assert nb_admin.balance == ob_admin.balance - 5
    assert nb0.balance == ob0.balance
    assert nb0.frozen_balances[0].amount == 5

    # Balance of
    ob_admin = iost.get_token_balance(admin.name, token_sym)
    ob0 = iost.get_token_balance(account.name, token_sym)

    tx = iost.create_call_tx('token.iost', 'balanceOf',
                             token_sym, account.name)
    admin.sign_publish(tx)
    print('querying balance of token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
    except TransactionError as e:
        print(e)
        exit(1)

    nb_admin = iost.get_token_balance(admin.name, token_sym)
    nb0 = iost.get_token_balance(account.name, token_sym)
    assert nb_admin.balance == ob_admin.balance
    assert nb0.balance == ob0.balance + 5
    assert len(nb0.frozen_balances) == 0

    # Token supply
    tx = iost.create_call_tx('token.iost', 'supply', token_sym)
    account.sign_publish(tx)
    print('querying supply of token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
        assert txr.returns[0] == '["99.1"]'
    except TransactionError as e:
        print(e)
        exit(1)

    # Token destroy
    ob0 = iost.get_token_balance(account.name, token_sym)

    tx = iost.create_call_tx('token.iost', 'destroy',
                             token_sym, account.name, str(ob0.balance))
    account.sign_publish(tx)
    print('destroying token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
    except TransactionError as e:
        print(e)
        exit(1)

    nb0 = iost.get_token_balance(account.name, token_sym)
    assert nb0.balance == 0

    # Token total supply
    tx = iost.create_call_tx('token.iost', 'totalSupply', token_sym)
    account.sign_publish(tx)
    print('querying total supply of token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
        assert txr.returns[0] == '["21000000"]'
    except TransactionError as e:
        print(e)
        exit(1)

    # Token supply
    tx = iost.create_call_tx('token.iost', 'supply', token_sym)
    account.sign_publish(tx)
    print('querying supply of token...')
    try:
        txr = iost.send_and_wait_tx(tx)
        print(txr)
        assert txr.returns[0] == '["50.000000001"]'
    except TransactionError as e:
        print(e)
        exit(1)
