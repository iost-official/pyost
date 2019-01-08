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
    acc1_info = iost.get_account_info(acc1.name)
    print(f'{acc1_info.name}: balance={acc1_info.balance} gas={acc1_info.gas_info.current_total} ram={acc1_info.ram_info.available}')

    acc2_seckey = b58decode(b'3weJNnPE16XDBncfZT68Jm13HQ68AqnvCjpNLZtVUV1FZyVQJBFpeP5TZhRhYTaDKjjpMoc7WE5V9mSayGTyCYN7')
    acc2_kp = KeyPair(Ed25519, acc2_seckey)
    acc2 = Account('iostsiri3')
    acc2.add_key_pair(acc2_kp, 'active')
    acc2.add_key_pair(acc2_kp, 'owner')
    acc2_info = iost.get_account_info(acc2.name)
    print(f'{acc2_info.name}: balance={acc2_info.balance} gas={acc2_info.gas_info.current_total} ram={acc2_info.ram_info.available}')

    tx = iost.create_transfer_tx('iost', acc2.name, acc1.name, 1)
    acc1.sign_publish(tx)

    print('Waiting for transaction to be processed...')
    try:
        receipt = iost.wait_tx(iost.send_tx(tx), verbose=True)
        print(f'Receipt status: {receipt.status_code}')
        print(receipt)
    except TimeoutError as e:
        print(e)
    except RuntimeError as e:
        print(e)

    acc1_info = iost.get_account_info(acc1.name)
    print(f'{acc1_info.name}: balance={acc1_info.balance} gas={acc1_info.gas_info.current_total} ram={acc1_info.ram_info.available}')

    acc2_info = iost.get_account_info(acc2.name)
    print(f'{acc2_info.name}: balance={acc2_info.balance} gas={acc2_info.gas_info.current_total} ram={acc2_info.ram_info.available}')
