import time
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair
from base58 import b58decode

if __name__ == '__main__':
    iost = IOST('localhost:30002')

    admin_seckey = b58decode(b'1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB')
    admin_kp = KeyPair(Ed25519, admin_seckey)
    admin = Account('producer00001')
    admin.add_key_pair(admin_kp, 'active')
    admin.add_key_pair(admin_kp, 'owner')

    account_seckey = b58decode(
        b'4vZ8qw2MaGLVXsbW7TcyTDcEqrefAS34vuM1eJf7YrBL9Fpnq3LgRyDjnUfv7kjvPfsA5tQGnou3Bv2bYNXyorK1')
    account_kp = KeyPair(Ed25519, account_seckey)
    account = Account('testacc1')
    account.add_key_pair(account_kp, 'active')
    account.add_key_pair(account_kp, 'owner')

    # Create token
    token_sym = 't' + str(int(time.time() * 1000000))[-4:]
    tx = iost.create_call_tx('token.iost', 'create', token_sym, admin.name, 21000000,
                             {"fullName": "bit coin", "decimal": 9})
    admin.sign_publish(tx)
    print('creating token...')
    txr = iost.send_and_wait_tx(tx)
    print(txr)

    ob_admin = iost.get_balance(admin.name, token_sym)
    ob0 = iost.get_balance(account.name, token_sym)

    # Issue token
    tx = iost.create_call_tx('token.iost', 'issue', token_sym, account.name, '99.1')
    admin.sign_publish(tx)
    print('issuing token...')
    txr = iost.send_and_wait_tx(tx)
    print(txr)

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
    txr = iost.send_and_wait_tx(tx)
    print(txr)

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
    txr = iost.send_and_wait_tx(tx)
    print(txr)

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
    txr = iost.send_and_wait_tx(tx)
    print(txr)

    nb_admin = iost.get_token_balance(admin.name, token_sym)
    nb0 = iost.get_token_balance(account.name, token_sym)
    assert nb_admin.balance == ob_admin.balance
    assert nb0.balance == ob0.balance + 5
    assert len(nb0.frozen_balances) == 0

    # Token supply
    tx = iost.create_call_tx('token.iost', 'supply', token_sym)
    account.sign_publish(tx)
    print('querying supply of token...')
    txr = iost.send_and_wait_tx(tx)
    print(txr)
    assert txr.returns[0] == '["99.1"]'

    # Token destroy
    ob0 = iost.get_token_balance(account.name, token_sym)

    tx = iost.create_call_tx('token.iost', 'destroy',
                             token_sym, account.name, str(ob0.balance))
    account.sign_publish(tx)
    print('destroying token...')
    txr = iost.send_and_wait_tx(tx)
    print(txr)

    nb0 = iost.get_token_balance(account.name, token_sym)
    assert nb0.balance == 0

    # Token total supply
    tx = iost.create_call_tx('token.iost', 'totalSupply', token_sym)
    account.sign_publish(tx)
    print('querying total supply of token...')
    txr = iost.send_and_wait_tx(tx)
    print(txr)
    assert txr.returns[0] == '["21000000"]'

    # Token supply
    tx = iost.create_call_tx('token.iost', 'supply', token_sym)
    account.sign_publish(tx)
    print('querying supply of token...')
    txr = iost.send_and_wait_tx(tx)
    print(txr)
    assert txr.returns[0] == '["50.000000001"]'
