import time
import json
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
    iost.publisher = admin

    hw_contract = '{"ID":"hw","info":{"lang":"javascript","version":"1.0.0","abi":[{"name":"hello"}, {"name":"can_update", "args": ["string"]}]},"code":"class Contract {init(){} hello(){return \\"world\\";} can_update(data){return true;}} module.exports = Contract;"}';

    # Set code
    # contract_id = 'ContractF2T8W8HnFDh3JdXT4fvXWTLKqhctZsBT6qEV3EVMsZ8V'
    print('setting code...')
    txr = iost.call('system.iost', 'SetCode', hw_contract)
    contract_id = json.loads(txr.returns[0])[0]
    print(f'Contract ID: {contract_id}')

    print('sending hello...')
    txr = iost.call(contract_id, 'hello')
    res = json.loads(txr.returns[0])[0]
    print(f'Response: {res}')

    hw_contract2 = '{"ID":"' + contract_id + '","info":{"lang":"javascript","version":"1.0.0","abi":[{"name":"hello", "args":["string"]}, {"name":"can_update", "args":["string"]}]},"code":"class Contract {init(){} hello(data){return data;} can_update(data){return false;}} module.exports = Contract;"}';
    print('updating code...')
    txr = iost.call('system.iost', 'UpdateCode', hw_contract2, '')
    print(txr.status_code.name)

    data = str(time.time())
    print(f'sending {data}...')
    txr = iost.call(contract_id, 'hello', data)
    res = json.loads(txr.returns[0])[0]
    print(f'Response: {res}')

    hw_contract3 = '{"ID":"' + contract_id + '","info":{"lang":"javascript","version":"1.0.0","abi":[{"name":"hello", "args":["string"]}]},"code":"class Contract {init(){} hello(data){return data;}} module.exports = Contract;"}';
    print('updating bad code...')
    txr = iost.call('system.iost', 'UpdateCode', hw_contract3, '')
    print(txr.status_code.name)
