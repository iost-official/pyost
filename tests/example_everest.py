from pyost.iost import IOST
from pyost.account import Account
from pyost.algorithm import Ed25519, KeyPair

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    acc1_seckey = b'58NCdrz3iUfqKnEk6AX57rGrv9qrvn8EXtiUvVXMLqkKJKSFuW6TR6iuuYBtjgzhwm9ew6e9Pjg3zx5n6ya9MHJ3'
    acc1_kp = KeyPair(Ed25519, acc1_seckey)
    acc1 = Account('iostsiri')
    acc1.add_key_pair(acc1_kp, 'active')
    acc1.add_key_pair(acc1_kp, 'owner')
    print(f'Account 1:\n{iost.get_account(acc1.name)}')

    # seckey2 = '3vFoZPT1c3FSNVa9qrYMa2SQyxNQ8dfLSySNSzWokZQb4U1HToW1qUL3XzhpDE66MnjeUGwSDrYDJYgDFUary4Mb'
    # account2 = Account(seckey2, algorithm.Ed25519)
    # print(f'Account 2 pubkey: {account2.pubkey}')
    # print(f'Account 2 balance: {iost.get_balance(account2.pubkey)}')
    #
    # tx = iost.transfer(account1.pubkey, account1.pubkey, 1)
    # tx.gas_limit = 1
    # tx.gas_price = 1
    # # tx.add_signer(account1.pubkey)
    # # account1.sign_tx_content(tx)
    # tx.add_publisher_sign(account1)
    # tx.verify_self()
    #
    # tx_res = iost.send_tx(tx)
    # print(f'Transaction status: {tx_res.status}')
    #
    # sleep(5)
    # try:
    #     tx_res = iost.get_tx_by_hash(tx_res._hash)
    #     print(tx_res)
    # except Exception as err:
    #     print(err)
    #
    # print(f'Account 1 balance: {iost.get_balance(account1.pubkey)}')
    # print(f'Account 2 balance: {iost.get_balance(account2.pubkey)}')
