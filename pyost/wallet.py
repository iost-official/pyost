from pathlib import Path
from base58 import b58encode
import re

from pyost.algorithm import Algorithm, Ed25519, Secp256k1
from pyost.account import Account, get_id_by_pubkey


def create_account(nickname: str = 'id', path: str = None,
                   sign_algo: str = Ed25519.NAME):
    if re.match('[?*:|/\\\]', nickname) or len(nickname) > 16:
        raise ValueError('Invalid nickname, it should be less than 16'
                         'characters and exclude special characters: ?*:|/\\')

    algo = Algorithm.get_algorithm_by_name(sign_algo)

    account = Account(None, algo)

    if path is None:
        path = Path.home().joinpath('.iwallet')
    path.mkdir(0o0700, exist_ok=True)

    filename = path.joinpath(f'{nickname}_{algo.NAME}').as_posix()

    with open(filename + '.pub', 'wb') as f:
        f.write(b58encode(account.pubkey))

    with open(filename, 'wb') as f:
        f.write(b58encode(account.seckey))

    print('The IOST account ID is:')
    print(get_id_by_pubkey(account.pubkey))
    print(f'The keys have been saved in {filename}(.pub)')


if __name__ == '__main__':
    create_account()
