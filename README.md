# PyOST

Python SDK for the IOST blockchain, wrap the RPC API to easily create and send transaction, manage accounts, publish and execute smart contracts, etc.

### Installation

Install the library and its dependencies. Needs at least Python 3.5.

```sh
$ pip install pyost
```

### Examples

Connect to the blockchain:

```python
from pyost.iost import IOST
iost = IOST('localhost:30002')
```

Get information about the blockchain:

```python
print(iost.get_node_info())
```

Load an account from a b58 secret key:
```python
from base58 import b58decode
from pyost.account import Account
from pyost.algorithm import Ed25519
from pyost.signature import KeyPair
acc_seckey = b58decode(b'1rANSfcRzr4HkhbUFZ7L1Zp69JZZHiDDq5v7dNSbbEqeU4jxy3fszV4HGiaLQEyqVpS1dKT9g7zCVRxBVzuiUzB')
acc_kp = KeyPair(Ed25519, acc_seckey)
acc = Account('producer00001')
acc.add_key_pair(acc_kp, 'active')
acc.add_key_pair(acc_kp, 'owner')
```

Get account info:
```python
print(iost.get_account_info(acc.name))
```