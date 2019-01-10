import sys
import subprocess
import os
import collections
import time
import re
import json
import argparse
import random
from base58 import b58decode
from multiprocessing.pool import ThreadPool
from pyost.iost import IOST
from pyost.account import Account, KeyPair
from pyost.algorithm import Ed25519
from pyost.transaction import TransactionError, Transaction, Action
from pyost.contract import Contract

assert sys.version_info.major == 3
assert sys.version_info.minor >= 6

DEFAULT_EXPIRATION = 10
DEFAULT_GASLIMIT = 2000000
DEFAULT_GASRATIO = 1
DEFAULT_NODEIP = '35.180.171.246'
TESTID = 'iostsiri'
initial_coin_of_bet_user = 5

iost = IOST(f'{DEFAULT_NODEIP}:30002', gas_limit=DEFAULT_GASLIMIT, gas_ratio=DEFAULT_GASRATIO,
            expiration=DEFAULT_EXPIRATION)


def log(s):
    print(s)


def check_float_equal(a, b):
    assert abs(a - b) < 1e-6, f"not equal {a} {b}"


def get_balance(account_name):
    cmd = 'iwallet balance ' + account_name
    stdout = call(cmd)
    amount = re.findall('"balance": (\S+),', stdout)[0]
    return float(amount)


def fetch_contract_state(cid, key):
    data = {"id": cid, "key": key}
    cmd = f"curl -s -X POST --data '{json.dumps(data)}' http://{DEFAULT_NODEIP}:30001/getContractStorage"
    stdout = call(cmd)
    json_result = eval(json.loads(stdout)['data'])
    return json_result

def send(tx, verbose=False):
    try:
        txr = iost.send_and_wait_tx(tx)
        if verbose:
            print(txr)
        return txr
    except TransactionError as e:
        print(e)
        exit(1)


def publish_contract(js_file, js_abi_file, account):
    with open(js_file, 'r') as f:
        code = f.read()
    with open(js_abi_file, 'r') as f:
        abi_file = json.load(f)

    contract = Contract(code=code).from_json(abi_file)
    tx = iost.create_call_tx('system.iost', 'SetCode', contract.to_json())
    account.sign_publish(tx)
    print(tx)
    txr = send(tx)
    print(txr)
    print(iost.get_tx_by_hash(txr.tx_hash))


def init_account():
    private_key = b58decode(b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3')
    kp = KeyPair(Ed25519, private_key)
    testid_account = Account(TESTID)
    testid_account.add_key_pair(kp, 'active')
    testid_account.add_key_pair(kp, 'owner')
    iost.publisher = testid_account

    print(iost.get_account_info(iost.publisher.name).ram_info)
    print(iost.get_account_info(iost.publisher.name).gas_info)

    # TODO uncomment
    #iost.call('ram.iost', 'buy', testid_account.name, testid_account.name, 50000)
    #iost.call('gas.iost', 'pledge', testid_account.name, testid_account.name, '100')
    #print(iost.get_account_info(iost.publisher.name).ram_info)
    #print(iost.get_account_info(iost.publisher.name).gas_info)
    return testid_account


def publish():
    # TODO uncomment this
    #uploader_account = iost.new_account('sirilucky2', iost.publisher.name, 50000, 20, 0)
    #print(uploader_account)

    private_key = b58decode(b'3rDmfY3aFTUiMzbG7BkYmk7D5UKjSgKV46KnxibVYWCTxqRk5ZEXqYxAi4wv9yUdJUvJi2ZpHY6oHxoAf2CN8Zci')
    kp = KeyPair(Ed25519, private_key)
    uploader_account = Account('sirilucky2')
    uploader_account.add_key_pair(kp, 'active')
    uploader_account.add_key_pair(kp, 'owner')

    cid = publish_contract('contract/lucky_bet.js',
                           'contract/lucky_bet.js.abi', uploader_account)
    return cid


def get_bet_users():
    bet_user_num = 20  # must be same as `maxUserNumber` in lucky_bet.js
    bet_users = [
        f'user_{random.randint(0, 1000000)}' for idx in range(bet_user_num)]

    def create_bet_user(user):
        create_account(TESTID, user, 600, 100, initial_coin_of_bet_user, False)

    pool = ThreadPool(bet_user_num)
    pool.map(create_bet_user, bet_users)
    return bet_users


def main():
    account = init_account()
    cid = publish()
    exit(0)

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
        args = [bet_users[idx], lucky_number, bet_coin, nouce]
        call_contract(bet_users[idx], cid, 'bet', args, False)

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
        real_reward = rewards[bet_users[idx]]
        calculated_reward = 0 if lucky_numbers[idx] != final_lucky_number else total_coins_bet * 95 // 100 * bet_coins[
            idx] // all_lucky_bets
        check_float_equal(real_reward, calculated_reward)
    assert win_user_num == bet_user_num // 10
    # check balance of each user
    for i in range(bet_user_num):
        calculated_balance = initial_coin_of_bet_user - \
                             bet_coins[i] + rewards[bet_users[i]]
        # log(f'calculated_balance {calculated_balance} actual_balance {final_balances[i]}')
        check_float_equal(calculated_balance, final_balances[i])
    log('Congratulations! You have just run a smart contract on IOST!')


if __name__ == '__main__':
    main()
