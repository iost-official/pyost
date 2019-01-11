from base58 import b58decode
from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair

if __name__ == '__main__':
    iost = IOST('localhost:30002')

    account_seckey = b58decode(
        b'4vZ8qw2MaGLVXsbW7TcyTDcEqrefAS34vuM1eJf7YrBL9Fpnq3LgRyDjnUfv7kjvPfsA5tQGnou3Bv2bYNXyorK1')
    account_kp = KeyPair(Ed25519, account_seckey)
    account = Account('testacc1')
    account.add_key_pair(account_kp, 'active')
    account.add_key_pair(account_kp, 'owner')

    print(f'Account RAM: {iost.get_account_info(account.name).ram_info.available}')

    print(f'RAM price: {iost.get_ram_info().buy_price}')
    tx = iost.create_call_tx('ram.iost', 'buy', account.name, account.name, 50000)
    tx.gas_limit = 1000000
    account.sign_publish(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.send_and_wait_tx(tx)
        print(receipt)
    except TimeoutError as e:
        print(f'ERROR: {e}')
    except RuntimeError as e:
        print(f'ERROR: {e}')

    print(f'Account RAM: {iost.get_account_info(account.name).ram_info.available}')
