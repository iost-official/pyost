from unittest import main, TestCase
import base58
from pyost import IOST


class TestIOST(TestCase):
    def setUp(self):
        self.iost = IOST('localhost:30002')

    def test_get_net_id(self):
        id = self.iost.get_net_id()
        self.assertEqual(id, '12D3KooWGPpGc8gbaHGJ6BywPrUoUKpPUKPmbCyr3ZLfgQRqj9m5')

    def test_get_height(self):
        height = self.iost.get_height()
        self.assertGreaterEqual(height, 0)

    def test_get_tx_by_hash(self):
        tx_hash = '6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb'
        tx, res_hash = self.iost.get_tx_by_hash(tx_hash)
        compare_dict = {
            'time': 1544123981522270000,
            'expiration': 1544124281522263000,
            'gasLimit': 1000,
            'gasPrice': 1,
            'actions': [{
                'contract': 'iost.system',
                'actionName': 'Transfer',
                'data': '["IOSTfQFocqDn7VrKV7vvPqhAQGyeFU9XMYo5SNn5yQbdbzC75wM7C", "6d8jQzRcxawmTebQQhrWvBvbjpSp9CnPFCFQsuBoMWQc", 1000000000000]'
            }],
            'publisher': {
                'algorithm': 2,
                'sig': b'\xe6\x99~\xf5P\xe1\xf0P\x83tK\xc3\xc8^\x06>\xc3\x1a\x13.f=\xe6\x86\x9e\x88\xcc\x8ehK\xcd&\xa4\x8d1\xe4&>\x07\xac\x15\x13\xfa\xe6\x18\x8f\x05\x1d\xfbR\x8e\x8cI&\x9f\xbb\xa8-\xc2\xf6\xdbO\xba\x01',
                'pubKey': b'W1\xad\xeb]\x1a\x80~\xc9\xc48%8\x9e^\xdf\xf7\x04\x12\xe4d:\x94b\x9ae*\xf1\xbf\xcf/\x08'
            }
        }
        # TODO What is this value?
        # print(base58.b58encode(compare_dict['publisher']['pubKey']))
        self.assertEqual(res_hash, base58.b58decode(tx_hash))
        self.assertDictEqual(tx, compare_dict)

    def test_get_tx_receipt_by_hash(self):
        tx_hash = '6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb'
        receipt_hash = 'GWh7aHCZZeEjJXzQjtRcez6j1rbzNtbdGTQ7arNsB25i'
        tx, res_hash = self.iost.get_tx_receipt_by_hash(receipt_hash)
        compare_dict = {
            'txHash': b"T\xefO\x9fD\x87\xca\xf01q'4\x04\xcb\xc9\xa9Y\xfa\x80(\xf2\xaa\x07Y\xfcY\xd6\xcd\x10b\xde\xea",
            'gasUsage': 303,
            'status': {},
            'succActionNum': 1
        }
        self.assertEqual(compare_dict['txHash'], base58.b58decode(tx_hash))
        self.assertEqual(res_hash, base58.b58decode(receipt_hash))
        self.assertDictEqual(tx, compare_dict)

    def test_get_tx_receipt_by_tx_hash(self):
        tx_hash = '6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb'
        receipt_hash = 'GWh7aHCZZeEjJXzQjtRcez6j1rbzNtbdGTQ7arNsB25i'
        tx, res_hash = self.iost.get_tx_receipt_by_tx_hash(tx_hash)
        compare_dict = {
            'txHash': b"T\xefO\x9fD\x87\xca\xf01q'4\x04\xcb\xc9\xa9Y\xfa\x80(\xf2\xaa\x07Y\xfcY\xd6\xcd\x10b\xde\xea",
            'gasUsage': 303,
            'status': {},
            'succActionNum': 1
        }
        self.assertEqual(compare_dict['txHash'], base58.b58decode(tx_hash))
        self.assertEqual(res_hash, base58.b58decode(receipt_hash))
        self.assertDictEqual(tx, compare_dict)

    def test_get_balance(self):
        account_id = '6d8jQzRcxawmTebQQhrWvBvbjpSp9CnPFCFQsuBoMWQc'
        balance = self.iost.get_balance(account_id, False)
        self.assertEqual(balance, 4000000000000)

if __name__ == '__main__':
    main()
