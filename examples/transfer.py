from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair
from pyost.transaction import TransactionError
from base58 import b58decode


def print_balance(account_name: str):
    account = iost.get_account_info(account_name)
    print(
        f'{account.name}: balance={account.balance} gas={account.gas_info.current_total} ram={account.ram_info.available}')


if __name__ == '__main__':
    iost = IOST('localhost:30002')

    admin_seckey = b58decode(b'1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB')
    admin_kp = KeyPair(Ed25519, admin_seckey)
    admin = Account('producer00001')
    admin.add_key_pair(admin_kp, 'active')
    admin.add_key_pair(admin_kp, 'owner')
    acc1 = admin
    print_balance(acc1.name)

    acc2_seckey = b58decode(b'4vZ8qw2MaGLVXsbW7TcyTDcEqrefAS34vuM1eJf7YrBL9Fpnq3LgRyDjnUfv7kjvPfsA5tQGnou3Bv2bYNXyorK1')
    acc2_kp = KeyPair(Ed25519, acc2_seckey)
    acc2 = Account('testacc1')
    acc2.add_key_pair(acc2_kp, 'active')
    acc2.add_key_pair(acc2_kp, 'owner')
    print_balance(acc2.name)

    tx = iost.create_transfer_tx('iost', acc1.name, acc2.name, 10000)

    # Those 2 lines are not necessary for transfer, this is just for illustrating multi-sig
    tx.add_signer(acc2.name, 'active')
    acc2.sign(tx, 'active')

    acc1.sign_publish(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.send_and_wait_tx(tx)
        # receipt = iost.wait_tx(iost.send_tx(tx), verbose=True)
        print(receipt)
    except TransactionError as e:
        print(f'Transaction error {e.status_code}: {e}')
    except TimeoutError as e:
        print(f'Timeout error: {e}')

    # All of this can also be written with the short version
    # iost.publisher = acc1
    # try:
    #     receipt = iost.transfer('iost', acc1.name, acc2.name, 1)
    #     print(receipt)
    # except TransactionError as e:
    #     print(f'Transaction error {e.status_code}: {e}')
    # except TimeoutError as e:
    #     print(f'Timeout error: {e}')

    print_balance(acc1.name)
    print_balance(acc2.name)
