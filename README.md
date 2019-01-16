# PyOST

Python SDK for the IOST blockchain, wrap the RPC API to easily create and send transactions,
manage accounts, publish and execute smart contracts, etc.

## Installation

Install the library and its dependencies. Needs at least Python 3.5.

```sh
$ pip install pyost
```

## Examples

### Blockchain Information

Connect to the blockchain:
```python
from pyost.iost import IOST
iost = IOST('localhost:30002')
```

Get information about the blockchain:
```python
print(iost.get_node_info())
print(iost.get_chain_info())
print(iost.get_ram_info())
print(iost.get_gas_ratio())
```

Get information about a block:
```python
# By block number.
block0 = iost.get_block_by_num(0)
print(block0)

# By block hash, complete=True will retrieve the full list of Transactions.
print(iost.get_block_by_hash(block0.hash, complete=True))
```

### Account Creation

Load an account from a base58 secret key:
```python
from base58 import b58decode
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair
acc_seckey = b58decode(b'<your base58 private key>')
acc_kp = KeyPair(Ed25519, acc_seckey)
acc = Account('<account_name>')
acc.add_key_pair(acc_kp, 'active')
acc.add_key_pair(acc_kp, 'owner')
```

Get account information and token balances:
```python
print(iost.get_account_info(acc.name))
print(iost.get_token_balance(acc.name))
print(iost.get_token721_balance(acc.name, 'token_name'))
```

Create a new account, first we need to generate a pair of public and private keys:
```python
acc2_kp = KeyPair(Ed25519)
# WARNING Do not forget to store the new account secret key:
from base58 import b58encode
print(b58encode(acc2_kp.seckey))

acc2 = Account('<new_account_name>')
acc2.add_key_pair(acc2_kp, 'active')
acc2.add_key_pair(acc2_kp, 'owner')
```

Then we must use an existing account to pledge coins for this new account:
```python
from pyost.transaction import TransactionError

tx = iost.create_new_account_tx(acc2.name, acc.name,
                                b58encode(acc2_kp.pubkey),
                                b58encode(acc2_kp.pubkey), 0, 100.0, 100.0)
tx.gas_limit = 1000000.0
acc.sign_publish(tx)

try:
    receipt = iost.send_and_wait_tx(tx)
except (TransactionError, TimeoutError):
    pass
```

There is a shorter version for the previous 2 blocks of code:
```python
# Need to set the first account as the default publisher to automatically sign Transactions:
iost.publisher = acc

try:
    acc2 = iost.new_account('<new_account_name>', acc.name, 0, 100.0, 100.0, Ed25519)
except (TransactionError, TimeoutError):
    pass

# WARNING Do not forget to store the new account secret key:
print(b58encode(acc2.get_key_pair('active').seckey))
```

### Calling an ABI function

Example to buy RAM for own account:
```python
ram_amount = 1024
tx = iost.create_call_tx('ram.iost', 'buy', acc.name, acc.name, ram_amount)
acc.sign_publish(tx)

try:
    receipt = iost.send_and_wait_tx(tx)
except (TransactionError, TimeoutError):
    pass
```

### Token Transfer

```python
token = 'iost'
from_name = acc.name
to_name = acc2.name
amount = 10000
```

Create a transfer Transaction, there are multiple way.
Manually:
```python
from pyost.transaction import Transaction
tx = Transaction(gas_limit=100000.0, gas_ratio=1.0, expiration=90, delay=0)
tx.add_amount_limit('*', 'unlimited')
tx.add_amount_limit('iost', str(amount))
tx.add_action('token.iost', 'transfer', token, from_name, to_name, str(amount), '')
```

By using the Transaction creation helper function:
```python
tx = iost.create_tx()
tx.add_action('token.iost', 'transfer', token, from_name, to_name, str(amount), '')
tx.add_amount_limit('iost', str(amount))
```

By using the call creation helper function:
```python
tx = iost.create_call_tx('token.iost', 'transfer', token, from_name, to_name, str(amount), '')
tx.add_amount_limit('iost', str(amount))
```

By using the transfer creation helper function:
```python
tx = iost.create_transfer_tx('iost', from_name, to_name, amount)
```

You can now sign this Transaction with multiple signers (this is not mandatory for transfer,
 just to illustrate multi-sig):
```python
tx.add_signer(acc2.name, 'active')
acc2.sign(tx, 'active')
```

You must sign the Transaction with one publisher (if no signers was added in the previous step,
the publisher must be the same as the `from_name` account):
```python
acc.sign_publish(tx)
```

And finally send the Transaction and wait for it to be processed:
```python
try:
    receipt = iost.send_and_wait_tx(tx)
    # Alternatively:
    # receipt = iost.wait_tx(iost.send_tx(tx), verbose=True)
except (TransactionError, TimeoutError):
    pass
```

There is a shorter version for all code in this section:
```python
iost.publisher = acc

try:
    receipt = iost.transfer('iost', from_name, to_name, amount)
except (TransactionError, TimeoutError):
    pass
```

### Publishing and Calling Smart Contract

Load the smart contract code and ABI files:
```python
with open(js_file, 'r') as f:
    code = f.read()
with open(js_abi_file, 'r') as f:
    abi_file = json.load(f)

from pyost.contract import Contract
contract = Contract(code=code).from_json(abi_file)
```

Publish it as follow and save the returned contract id:
```python
try:
    receipt = iost.publish(contract)
except (TransactionError, TimeoutError):
    pass
contract_id = json.loads(receipt.returns[0])[0]
```

Call the contract's ABI:
```python
txr = iost.call(contract_id, '<func_name>', '<args1>', '<args2>')
res = json.loads(txr.returns[0])[0]
print(f'Response: {res}')
```

Upate the contract's code:
```python
txr = iost.call('system.iost', 'updateCode', new_contract.to_json(), '')
print(txr.status_code.name)
```

### Token Creation

Create a new token:
```python
token_sym = '<token_name>'
token_amount = 21000000
tx = iost.create_call_tx('token.iost', 'create', token_sym, acc.name, token_amount,
                         {"fullName": "bit coin", "decimal": 9})
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)
```

Issue tokens:
```python
issue_amount = 99.1
tx = iost.create_call_tx('token.iost', 'issue', token_sym, acc.name, str(issue_amount))
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)

print(iost.get_balance(acc.name, token_sym))
```

Transfer tokens:
```python
transfer_amount = 55.000000001
print(iost.get_balance(acc.name, token_sym))
print(iost.get_balance(acc2.name, token_sym))

tx = iost.create_transfer_tx(token_sym, acc.name, acc2.name, transfer_amount)
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)

print(iost.get_balance(acc.name, token_sym))
print(iost.get_balance(acc2.name, token_sym))
```

Transfer freeze:
```python
transfer_amount = 5
tx = iost.create_call_tx('token.iost', 'transferFreeze',
                         token_sym, acc.name, acc2.name, str(transfer_amount),
                         int((time.time() + 5000) * 1e6), '')
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)
print(iost.get_token_balance(acc2.name, token_sym).frozen_balances[0])
```

Balance of:
```python
tx = iost.create_call_tx('token.iost', 'balanceOf',
                         token_sym, acc.name)
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)
print(iost.get_balance(acc2.name, token_sym))
```

Get token supply:
```python
tx = iost.create_call_tx('token.iost', 'supply', token_sym)
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)
print(txr.returns[0])
```

Destroy tokens:
```python
destroy_amount = 10
tx = iost.create_call_tx('token.iost', 'destroy',
                         token_sym, acc.name, str(destroy_amount))
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)
```

Total supply:
```python
tx = iost.create_call_tx('token.iost', 'totalSupply', token_sym)
acc.sign_publish(tx)
txr = iost.send_and_wait_tx(tx)
print(txr.returns[0])
```
