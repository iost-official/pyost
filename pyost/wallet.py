from pathlib import Path
from base58 import b58encode
from typing import List, Type
import re
import json
import math
import time

from pyost.iost import IOST
from pyost.algorithm import Algorithm, Ed25519, Secp256k1
from pyost.account import Account, get_id_by_pubkey, get_pubkey_by_id
from pyost.transaction import Action, Transaction, sign_tx


def get_default_key_path(filename: str = None):
    path = Path.home().joinpath('.iwallet')
    if filename is not None:
        path = path.joinpath(filename)
    return path.as_posix()


def create_account(nickname: str = 'id', key_path: str = get_default_key_path(),
                   sign_algo: str = Ed25519.NAME):
    if re.match('[?*:|/\\\]', nickname) or len(nickname) > 16:
        raise ValueError('Invalid nickname, it should be less than 16 '
                         'characters and exclude special characters: ?*:|/\\')

    algo = Algorithm.get_algorithm_by_name(sign_algo)

    account = Account(None, algo)

    path = Path(key_path)
    path.mkdir(0o0700, exist_ok=True)

    filename = path.joinpath(f'{nickname}_{algo.NAME}').as_posix()

    with open(filename + '.pub', 'wb') as f:
        f.write(b58encode(account.pubkey))

    with open(filename, 'wb') as f:
        f.write(b58encode(account.seckey))

    print('The IOST account id is:')
    print(get_id_by_pubkey(account.pubkey))
    print(f'The keys have been saved in {filename}(.pub)')


def call(*args, gas_limit: int = 1000, gas_price: int = 1, expiration: int = 60 * 5,
         signers: List[str] = None, key_path: str = None,
         sign_algo: Type[Algorithm] = Ed25519.NAME):
    if len(args) % 3 != 0:
        raise ValueError('Number of args should be a multiplier of 3.')

    args = list(args)
    actions = []

    for i in range(0, len(args), 3):
        if args[i] == 'iost.system' and args[i + 1] == 'Transfer':
            data = handle_transfer_data(args[i + 2])
            args[i + 2] = data

        actions.append(Action(*args[i:i + 3]))

    if signers is not None and len(signers) > 0:
        pubkeys = [get_pubkey_by_id(signer) for signer in signers]
    else:
        pubkeys = []

    tx = Transaction(actions, pubkeys, gas_limit, gas_price, expiration)

    if signers is None or len(signers) == 0:
        print(f'The transaction does not contain any signers so it will be directly'
              f'sent to the IOST node and the secret key in {key_path} will be used.')

        if key_path is None:
            key_path = get_default_key_path(f'id_{sign_algo.NAME}')

        with open(key_path, 'rb') as f:
            seckey = f.readline()

        account = Account(seckey, sign_algo)

        tx_hash = iost.send_tx(sign_tx(tx, account))

        print('The transaction has been sent to the IOST node.')
        print(f'Tx hash: {tx_hash}')
    else:
        tx_bytes = tx.encode()

        if dest == 'default':
            dest = Path(dest).stem + '.sc'

        with open(dest, 'wb') as f:
            f.write(tx_bytes)

        print('The unsigned transaction has been saved to', dest)
        print('The account ids of the signers are: ', signers)
        print('Please inform them to sign this contract'
              'and send the generated signatures back to you')


def handle_transfer_data(data: str) -> str:
    if data.endswith(',]'):
        data = data[:-2] + ']'
    js = json.loads(data)

    if not isinstance(js, list) or len(js) != 3:
        raise ValueError(f'\'Transfer\' call needs 3 arguments but got {len(js)}.')

    amount = float(js[2])
    max_int64 = 2 ** 63 - 1
    if amount * 1e8 > max_int64:
        raise ValueError(f'You cannot transfer more than {max_int64 / 1e8}')

    return f'["{js[0]}", "{js[1]}", "{max_int64 / 1e8}"]'


def publish()
    pass

if __name__ == '__main__':
    call(1, 2, 3, 4, gas_limit=1, gas_price=1)
