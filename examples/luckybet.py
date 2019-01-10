import sys
import subprocess
import os
import collections
import time
import re
import json
import argparse
import random
from multiprocessing.pool import ThreadPool

assert sys.version_info.major == 3
assert sys.version_info.minor >= 6

DEFAULT_EXPIRATION = 10
DEFAULT_GASLIMIT = 2000000
DEFAULT_GASRATIO = 1
DEFAULT_NODEIP = '127.0.0.1'
TESTID='admin'
initial_coin_of_bet_user = 5

command_prefix = f'iwallet --expiration {DEFAULT_EXPIRATION} --gas_limit {DEFAULT_GASLIMIT} --gas_ratio {DEFAULT_GASRATIO} --amount_limit "iost:3000000|ram:10000" '


def log(s):
    print(s)


def check_float_equal(a, b):
    assert abs(a - b) < 1e-6, f"not equal {a} {b}"


def call(cmd, verbose=False):
    log(cmd)
    ret = subprocess.run(cmd, encoding='utf8', shell=True,
                         stdout=subprocess.PIPE)
    assert not ret.stdout is None
    if verbose or ret.returncode != 0:
        print(ret.stdout)
    ret.check_returncode()
    return ret.stdout


def create_account(creator, account_name, initial_ram, initial_gas_pledge, initial_balance, verbose=False):
    call(f'{command_prefix} --account {creator} account --create {account_name} '
         + f'--initial_ram {initial_ram} --initial_gas_pledge {initial_gas_pledge} --initial_balance {initial_balance}', verbose)


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


def call_contract(caller_name, cid, function_name, function_args, verbose=False):
    cmd = f'{command_prefix} --account {caller_name} call '
    function_args_str = json.dumps(function_args)
    cmd += f' {cid} {function_name} \'{function_args_str}\''
    call(cmd, verbose)


def publish_contract(js_file, js_abi_file, account_name):
    cmd = f'{command_prefix} --account {account_name} publish {js_file} {js_abi_file}'
    stdout = call(cmd)
    contract_id = re.findall(r'The contract id is (\S+)$', stdout)[0]
    return contract_id


def init_account():
    private_key = '2yquS3ySrGWPEKywCPzX4RTJugqRh7kJSo5aehsLYPEWkUxBWA39oMrZ7ZxuM4fgyXYs2cPwh5n8aNNpH5x2VyK1'
    cmd = f'iwallet account --import {TESTID} {private_key}'
    call(cmd)
    # need some ram and gas for creating users later
    # buy 5000000 bytes
    call_contract(TESTID, 'ram.iost', 'buy', [TESTID, TESTID, 5000000])
    # pledge 3000000 IOSTs for gas
    call_contract(TESTID, 'gas.iost', 'pledge', [TESTID, TESTID, '3000000'])


def publish():
    # publish the contract
    create_account(TESTID, 'uploader', 50000, 20, 0)
    cid = publish_contract('contract/lucky_bet.js',
                           'contract/lucky_bet.js.abi', 'uploader')
    return cid


def get_bet_users():
    bet_user_num = 20 # must be same as `maxUserNumber` in lucky_bet.js
    bet_users = [
        f'user_{random.randint(0, 1000000)}' for idx in range(bet_user_num)]

    def create_bet_user(user):
        create_account(TESTID, user, 600, 100, initial_coin_of_bet_user, False)
    pool = ThreadPool(bet_user_num)
    pool.map(create_bet_user, bet_users)
    return bet_users


def main():
    init_account()
    cid = publish()

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
    contract_state = fetch_contract_state(cid, f'result{round_num-1}')
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
    all_lucky_bets = int(sum([bet_coins[idx] for idx in range(bet_user_num) if lucky_numbers[idx] == final_lucky_number]))
    for idx in range(bet_user_num):
        real_reward = rewards[bet_users[idx]]
        calculated_reward = 0 if lucky_numbers[idx] != final_lucky_number else total_coins_bet * 95 // 100 * bet_coins[idx] // all_lucky_bets
        check_float_equal(real_reward, calculated_reward)
    assert win_user_num == bet_user_num // 10
    # check balance of each user
    for i in range(bet_user_num):
        calculated_balance = initial_coin_of_bet_user - \
            bet_coins[i] + rewards[bet_users[i]]
        #log(f'calculated_balance {calculated_balance} actual_balance {final_balances[i]}')
        check_float_equal(calculated_balance, final_balances[i])
    log('Congratulations! You have just run a smart contract on IOST!')


if __name__ == '__main__':
    main()
