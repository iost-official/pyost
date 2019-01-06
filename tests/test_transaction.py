from unittest import main, TestCase
import base58
from pyost.transaction import Transaction, Action
from pyost.account import Account
from pyost.signature import Signature
from pyost.algorithm import Algorithm, Secp256k1, Ed25519, KeyPair
from pyost.api.rpc.pb import rpc_pb2 as pb


class TestAction(TestCase):
    def test_action(self):
        action1 = Action('contract1', 'actionname1', '{\"num\": 1, \"message\": \"contract1\"}')

        encoded = action1.encode()
        action2 = Action()
        action2.decode(encoded)
        self.assertEqual(action1.contract, action2.contract)
        self.assertEqual(action1.action_name, action2.action_name)
        self.assertEqual(action1.data, action2.data)


class TestTransaction(TestCase):
    def setUp(self):
        self.algo = Ed25519
        self.actions = []
        self.actions.append(Action('contract1', 'actionname1', '{\"num\": 1, \"message\": \"contract1\"}'))
        self.actions.append(Action('contract2', 'actionname2', '1'))

        self.a1 = KeyPair(self.algo)
        self.a2 = KeyPair(self.algo)
        self.a3 = KeyPair(self.algo)

    def test_serialize_proto(self):
        tr = pb.Transaction(
            time=99,
            actions=[pb.Action(contract='contract1', actionName='actionname1',
                               data='{\"num\": 1, \"message\": \"contract1\"}')],
            signers=[self.a1.id],
        )
        b = tr.SerializeToString()

        tx1 = pb.Transaction()
        tx1.ParseFromString(b)
        self.assertEqual(99, tx1.time)

    def encode_and_decode(self):
        tx = Transaction(actions=self.actions, signers=[self.a1.id],
                         gas_limit=100000, gas_ratio=100, expiration=11, delay=0)
        tx1 = Transaction(actions=[], signers=[],
                         gas_limit=0, gas_ratio=0, expiration=0, delay=0)
        hash = tx._hash()

        encoded = tx.encode()
        self.assertIsNotNone(tx1.decode(encoded))

        hash1 = tx1.hash()
        self.assertEqual(hash, hash1)

        sig = sign_tx_content(tx, self.a1)
        self.assertIsNotNone(sig)
        self.assertIsNotNone(sign_tx(tx, self.a1, sig))

        hash = tx.hash()
        encoded = tx.encode()
        self.assertIsNotNone(tx1.decode(encoded))

        hash1 = tx1.hash()
        self.assertEqual(hash, hash1)

        self.assertEqual(tx.time, tx1.time)
        self.assertEqual(tx.expiration, tx1.expiration)
        self.assertEqual(tx.gas_limit, tx1.gas_limit)
        self.assertEqual(tx.gas_price, tx1.gas_price)
        self.assertEqual(len(tx.actions), len(tx1.actions))
        for i in range(len(tx.actions)):
            self.assertEqual(tx.actions[i].contract, tx1.actions[i].contract)
            self.assertEqual(tx.actions[i].action_name, tx1.actions[i].action_name)
            self.assertEqual(tx.actions[i].data, tx1.actions[i].data)
        self.assertEqual(len(tx.signers), len(tx1.signers))
        for i in range(len(tx.signers)):
            self.assertEqual(tx.signers[i], tx1.signers[i])
        self.assertEqual(len(tx.signs), len(tx1.signs))
        for i in range(len(tx.actions)):
            self.assertEqual(tx.signs[i].algorithm, tx1.signs[i].algorithm)
            self.assertEqual(tx.signs[i].pubkey, tx1.signs[i].pubkey)
            self.assertEqual(tx.signs[i].sig, tx1.signs[i].sig)
        self.assertTrue((tx.publisher is None and tx1.publisher is None)
                        or tx.publisher.algorithm == tx1.publisher.algorithm)
        self.assertTrue((tx.publisher is None and tx1.publisher is None)
                        or tx.publisher.pubkey == tx1.publisher.pubkey)
        self.assertTrue((tx.publisher is None and tx1.publisher is None)
                        or tx.publisher.sig == tx1.publisher.sig)

    def test_sig_and_verify(self):
        tx = Transaction(self.actions, [self.a1.pubkey, self.a2.pubkey], 9999, 1, 1)

        sig1 = sign_tx_content(tx, self.a1)
        self.assertTrue(tx.verify_signer(sig1))
        tx.signs.append(sig1)

        with self.assertRaises(PermissionError) as cm:
            tx.verify_self()
        print(cm.exception)

        sig2 = sign_tx_content(tx, self.a2)
        self.assertTrue(tx.verify_signer(sig2))
        tx.signs.append(sig2)

        with self.assertRaises(PermissionError) as cm:
            tx.verify_self()
        print(cm.exception)

        with self.assertRaises(PermissionError) as cm:
            sign_tx_content(tx, self.a3)
        print(cm.exception)

        self.assertIsNotNone(sign_tx(tx, self.a3))
        self.assertTrue(tx.verify_self())

        tx.publisher = Signature(self.algo, b'hello', self.algo.gen_seckey())
        with self.assertRaises(PermissionError) as cm:
            tx.verify_self()
        print(cm.exception)

        tx.signs[0] = Signature(self.algo, b'hello', self.algo.gen_seckey())
        with self.assertRaises(PermissionError) as cm:
            tx.verify_self()
        print(cm.exception)
