import sys
import collections
import json
import random
from base58 import b58decode
from multiprocessing.pool import ThreadPool
from pyost.iost import IOST
from pyost.account import Account, KeyPair
from pyost.algorithm import Ed25519
from pyost.transaction import TransactionError
from pyost.contract import Contract

assert sys.version_info.major == 3
assert sys.version_info.minor >= 6

DEFAULT_EXPIRATION = 10
DEFAULT_GASLIMIT = 1000000
DEFAULT_GASRATIO = 1
DEFAULT_NODEIP = 'localhost'
TESTID = 'admin'
KEY = '2yquS3ySrGWPEKywCPzX4RTJugqRh7kJSo5aehsLYPEWkUxBWA39oMrZ7ZxuM4fgyXYs2cPwh5n8aNNpH5x2VyK1'
initial_coin_of_bet_user = 5

iost = IOST(f'{DEFAULT_NODEIP}:30002', gas_limit=DEFAULT_GASLIMIT, gas_ratio=DEFAULT_GASRATIO,
            expiration=DEFAULT_EXPIRATION)


def log(s):
    print(s)


def check_float_equal(a, b):
    assert abs(a - b) < 1e-6, f"not equal {a} {b}"


def get_balance(account):
    return iost.get_balance(account.name)


def fetch_contract_state(cid, key):
    return json.loads(iost.get_contract_storage(cid, key))


def publish_contract(js_file, js_abi_file, account):
    with open(js_file, 'r') as f:
        code = f.read()
    with open(js_abi_file, 'r') as f:
        abi_file = json.load(f)
    contract = Contract(code=code).from_json(abi_file)

    try:
        # WARNING this will be signed by the testid not by the uploader's account
        txr = iost.publish(contract)
        return json.loads(txr.returns[0])[0]
    except TransactionError as e:
        print(e)
        exit(1)


def init_account():
    private_key = b58decode(bytes(KEY, 'utf8'))
    kp = KeyPair(Ed25519, private_key)
    testid_account = Account(TESTID)
    testid_account.add_key_pair(kp, 'active')
    testid_account.add_key_pair(kp, 'owner')
    iost.publisher = testid_account

    # print(iost.get_account_info(iost.publisher.name).ram_info)
    # print(iost.get_account_info(iost.publisher.name).gas_info)
    # iost.call('ram.iost', 'buy', testid_account.name, testid_account.name, 50000)
    # iost.call('gas.iost', 'pledge', testid_account.name, testid_account.name, '30000')
    # print(iost.get_account_info(iost.publisher.name).ram_info)
    # print(iost.get_account_info(iost.publisher.name).gas_info)


def publish():
    uploader_account = iost.new_account(f'upacc{random.randint(0, 1000000)}', iost.publisher.name, 50000, 20, 0)
    cid = publish_contract('contract/lucky_bet.js',
                           'contract/lucky_bet.js.abi', uploader_account)
    return cid


def get_bet_users():
    bet_user_num = 20  # must be same as `maxUserNumber` in lucky_bet.js
    bet_users = [
        f'user_{random.randint(0, 1000000)}' for _ in range(bet_user_num)]

    def create_bet_user(user):
        print(f'Creating account {user}...')
        account = iost.new_account(user, iost.publisher.name, 600, 100, initial_coin_of_bet_user)
        print(f'Account {user} created.')
        return account

    pool = ThreadPool(bet_user_num)
    return pool.map(create_bet_user, bet_users)


def main():
    init_account()
    cid = publish()
    print(f'Contract ID: {cid}')

    # create fake users with initial IOSTs
    bet_users = get_bet_users()
    bet_user_num = len(bet_users)
    pool = ThreadPool(bet_user_num)

    # bet
    bet_coins = [(idx // 2 % 5) + 1 for idx in range(bet_user_num)]
    lucky_numbers = [idx % 10 for idx in range(bet_user_num)]

    def bet(idx):
        lucky_number = lucky_numbers[idx]
        bet_coin = bet_coins[idx]
        nouce = ''
        tx = iost.create_call_tx(cid, 'bet', bet_users[idx].name, lucky_number, bet_coin, nouce)
        bet_users[idx].sign_publish(tx)
        try:
            txr = iost.send_and_wait_tx(tx)
            print(f'#{idx} status: {txr.status_code.name}')
        except TransactionError as e:
            print(e)

    pool.map(bet, range(bet_user_num))

    # get bet results
    final_balances = pool.map(get_balance, bet_users)
    print('Balance after the bet', final_balances)

    # check result
    round_num = fetch_contract_state(cid, 'round')
    assert round_num == 2
    final_lucky_number = fetch_contract_state(cid, 'last_lucky_block') % 10
    contract_state = fetch_contract_state(cid, f'result{round_num - 1}')
    rewards = collections.defaultdict(float)
    win_user_num = 0
    for record in contract_state['records']:
        if 'reward' in record:
            win_user_num += 1
            reward = float(record['reward'])
            rewards[record['account']] = reward
    log(f'rewards: {rewards}')
    # check reward
    total_coins_bet = int(sum(bet_coins))
    all_lucky_bets = int(
        sum([bet_coins[idx] for idx in range(bet_user_num) if lucky_numbers[idx] == final_lucky_number]))
    for idx in range(bet_user_num):
        real_reward = rewards[bet_users[idx].name]
        calculated_reward = 0 if lucky_numbers[idx] != final_lucky_number else total_coins_bet * 95 // 100 * bet_coins[
            idx] // all_lucky_bets
        check_float_equal(real_reward, calculated_reward)
    assert win_user_num == bet_user_num // 10
    # check balance of each user
    for i in range(bet_user_num):
        calculated_balance = initial_coin_of_bet_user - \
                             bet_coins[i] + rewards[bet_users[i].name]
        # log(f'calculated_balance {calculated_balance} actual_balance {final_balances[i]}')
        check_float_equal(calculated_balance, final_balances[i])
    log('Congratulations! You have just run a smart contract on IOST!')


if __name__ == '__main__':
    main()
