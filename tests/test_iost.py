from unittest import main, TestCase
import base58
from pyost.iost import IOST
from pyost.transaction import Transaction


class TestIOST(TestCase):
    def setUp(self):
        self.iost = IOST('localhost:30002')

    def test_get_height(self):
        height = self.iost.get_height()
        self.assertGreaterEqual(height, 0)

    def test_get_tx_by_hash(self):
        tx_hash = b'6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb'
        tx, res_hash = self.iost.get_tx_by_hash(tx_hash)
        tx_compare = Transaction()  # add content
        print(tx)
        self.assertEqual(res_hash, tx_hash)
        # self.assertDictEqual(tx, tx_compare)

    def test_get_tx_receipt_by_hash(self):
        tx_hash = b'6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb'
        receipt_hash = b'GWh7aHCZZeEjJXzQjtRcez6j1rbzNtbdGTQ7arNsB25i'
        tx, res_hash = self.iost.get_tx_receipt_by_hash(receipt_hash)
        compare_dict = {
            'txHash': b'6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb',
            'gasUsage': 303,
            'status': {},
            'succActionNum': 1
        }
        self.assertEqual(compare_dict['txHash'], tx_hash)
        self.assertEqual(res_hash, receipt_hash)
        self.assertDictEqual(tx, compare_dict)

    def test_get_tx_receipt_by_tx_hash(self):
        tx_hash = b'6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb'
        receipt_hash = b'GWh7aHCZZeEjJXzQjtRcez6j1rbzNtbdGTQ7arNsB25i'
        tx, res_hash = self.iost.get_tx_receipt_by_tx_hash(tx_hash)
        compare_dict = {
            'txHash': b'6iYtt5eqwmEcDKfte7FhZFpcVXgsf7CR7wfbm1CqiHZb',
            'gasUsage': 303,
            'status': {},
            'succActionNum': 1
        }
        self.assertEqual(compare_dict['txHash'], base58.b58decode(tx_hash))
        self.assertEqual(res_hash, base58.b58decode(receipt_hash))
        self.assertDictEqual(tx, compare_dict)

    def test_get_block_by_hash(self):
        block_hash = b'3VkWkdWf9ixSVNqqh9Cod22GXkaPQjhCzKD69Xx3nzDX'
        block_info = self.iost.get_block_by_hash(block_hash)
        compare_dict = {
            'head': {
                'txsHash': b'\x04\xe5#=\xa0\xcfq\x89\xcdG\xe8\x1b\xb5\x84Y]\xce\xf6\xca+\xc7\xe1\x9d\xe7\xbd\xbf\x82xOB\xdaU',
                'merkleHash': b'\x05\xb3\xb7#R\r\xdcU\x9d\x1dr\x0f@.\x80wQ\xd2$\xf0\xfd\x8bCp\xe3=\xd2~\x82*\xcf?',
                'witness': 'IOST2FpDWNFqH9VuA8GbbVAwQcyYGHZxFeiTwSyaeyXnV84yJZAG7A'},
            'hash': b'%\x14\xd67\x1anx\xac\x1b\xdd\xa6\x97\xb1;J\x8e\xa7\xc2~\xb5>\xd2\xc0\xb5h\x07[6VS\x94\xe2',
            'txhash': [
                b"\x97\xff\xe4Lv\x91\x10[\x90\x02\xc2\x93\x86\x81h\n\rt\x94_\x8b\xa1\x01\xc1\x87;\xf3\x02\x17',\xdb"],
            'receiptHash': [
                b'\x93\x95\x1a\xa4\xdbG\x8f\xa6\x94\x9c\xb2Sv\xa3\xa3X\xa5\xf9z\xfdS\x86c~\xaf\xbc\xc5\xee\xc2\x03DP']
        }
        self.assertDictEqual(block_info, compare_dict)

    def test_get_block_by_hash_complete(self):
        block_hash = '3VkWkdWf9ixSVNqqh9Cod22GXkaPQjhCzKD69Xx3nzDX'
        block_info = self.iost.get_block_by_hash(block_hash, complete=True)
        compare_dict = {
            'head': {
                'txsHash': b'\x04\xe5#=\xa0\xcfq\x89\xcdG\xe8\x1b\xb5\x84Y]\xce\xf6\xca+\xc7\xe1\x9d\xe7\xbd\xbf\x82xOB\xdaU',
                'merkleHash': b'\x05\xb3\xb7#R\r\xdcU\x9d\x1dr\x0f@.\x80wQ\xd2$\xf0\xfd\x8bCp\xe3=\xd2~\x82*\xcf?',
                'witness': 'IOST2FpDWNFqH9VuA8GbbVAwQcyYGHZxFeiTwSyaeyXnV84yJZAG7A'
            },
            'hash': b'%\x14\xd67\x1anx\xac\x1b\xdd\xa6\x97\xb1;J\x8e\xa7\xc2~\xb5>\xd2\xc0\xb5h\x07[6VS\x94\xe2',
            'txs': [{
                'gasLimit': 100000000,
                'actions': [
                    {'contract': 'iost.system', 'actionName': 'IssueIOST',
                     'data': '["IOSTfQFocqDn7VrKV7vvPqhAQGyeFU9XMYo5SNn5yQbdbzC75wM7C", 2100000000000000000]'},
                    {'contract': 'iost.system', 'actionName': 'InitSetCode',
                     'data': '["iost.vote", "Cglpb3N0LnZvdGUS7gIKCmphdmFzY3JpcHQSBTEuMC4wGg0KC2NvbnN0cnVjdG9yGgYKBGluaXQaFAoKY2FuX3VwZGF0ZSoGc3RyaW5nGhYKDEluaXRQcm9kdWNlcioGc3RyaW5nGhMKCUluaXRBZG1pbioGc3RyaW5nGjIKEFJlZ2lzdGVyUHJvZHVjZXIqBnN0cmluZyoGc3RyaW5nKgZzdHJpbmcqBnN0cmluZxowCg5VcGRhdGVQcm9kdWNlcioGc3RyaW5nKgZzdHJpbmcqBnN0cmluZyoGc3RyaW5nGhcKDUxvZ0luUHJvZHVjZXIqBnN0cmluZxoYCg5Mb2dPdXRQcm9kdWNlcioGc3RyaW5nGhwKElVucmVnaXN0ZXJQcm9kdWNlcioGc3RyaW5nGh4KBFZvdGUqBnN0cmluZyoGc3RyaW5nKgZudW1iZXIaIAoGVW52b3RlKgZzdHJpbmcqBnN0cmluZyoGbnVtYmVyGgYKBFN0YXQa3lZjb25zdCBzb2Z0RmxvYXRSYXRlID0gMWU4Owpjb25zdCBwcm9kdWNlclJlZ2lzdGVyRmVlID0gMTAwMCAqIDEwMDAgKiBzb2Z0RmxvYXRSYXRlOwpjb25zdCBwcmVQcm9kdWNlclRocmVzaG9sZCA9IDIxMDAgKiAxMDAwMDsKY29uc3Qgdm90ZUxvY2tUaW1lID0gMjAwOwpjb25zdCB2b3RlU3RhdEludGVydmFsID0gMjAwOwoKY2xhc3MgVm90ZUNvbnRyYWN0IHsKICAgIGNvbnN0cnVjdG9yKCkgewogICAgfQogICAgaW5pdCgpIHsKICAgICAgICB0aGlzLl9wdXQoImN1cnJlbnRQcm9kdWNlckxpc3QiLCBbXSk7CiAgICAgICAgdGhpcy5fcHV0KCJwZW5kaW5nUHJvZHVjZXJMaXN0IiwgW10pOwogICAgICAgIHRoaXMuX3B1dCgicGVuZGluZ0Jsb2NrTnVtYmVyIiwgMCk7CiAgICB9CgogICAgSW5pdFByb2R1Y2VyKHByb0lEKSB7CiAgICAJY29uc3QgYm4gPSB0aGlzLl9nZXRCbG9ja051bWJlcigpOwogICAgCWlmKGJuICE9PSAwKSB7CiAgICAJCXRocm93IG5ldyBFcnJvcigiaW5pdCBvdXQgb2YgZ2VuZXNpcyBibG9jayIpCgkJfQoKICAgIAlsZXQgcGVuZGluZ1Byb2R1Y2VyTGlzdCA9IHRoaXMuX2dldCgicGVuZGluZ1Byb2R1Y2VyTGlzdCIpOwoJCXBlbmRpbmdQcm9kdWNlckxpc3QucHVzaChwcm9JRCk7CiAgICAgICAgY29uc3Qga2V5Q21wID0gZnVuY3Rpb24oYSwgYikgewogICAgICAgICAgICBpZiAoYiA8IGEpIHsKICAgICAgICAgICAgICAgIHJldHVybiAxOwogICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgcmV0dXJuIC0xOwogICAgICAgICAgICB9CiAgICAgICAgfTsKICAgICAgICBwZW5kaW5nUHJvZHVjZXJMaXN0LnNvcnQoa2V5Q21wKTsKICAgICAgICB0aGlzLl9wdXQoInBlbmRpbmdQcm9kdWNlckxpc3QiLCBwZW5kaW5nUHJvZHVjZXJMaXN0KTsKCiAgICAgICAgY29uc3QgcHJvZHVjZXJOdW1iZXIgPSBwZW5kaW5nUHJvZHVjZXJMaXN0Lmxlbmd0aDsKICAgICAgICB0aGlzLl9wdXQoInByb2R1Y2VyTnVtYmVyIiwgcHJvZHVjZXJOdW1iZXIpOwoKICAgICAgICBjb25zdCByZXQgPSBCbG9ja0NoYWluLmRlcG9zaXQocHJvSUQsIHByb2R1Y2VyUmVnaXN0ZXJGZWUpOwogICAgICAgIGlmIChyZXQgIT09IDApIHsKICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJjb25zdHJ1Y3RvciBkZXBvc2l0IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CiAgICAgICAgfQogICAgICAgIHRoaXMuX21hcFB1dCgicHJvZHVjZXJUYWJsZSIsIHByb0lELCB7CiAgICAgICAgICAgICJsb2MiOiAiIiwKICAgICAgICAgICAgInVybCI6ICIiLAogICAgICAgICAgICAibmV0SWQiOiAiIiwKICAgICAgICAgICAgIm9ubGluZSI6IHRydWUsCiAgICAgICAgICAgICJzY29yZSI6IDAsCiAgICAgICAgICAgICJ2b3RlcyI6IDAKICAgICAgICB9KTsKICAgIH0KCiAgICBJbml0QWRtaW4oYWRtaW5JRCkgewogICAgICAgIGNvbnN0IGJuID0gdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKTsKICAgICAgICBpZihibiAhPT0gMCkgewogICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoImluaXQgb3V0IG9mIGdlbmVzaXMgYmxvY2siKQogICAgICAgIH0KICAgICAgICB0aGlzLl9wdXQoImFkbWluSUQiLCBhZG1pbklEKTsKICAgIH0KCiAgICBjYW5fdXBkYXRlKGRhdGEpIHsKICAgICAgICBjb25zdCBhZG1pbiA9IHRoaXMuX2dldCgiYWRtaW5JRCIpOwogICAgICAgIHRoaXMuX3JlcXVpcmVBdXRoKGFkbWluKTsKICAgICAgICByZXR1cm4gdHJ1ZTsKICAgIH0KCglfcmVxdWlyZUF1dGgoYWNjb3VudCkgewoJCWNvbnN0IHJldCA9IEJsb2NrQ2hhaW4ucmVxdWlyZUF1dGgoYWNjb3VudCk7CgkJaWYgKHJldCAhPT0gdHJ1ZSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInJlcXVpcmUgYXV0aCBmYWlsZWQuIHJldCA9ICIgKyByZXQpOwoJCX0KCX0KCglfZ2V0QmxvY2tOdW1iZXIoKSB7CgkJY29uc3QgYmkgPSBKU09OLnBhcnNlKEJsb2NrQ2hhaW4uYmxvY2tJbmZvKCkpOwoJCWlmICghYmkgfHwgYmkgPT09IHVuZGVmaW5lZCB8fCBiaS5udW1iZXIgPT09IHVuZGVmaW5lZCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoImdldCBibG9jayBudW1iZXIgZmFpbGVkLiBiaSA9ICIgKyBiaSk7CgkJfQoJCXJldHVybiBiaS5udW1iZXI7Cgl9CgogICAgX2dldChrKSB7CiAgICAgICAgcmV0dXJuIEpTT04ucGFyc2Uoc3RvcmFnZS5nZXQoaykpOwogICAgfQoJX3B1dChrLCB2KSB7CiAgICAgICAgY29uc3QgcmV0ID0gc3RvcmFnZS5wdXQoaywgSlNPTi5zdHJpbmdpZnkodikpOwogICAgICAgIGlmIChyZXQgIT09IDApIHsKICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJzdG9yYWdlIHB1dCBmYWlsZWQuIHJldCA9ICIgKyByZXQpOwogICAgICAgIH0KICAgIH0KICAgIF9tYXBHZXQoaywgZikgewogICAgICAgIHJldHVybiBKU09OLnBhcnNlKHN0b3JhZ2UubWFwR2V0KGssIGYpKTsKICAgIH0KICAgIF9tYXBQdXQoaywgZiwgdikgewogICAgICAgIGNvbnN0IHJldCA9IHN0b3JhZ2UubWFwUHV0KGssIGYsIEpTT04uc3RyaW5naWZ5KHYpKTsKICAgICAgICBpZiAocmV0ICE9PSAwKSB7CiAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcigic3RvcmFnZSBtYXAgcHV0IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CiAgICAgICAgfQogICAgfQoKICAgIF9tYXBEZWwoaywgZikgewogICAgICAgIGNvbnN0IHJldCA9IHN0b3JhZ2UubWFwRGVsKGssIGYpOwogICAgICAgIGlmIChyZXQgIT09IDApIHsKICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJzdG9yYWdlIG1hcCBkZWwgZmFpbGVkLiByZXQgPSAiICsgcmV0KTsKICAgICAgICB9CiAgICB9CgoJLy8gcmVnaXN0ZXIgYWNjb3VudCBhcyBhIHByb2R1Y2VyLCBuZWVkIHRvIHBsZWRnZSB0b2tlbgogICAgUmVnaXN0ZXJQcm9kdWNlcihhY2NvdW50LCBsb2MsIHVybCwgbmV0SWQpIHsKCQl0aGlzLl9yZXF1aXJlQXV0aChhY2NvdW50KTsKCQlpZiAoc3RvcmFnZS5tYXBIYXMoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50KSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIGV4aXN0cyIpOwoJCX0KCQljb25zdCByZXQgPSBCbG9ja0NoYWluLmRlcG9zaXQoYWNjb3VudCwgcHJvZHVjZXJSZWdpc3RlckZlZSk7CgkJaWYgKHJldCAhPT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInJlZ2lzdGVyIGRlcG9zaXQgZmFpbGVkLiByZXQgPSAiICsgcmV0KTsKCQl9CgkJdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCwgewoJCQkibG9jIjogbG9jLAoJCQkidXJsIjogdXJsLAoJCQkibmV0SWQiOiBuZXRJZCwKCQkJIm9ubGluZSI6IGZhbHNlLAoJCQkic2NvcmUiOiAwLAoJCQkidm90ZXMiOiAwCgkJfSk7CiAgICB9CgoJLy8gdXBkYXRlIHRoZSBpbmZvcm1hdGlvbiBvZiBhIHByb2R1Y2VyCiAgICBVcGRhdGVQcm9kdWNlcihhY2NvdW50LCBsb2MsIHVybCwgbmV0SWQpIHsKCQl0aGlzLl9yZXF1aXJlQXV0aChhY2NvdW50KTsKCQlpZiAoIXN0b3JhZ2UubWFwSGFzKCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCkpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJwcm9kdWNlciBub3QgZXhpc3RzIik7CgkJfQoJCWNvbnN0IHBybyA9IHRoaXMuX21hcEdldCgicHJvZHVjZXJUYWJsZSIsIGFjY291bnQpOwoJCXByby5sb2MgPSBsb2M7CgkJcHJvLnVybCA9IHVybDsKCQlwcm8ubmV0SWQgPSBuZXRJZDsKCQl0aGlzLl9tYXBQdXQoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50LCBwcm8pOwogICAgfQoKCS8vIHByb2R1Y2VyIGxvZyBpbiBhcyBvbmxpbmUgc3RhdGUKICAgIExvZ0luUHJvZHVjZXIoYWNjb3VudCkgewoJCXRoaXMuX3JlcXVpcmVBdXRoKGFjY291bnQpOwogICAgICAgIGlmICghc3RvcmFnZS5tYXBIYXMoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50KSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCBleGlzdHMsICIgKyBhY2NvdW50KTsKCQl9CiAgICAgICAgY29uc3QgcHJvID0gdGhpcy5fbWFwR2V0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCk7CgkJcHJvLm9ubGluZSA9IHRydWU7CiAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCwgcHJvKTsKICAgIH0KCgkvLyBwcm9kdWNlciBsb2cgb3V0IGFzIG9mZmxpbmUgc3RhdGUKICAgIExvZ091dFByb2R1Y2VyKGFjY291bnQpIHsKCQl0aGlzLl9yZXF1aXJlQXV0aChhY2NvdW50KTsKICAgICAgICBpZiAoIXN0b3JhZ2UubWFwSGFzKCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCkpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJwcm9kdWNlciBub3QgZXhpc3RzIik7CgkJfQoJCWlmICh0aGlzLl9nZXQoInBlbmRpbmdQcm9kdWNlckxpc3QiKS5pbmNsdWRlcyhhY2NvdW50KSB8fAogICAgICAgICAgICB0aGlzLl9nZXQoImN1cnJlbnRQcm9kdWNlckxpc3QiKS5pbmNsdWRlcyhhY2NvdW50KSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIGluIHBlbmRpbmcgbGlzdCBvciBpbiBjdXJyZW50IGxpc3QsIGNhbid0IGxvZ291dCIpOwoJCX0KICAgICAgICBjb25zdCBwcm8gPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50KTsKCQlwcm8ub25saW5lID0gZmFsc2U7CiAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCwgcHJvKTsKICAgIH0KCgkvLyByZW1vdmUgYWNjb3VudCBmcm9tIHByb2R1Y2VyIGxpc3QKCVVucmVnaXN0ZXJQcm9kdWNlcihhY2NvdW50KSB7CgkJdGhpcy5fcmVxdWlyZUF1dGgoYWNjb3VudCk7CiAgICAgICAgaWYgKCFzdG9yYWdlLm1hcEhhcygicHJvZHVjZXJUYWJsZSIsIGFjY291bnQpKSB7CgkJCXRocm93IG5ldyBFcnJvcigicHJvZHVjZXIgbm90IGV4aXN0cyIpOwoJCX0KICAgICAgICBpZiAodGhpcy5fZ2V0KCJwZW5kaW5nUHJvZHVjZXJMaXN0IikuaW5jbHVkZXMoYWNjb3VudCkgfHwKICAgICAgICAgICAgdGhpcy5fZ2V0KCJjdXJyZW50UHJvZHVjZXJMaXN0IikuaW5jbHVkZXMoYWNjb3VudCkpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJwcm9kdWNlciBpbiBwZW5kaW5nIGxpc3Qgb3IgaW4gY3VycmVudCBsaXN0LCBjYW4ndCB1bnJlZ2lzdCIpOwoJCX0KCQkvLyB3aWxsIGNsZWFyIHZvdGVzIGFuZCBzY29yZSBvZiB0aGUgcHJvZHVjZXIKCiAgICAgICAgdGhpcy5fbWFwRGVsKCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCk7CiAgICAgICAgdGhpcy5fbWFwRGVsKCJwcmVQcm9kdWNlck1hcCIsIGFjY291bnQpOwoKCQljb25zdCByZXQgPSBCbG9ja0NoYWluLndpdGhkcmF3KGFjY291bnQsIHByb2R1Y2VyUmVnaXN0ZXJGZWUpOwoJCWlmIChyZXQgIT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoIndpdGhkcmF3IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CgkJfQoJfQoKCS8vIHZvdGUsIG5lZWQgdG8gcGxlZGdlIHRva2VuCglWb3RlKHByb2R1Y2VyLCB2b3RlciwgYW1vdW50KSB7CgkJdGhpcy5fcmVxdWlyZUF1dGgodm90ZXIpOwoJCWFtb3VudCA9IE1hdGguZmxvb3IoYW1vdW50KTsKCiAgICAgICAgaWYgKCFzdG9yYWdlLm1hcEhhcygicHJvZHVjZXJUYWJsZSIsIHByb2R1Y2VyKSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCBleGlzdHMiKTsKCQl9CgoJCWNvbnN0IHJldCA9IEJsb2NrQ2hhaW4uZGVwb3NpdCh2b3RlciwgYW1vdW50ICogc29mdEZsb2F0UmF0ZSk7CgkJaWYgKHJldCAhPT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInZvdGUgZGVwb3NpdCBmYWlsZWQuIHJldCA9ICIgKyByZXQpOwoJCX0KCgkJbGV0IHZvdGVSZXMgPSB7fTsKICAgICAgICBpZiAoc3RvcmFnZS5tYXBIYXMoInZvdGVUYWJsZSIsIHZvdGVyKSkgewoJCSAgICB2b3RlUmVzID0gdGhpcy5fbWFwR2V0KCJ2b3RlVGFibGUiLCB2b3Rlcik7CgkJfQoJCS8vIHJlY29yZCB0aGUgYW1vdW50IGFuZCB0aW1lIG9mIHRoZSB2b3RlCgkJaWYgKHZvdGVSZXMuaGFzT3duUHJvcGVydHkocHJvZHVjZXIpKSB7CgkJCXZvdGVSZXNbcHJvZHVjZXJdLmFtb3VudCArPSBhbW91bnQ7CgkJfSBlbHNlIHsKICAgICAgICAgICAgdm90ZVJlc1twcm9kdWNlcl0gPSB7fTsKCQkJdm90ZVJlc1twcm9kdWNlcl0uYW1vdW50ID0gYW1vdW50OwoJCX0KCQl2b3RlUmVzW3Byb2R1Y2VyXS50aW1lID0gdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKTsKICAgICAgICB0aGlzLl9tYXBQdXQoInZvdGVUYWJsZSIsIHZvdGVyLCB2b3RlUmVzKTsKCgkJLy8gaWYgcHJvZHVjZXIncyB2b3RlcyA+PSBwcmVQcm9kdWNlclRocmVzaG9sZCwgdGhlbiBpbnNlcnQgaW50byBwcmVQcm9kdWNlciBtYXAKICAgICAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBwcm9kdWNlcik7CgkJcHJvUmVzLnZvdGVzICs9IGFtb3VudDsKCQlpZiAocHJvUmVzLnZvdGVzIC0gYW1vdW50IDwgIHByZVByb2R1Y2VyVGhyZXNob2xkICYmCgkJCQlwcm9SZXMudm90ZXMgPj0gcHJlUHJvZHVjZXJUaHJlc2hvbGQpIHsKCQkgICAgdGhpcy5fbWFwUHV0KCJwcmVQcm9kdWNlck1hcCIsIHByb2R1Y2VyLCB0cnVlKTsKCQl9CiAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgcHJvZHVjZXIsIHByb1JlcykKCX0KCgkvLyB1bnZvdGUKCVVudm90ZShwcm9kdWNlciwgdm90ZXIsIGFtb3VudCkgewogICAgICAgIGFtb3VudCA9IE1hdGguZmxvb3IoYW1vdW50KTsKCQl0aGlzLl9yZXF1aXJlQXV0aCh2b3Rlcik7CgoJCWlmICghc3RvcmFnZS5tYXBIYXMoInZvdGVUYWJsZSIsIHZvdGVyKSkgewogICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCB2b3RlZCIpOwogICAgICAgIH0KICAgICAgICBjb25zdCB2b3RlUmVzID0gdGhpcy5fbWFwR2V0KCJ2b3RlVGFibGUiLCB2b3Rlcik7CgkJaWYgKCF2b3RlUmVzLmhhc093blByb3BlcnR5KHByb2R1Y2VyKSkgewogICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCB2b3RlZCIpCiAgICAgICAgfQogICAgICAgIGlmICh2b3RlUmVzW3Byb2R1Y2VyXS5hbW91bnQgPCBhbW91bnQpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJ2b3RlIGFtb3VudCBsZXNzIHRoYW4gZXhwZWN0ZWQiKQoJCX0KCQlpZiAodm90ZVJlc1twcm9kdWNlcl0udGltZSArIHZvdGVMb2NrVGltZT4gdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInZvdGUgc3RpbGwgbG9ja2VkIikKCQl9CgkJdm90ZVJlc1twcm9kdWNlcl0uYW1vdW50IC09IGFtb3VudDsKCQl0aGlzLl9tYXBQdXQoInZvdGVUYWJsZSIsIHZvdGVyLCB2b3RlUmVzKTsKCgkJLy8gaWYgcHJvZHVjZXIgbm90IGV4aXN0LCBpdCdzIGJlY2F1c2UgcHJvZHVjZXIgaGFzIHVucmVnaXN0ZXJlZCwgZG8gbm90aGluZwoJCWlmIChzdG9yYWdlLm1hcEhhcygicHJvZHVjZXJUYWJsZSIsIHByb2R1Y2VyKSkgewoJCSAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBwcm9kdWNlcik7CgkJCWNvbnN0IG9yaSA9IHByb1Jlcy52b3RlczsKCQkJcHJvUmVzLnZvdGVzID0gTWF0aC5tYXgoMCwgb3JpIC0gYW1vdW50KTsKCQkJdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgcHJvZHVjZXIsIHByb1Jlcyk7CgoJCQkvLyBpZiBwcm9kdWNlcidzIHZvdGVzIDwgcHJlUHJvZHVjZXJUaHJlc2hvbGQsIHRoZW4gZGVsZXRlIGZyb20gcHJlUHJvZHVjZXIgbWFwCgkJCWlmIChvcmkgPj0gcHJlUHJvZHVjZXJUaHJlc2hvbGQgJiYKCQkJCQlwcm9SZXMudm90ZXMgPCBwcmVQcm9kdWNlclRocmVzaG9sZCkgewoJCQkgICAgdGhpcy5fbWFwRGVsKCJwcmVQcm9kdWNlck1hcCIsIHByb2R1Y2VyKTsKCQkJfQoJCX0KCgkJY29uc3QgcmV0ID0gQmxvY2tDaGFpbi53aXRoZHJhdyh2b3RlciwgYW1vdW50ICogc29mdEZsb2F0UmF0ZSk7CgkJaWYgKHJldCAhPT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoIndpdGhkcmF3IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CgkJfQoKICAgICAgICBjb25zdCBzZXJ2aSA9IE1hdGguZmxvb3IoYW1vdW50ICogdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKSAvIHZvdGVMb2NrVGltZSk7CgkJY29uc3QgcmV0MiA9IEJsb2NrQ2hhaW4uZ3JhbnRTZXJ2aSh2b3Rlciwgc2VydmkpOwoJCWlmIChyZXQyICE9PSAwKSB7CgkJICAgIHRocm93IG5ldyBFcnJvcigiZ3JhbnQgc2VydmkgZmFpbGVkLiByZXQgPSAiICsgcmV0Mik7CiAgICAgICAgfQoJfQoKCS8vIGNhbGN1bGF0ZSB0aGUgdm90ZSByZXN1bHQsIG1vZGlmeSBwZW5kaW5nUHJvZHVjZXJMaXN0CglTdGF0KCkgewoJCS8vIGNvbnRyb2xsIGF1dGgKCQljb25zdCBibiA9IHRoaXMuX2dldEJsb2NrTnVtYmVyKCk7CgkJY29uc3QgcGVuZGluZ0Jsb2NrTnVtYmVyID0gdGhpcy5fZ2V0KCJwZW5kaW5nQmxvY2tOdW1iZXIiKTsKCQlpZiAoYm4gJSB2b3RlU3RhdEludGVydmFsIT09IDAgfHwgYm4gPD0gcGVuZGluZ0Jsb2NrTnVtYmVyKSB7CgkJCXRocm93IG5ldyBFcnJvcigic3RhdCBmYWlsZWQuIGJsb2NrIG51bWJlciBtaXNtYXRjaC4gcGVuZGluZyBibiA9ICIgKyBwZW5kaW5nQmxvY2tOdW1iZXIgKyAiLCBibiA9ICIgKyBibik7CgkJfQoKCQkvLyBhZGQgc2NvcmVzIGZvciBwcmVQcm9kdWNlck1hcAoJCWNvbnN0IHByZUxpc3QgPSBbXTsJLy8gbGlzdCBvZiBwcm9kdWNlcnMgd2hvc2Ugdm90ZSA+IHRocmVzaG9sZAogICAgICAgIGNvbnN0IHByZVByb2R1Y2VyTWFwS2V5cyA9IHN0b3JhZ2UubWFwS2V5cygicHJlUHJvZHVjZXJNYXAiKTsKCiAgICAgICAgY29uc3QgcGVuZGluZ1Byb2R1Y2VyTGlzdCA9IHRoaXMuX2dldCgicGVuZGluZ1Byb2R1Y2VyTGlzdCIpOwoKCQlmb3IgKGxldCBpIGluIHByZVByb2R1Y2VyTWFwS2V5cykgewoJCSAgICBjb25zdCBrZXkgPSBwcmVQcm9kdWNlck1hcEtleXNbaV07CgkJICAgIGNvbnN0IHBybyA9IHRoaXMuX21hcEdldCgicHJvZHVjZXJUYWJsZSIsIGtleSk7CiAgICAgICAgICAgIC8vIGRvbid0IGdldCBzY29yZSBpZiBpbiBwZW5kaW5nIHByb2R1Y2VyIGxpc3Qgb3Igb2ZmbGluZQoJCSAgICBpZiAoIXBlbmRpbmdQcm9kdWNlckxpc3QuaW5jbHVkZXMoa2V5KSAmJgogICAgICAgICAgICAgICAgcHJvLnZvdGVzID49IHByZVByb2R1Y2VyVGhyZXNob2xkICYmCiAgICAgICAgICAgICAgICBwcm8ub25saW5lID09PSB0cnVlKSB7CiAgICAgICAgICAgICAgICBwcmVMaXN0LnB1c2goewogICAgICAgICAgICAgICAgICAgICJrZXkiOiBrZXksCiAgICAgICAgICAgICAgICAgICAgInByaW9yIjogMCwKICAgICAgICAgICAgICAgICAgICAidm90ZXMiOiBwcm8udm90ZXMsCiAgICAgICAgICAgICAgICAgICAgInNjb3JlIjogcHJvLnNjb3JlCiAgICAgICAgICAgICAgICB9KTsKICAgICAgICAgICAgfQogICAgICAgIH0KICAgICAgICBmb3IgKGxldCBpID0gMDsgaSA8IHByZUxpc3QubGVuZ3RoOyBpKyspIHsKCQkJY29uc3Qga2V5ID0gcHJlTGlzdFtpXS5rZXk7CgkJCWNvbnN0IGRlbHRhID0gcHJlTGlzdFtpXS52b3RlcyAtIHByZVByb2R1Y2VyVGhyZXNob2xkOwogICAgICAgICAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBrZXkpOwoKICAgICAgICAgICAgcHJvUmVzLnNjb3JlICs9IGRlbHRhOwogICAgICAgICAgICB0aGlzLl9tYXBQdXQoInByb2R1Y2VyVGFibGUiLCBrZXksIHByb1Jlcyk7CgkJCXByZUxpc3RbaV0uc2NvcmUgKz0gZGVsdGE7CgkJfQoKCQkvLyBzb3J0IGFjY29yZGluZyB0byBzY29yZSBpbiByZXZlcnNlZCBvcmRlcgoJCWNvbnN0IHNjb3JlQ21wID0gZnVuY3Rpb24oYSwgYikgewoJCQlpZiAoYi5zY29yZSAhPSBhLnNjb3JlKSB7CgkJCSAgICByZXR1cm4gYi5zY29yZSAtIGEuc2NvcmU7CgkJCX0gZWxzZSBpZiAoYi5wcmlvciAhPSBhLnByaW9yKSB7CgkJCSAgICByZXR1cm4gYi5wcmlvciAtIGEucHJpb3I7CgkJCX0gZWxzZSBpZiAoYi5rZXkgPCBhLmtleSkgewoJCQkgICAgcmV0dXJuIDE7CgkJCX0gZWxzZSB7CgkJCSAgICByZXR1cm4gLTE7CgkJCX0KCQl9OwoJCXByZUxpc3Quc29ydChzY29yZUNtcCk7CgoJCS8vIHVwZGF0ZSBwZW5kaW5nIGxpc3QKICAgICAgICBjb25zdCBwcm9kdWNlck51bWJlciA9IHRoaXMuX2dldCgicHJvZHVjZXJOdW1iZXIiKTsKCQljb25zdCByZXBsYWNlTnVtID0gTWF0aC5taW4ocHJlTGlzdC5sZW5ndGgsIE1hdGguZmxvb3IocHJvZHVjZXJOdW1iZXIgLyA2KSk7CgkJY29uc3Qgb2xkUHJlTGlzdCA9IFtdOwogICAgICAgIGZvciAobGV0IGtleSBpbiBwZW5kaW5nUHJvZHVjZXJMaXN0KSB7CgkJICAgIGNvbnN0IHggPSBwZW5kaW5nUHJvZHVjZXJMaXN0W2tleV07CgkJCW9sZFByZUxpc3QucHVzaCh7CgkJCQkia2V5IjogeCwKICAgICAgICAgICAgICAgICJwcmlvciI6IDEsCgkJCQkic2NvcmUiOiB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCB4KS5zY29yZQoJCQl9KTsKCQl9CgoJCS8vIHJlcGxhY2UgYXQgbW9zdCByZXBsYWNlTnVtIHByb2R1Y2VycwoJCWZvciAobGV0IGkgPSAwOyBpIDwgcmVwbGFjZU51bTsgaSsrKSB7CgkJCW9sZFByZUxpc3QucHVzaChwcmVMaXN0W2ldKTsKCQl9CgkJb2xkUHJlTGlzdC5zb3J0KHNjb3JlQ21wKTsKCQljb25zdCBuZXdMaXN0ID0gb2xkUHJlTGlzdC5zbGljZSgwLCBwcm9kdWNlck51bWJlcik7CgoJCWNvbnN0IGN1cnJlbnRMaXN0ID0gcGVuZGluZ1Byb2R1Y2VyTGlzdDsKCQl0aGlzLl9wdXQoImN1cnJlbnRQcm9kdWNlckxpc3QiLCBjdXJyZW50TGlzdCk7CgkJdGhpcy5fcHV0KCJwZW5kaW5nUHJvZHVjZXJMaXN0IiwgbmV3TGlzdC5tYXAoeCA9PiB4LmtleSkpOwoJCXRoaXMuX3B1dCgicGVuZGluZ0Jsb2NrTnVtYmVyIiwgdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKSk7CgoJCWZvciAobGV0IGkgPSAwOyBpIDwgcHJvZHVjZXJOdW1iZXI7IGkrKykgewoJCQlpZiAoIXBlbmRpbmdQcm9kdWNlckxpc3QuaW5jbHVkZXMoY3VycmVudExpc3RbaV0pKSB7CiAgICAgICAgICAgICAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBjdXJyZW50TGlzdFtpXSk7CiAgICAgICAgICAgICAgICBwcm9SZXMuc2NvcmUgPSAwOwogICAgICAgICAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgY3VycmVudExpc3RbaV0sIDApOwoJCQl9CgkJfQoJfQoKfQoKbW9kdWxlLmV4cG9ydHMgPSBWb3RlQ29udHJhY3Q7Cg=="]'},
                    {'contract': 'iost.vote', 'actionName': 'InitProducer',
                     'data': '["IOSTfQFocqDn7VrKV7vvPqhAQGyeFU9XMYo5SNn5yQbdbzC75wM7C"]'},
                    {'contract': 'iost.vote', 'actionName': 'InitAdmin',
                     'data': '["IOSTbbKmaZi1QRMfd7K8bK22KQSFuKadLhSNBw6tmyCHCRSvTr9QN"]'},
                    {'contract': 'iost.system', 'actionName': 'InitSetCode',
                     'data': '["iost.bonus", "Cgppb3N0LmJvbnVzEmUKBm5hdGl2ZRIFMS4wLjAaJwoKQ2xhaW1Cb251cxoGCGQQZBhkIOgHKgZzdHJpbmcqBm51bWJlchoYCgtjb25zdHJ1Y3RvchoGCGQQZBhkIOgHGhEKBGluaXQaBghkEGQYZCDoBxoFY29kZXM="]'}
                ],
                'publisher': {
                    'algorithm': 2,
                    'sig': b'}\x1c\x024\x18\x19\xa9+\x87\x8c\xb2t\xf7+L\xc2s\xfe8\xc0\xd0Lt\xbc\xb7*\xf8\xc1\x89\x91\x91\xa8\x88\xdd\xfa\x19S9\x8b\xb6\xcbJ\x95)\xeeN9\xea\x94#\x069\xca$u\xd9.\xf0(\xa7\xd4\x04\xed\x00',
                    'pubKey': b"\xa5UN\xfd\x0b\x1d\x10\x91y\x7f'\xcf\xea\xeaA\xfe\x0b\xeb\x9d\xc9Fw\x03\xe4\t\x99p:S\xe7\xd6C"
                }
            }],
            'receipts': [{
                'txHash': b"\x97\xff\xe4Lv\x91\x10[\x90\x02\xc2\x93\x86\x81h\n\rt\x94_\x8b\xa1\x01\xc1\x87;\xf3\x02\x17',\xdb",
                'gasUsage': 1514,
                'status': {},
                'succActionNum': 5
            }]
        }
        self.assertDictEqual(block_info, compare_dict)

    def test_get_block_by_num(self):
        block_num = 0
        block_info = self.iost.get_block_by_num(block_num)
        compare_dict = {
            'head': {
                'txsHash': b'\x04\xe5#=\xa0\xcfq\x89\xcdG\xe8\x1b\xb5\x84Y]\xce\xf6\xca+\xc7\xe1\x9d\xe7\xbd\xbf\x82xOB\xdaU',
                'merkleHash': b'\x05\xb3\xb7#R\r\xdcU\x9d\x1dr\x0f@.\x80wQ\xd2$\xf0\xfd\x8bCp\xe3=\xd2~\x82*\xcf?',
                'witness': 'IOST2FpDWNFqH9VuA8GbbVAwQcyYGHZxFeiTwSyaeyXnV84yJZAG7A'},
            'hash': b'%\x14\xd67\x1anx\xac\x1b\xdd\xa6\x97\xb1;J\x8e\xa7\xc2~\xb5>\xd2\xc0\xb5h\x07[6VS\x94\xe2',
            'txhash': [
                b"\x97\xff\xe4Lv\x91\x10[\x90\x02\xc2\x93\x86\x81h\n\rt\x94_\x8b\xa1\x01\xc1\x87;\xf3\x02\x17',\xdb"]
        }
        self.assertDictEqual(block_info, compare_dict)

    def test_get_block_by_num_complete(self):
        block_num = 0
        block_info = self.iost.get_block_by_num(block_num, complete=True)
        compare_dict = {
            'head': {
                'txsHash': b'\x04\xe5#=\xa0\xcfq\x89\xcdG\xe8\x1b\xb5\x84Y]\xce\xf6\xca+\xc7\xe1\x9d\xe7\xbd\xbf\x82xOB\xdaU',
                'merkleHash': b'\x05\xb3\xb7#R\r\xdcU\x9d\x1dr\x0f@.\x80wQ\xd2$\xf0\xfd\x8bCp\xe3=\xd2~\x82*\xcf?',
                'witness': 'IOST2FpDWNFqH9VuA8GbbVAwQcyYGHZxFeiTwSyaeyXnV84yJZAG7A'
            },
            'hash': b'%\x14\xd67\x1anx\xac\x1b\xdd\xa6\x97\xb1;J\x8e\xa7\xc2~\xb5>\xd2\xc0\xb5h\x07[6VS\x94\xe2',
            'txs': [{
                'gasLimit': 100000000,
                'actions': [
                    {'contract': 'iost.system', 'actionName': 'IssueIOST',
                     'data': '["IOSTfQFocqDn7VrKV7vvPqhAQGyeFU9XMYo5SNn5yQbdbzC75wM7C", 2100000000000000000]'},
                    {'contract': 'iost.system', 'actionName': 'InitSetCode',
                     'data': '["iost.vote", "Cglpb3N0LnZvdGUS7gIKCmphdmFzY3JpcHQSBTEuMC4wGg0KC2NvbnN0cnVjdG9yGgYKBGluaXQaFAoKY2FuX3VwZGF0ZSoGc3RyaW5nGhYKDEluaXRQcm9kdWNlcioGc3RyaW5nGhMKCUluaXRBZG1pbioGc3RyaW5nGjIKEFJlZ2lzdGVyUHJvZHVjZXIqBnN0cmluZyoGc3RyaW5nKgZzdHJpbmcqBnN0cmluZxowCg5VcGRhdGVQcm9kdWNlcioGc3RyaW5nKgZzdHJpbmcqBnN0cmluZyoGc3RyaW5nGhcKDUxvZ0luUHJvZHVjZXIqBnN0cmluZxoYCg5Mb2dPdXRQcm9kdWNlcioGc3RyaW5nGhwKElVucmVnaXN0ZXJQcm9kdWNlcioGc3RyaW5nGh4KBFZvdGUqBnN0cmluZyoGc3RyaW5nKgZudW1iZXIaIAoGVW52b3RlKgZzdHJpbmcqBnN0cmluZyoGbnVtYmVyGgYKBFN0YXQa3lZjb25zdCBzb2Z0RmxvYXRSYXRlID0gMWU4Owpjb25zdCBwcm9kdWNlclJlZ2lzdGVyRmVlID0gMTAwMCAqIDEwMDAgKiBzb2Z0RmxvYXRSYXRlOwpjb25zdCBwcmVQcm9kdWNlclRocmVzaG9sZCA9IDIxMDAgKiAxMDAwMDsKY29uc3Qgdm90ZUxvY2tUaW1lID0gMjAwOwpjb25zdCB2b3RlU3RhdEludGVydmFsID0gMjAwOwoKY2xhc3MgVm90ZUNvbnRyYWN0IHsKICAgIGNvbnN0cnVjdG9yKCkgewogICAgfQogICAgaW5pdCgpIHsKICAgICAgICB0aGlzLl9wdXQoImN1cnJlbnRQcm9kdWNlckxpc3QiLCBbXSk7CiAgICAgICAgdGhpcy5fcHV0KCJwZW5kaW5nUHJvZHVjZXJMaXN0IiwgW10pOwogICAgICAgIHRoaXMuX3B1dCgicGVuZGluZ0Jsb2NrTnVtYmVyIiwgMCk7CiAgICB9CgogICAgSW5pdFByb2R1Y2VyKHByb0lEKSB7CiAgICAJY29uc3QgYm4gPSB0aGlzLl9nZXRCbG9ja051bWJlcigpOwogICAgCWlmKGJuICE9PSAwKSB7CiAgICAJCXRocm93IG5ldyBFcnJvcigiaW5pdCBvdXQgb2YgZ2VuZXNpcyBibG9jayIpCgkJfQoKICAgIAlsZXQgcGVuZGluZ1Byb2R1Y2VyTGlzdCA9IHRoaXMuX2dldCgicGVuZGluZ1Byb2R1Y2VyTGlzdCIpOwoJCXBlbmRpbmdQcm9kdWNlckxpc3QucHVzaChwcm9JRCk7CiAgICAgICAgY29uc3Qga2V5Q21wID0gZnVuY3Rpb24oYSwgYikgewogICAgICAgICAgICBpZiAoYiA8IGEpIHsKICAgICAgICAgICAgICAgIHJldHVybiAxOwogICAgICAgICAgICB9IGVsc2UgewogICAgICAgICAgICAgICAgcmV0dXJuIC0xOwogICAgICAgICAgICB9CiAgICAgICAgfTsKICAgICAgICBwZW5kaW5nUHJvZHVjZXJMaXN0LnNvcnQoa2V5Q21wKTsKICAgICAgICB0aGlzLl9wdXQoInBlbmRpbmdQcm9kdWNlckxpc3QiLCBwZW5kaW5nUHJvZHVjZXJMaXN0KTsKCiAgICAgICAgY29uc3QgcHJvZHVjZXJOdW1iZXIgPSBwZW5kaW5nUHJvZHVjZXJMaXN0Lmxlbmd0aDsKICAgICAgICB0aGlzLl9wdXQoInByb2R1Y2VyTnVtYmVyIiwgcHJvZHVjZXJOdW1iZXIpOwoKICAgICAgICBjb25zdCByZXQgPSBCbG9ja0NoYWluLmRlcG9zaXQocHJvSUQsIHByb2R1Y2VyUmVnaXN0ZXJGZWUpOwogICAgICAgIGlmIChyZXQgIT09IDApIHsKICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJjb25zdHJ1Y3RvciBkZXBvc2l0IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CiAgICAgICAgfQogICAgICAgIHRoaXMuX21hcFB1dCgicHJvZHVjZXJUYWJsZSIsIHByb0lELCB7CiAgICAgICAgICAgICJsb2MiOiAiIiwKICAgICAgICAgICAgInVybCI6ICIiLAogICAgICAgICAgICAibmV0SWQiOiAiIiwKICAgICAgICAgICAgIm9ubGluZSI6IHRydWUsCiAgICAgICAgICAgICJzY29yZSI6IDAsCiAgICAgICAgICAgICJ2b3RlcyI6IDAKICAgICAgICB9KTsKICAgIH0KCiAgICBJbml0QWRtaW4oYWRtaW5JRCkgewogICAgICAgIGNvbnN0IGJuID0gdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKTsKICAgICAgICBpZihibiAhPT0gMCkgewogICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoImluaXQgb3V0IG9mIGdlbmVzaXMgYmxvY2siKQogICAgICAgIH0KICAgICAgICB0aGlzLl9wdXQoImFkbWluSUQiLCBhZG1pbklEKTsKICAgIH0KCiAgICBjYW5fdXBkYXRlKGRhdGEpIHsKICAgICAgICBjb25zdCBhZG1pbiA9IHRoaXMuX2dldCgiYWRtaW5JRCIpOwogICAgICAgIHRoaXMuX3JlcXVpcmVBdXRoKGFkbWluKTsKICAgICAgICByZXR1cm4gdHJ1ZTsKICAgIH0KCglfcmVxdWlyZUF1dGgoYWNjb3VudCkgewoJCWNvbnN0IHJldCA9IEJsb2NrQ2hhaW4ucmVxdWlyZUF1dGgoYWNjb3VudCk7CgkJaWYgKHJldCAhPT0gdHJ1ZSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInJlcXVpcmUgYXV0aCBmYWlsZWQuIHJldCA9ICIgKyByZXQpOwoJCX0KCX0KCglfZ2V0QmxvY2tOdW1iZXIoKSB7CgkJY29uc3QgYmkgPSBKU09OLnBhcnNlKEJsb2NrQ2hhaW4uYmxvY2tJbmZvKCkpOwoJCWlmICghYmkgfHwgYmkgPT09IHVuZGVmaW5lZCB8fCBiaS5udW1iZXIgPT09IHVuZGVmaW5lZCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoImdldCBibG9jayBudW1iZXIgZmFpbGVkLiBiaSA9ICIgKyBiaSk7CgkJfQoJCXJldHVybiBiaS5udW1iZXI7Cgl9CgogICAgX2dldChrKSB7CiAgICAgICAgcmV0dXJuIEpTT04ucGFyc2Uoc3RvcmFnZS5nZXQoaykpOwogICAgfQoJX3B1dChrLCB2KSB7CiAgICAgICAgY29uc3QgcmV0ID0gc3RvcmFnZS5wdXQoaywgSlNPTi5zdHJpbmdpZnkodikpOwogICAgICAgIGlmIChyZXQgIT09IDApIHsKICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJzdG9yYWdlIHB1dCBmYWlsZWQuIHJldCA9ICIgKyByZXQpOwogICAgICAgIH0KICAgIH0KICAgIF9tYXBHZXQoaywgZikgewogICAgICAgIHJldHVybiBKU09OLnBhcnNlKHN0b3JhZ2UubWFwR2V0KGssIGYpKTsKICAgIH0KICAgIF9tYXBQdXQoaywgZiwgdikgewogICAgICAgIGNvbnN0IHJldCA9IHN0b3JhZ2UubWFwUHV0KGssIGYsIEpTT04uc3RyaW5naWZ5KHYpKTsKICAgICAgICBpZiAocmV0ICE9PSAwKSB7CiAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcigic3RvcmFnZSBtYXAgcHV0IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CiAgICAgICAgfQogICAgfQoKICAgIF9tYXBEZWwoaywgZikgewogICAgICAgIGNvbnN0IHJldCA9IHN0b3JhZ2UubWFwRGVsKGssIGYpOwogICAgICAgIGlmIChyZXQgIT09IDApIHsKICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJzdG9yYWdlIG1hcCBkZWwgZmFpbGVkLiByZXQgPSAiICsgcmV0KTsKICAgICAgICB9CiAgICB9CgoJLy8gcmVnaXN0ZXIgYWNjb3VudCBhcyBhIHByb2R1Y2VyLCBuZWVkIHRvIHBsZWRnZSB0b2tlbgogICAgUmVnaXN0ZXJQcm9kdWNlcihhY2NvdW50LCBsb2MsIHVybCwgbmV0SWQpIHsKCQl0aGlzLl9yZXF1aXJlQXV0aChhY2NvdW50KTsKCQlpZiAoc3RvcmFnZS5tYXBIYXMoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50KSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIGV4aXN0cyIpOwoJCX0KCQljb25zdCByZXQgPSBCbG9ja0NoYWluLmRlcG9zaXQoYWNjb3VudCwgcHJvZHVjZXJSZWdpc3RlckZlZSk7CgkJaWYgKHJldCAhPT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInJlZ2lzdGVyIGRlcG9zaXQgZmFpbGVkLiByZXQgPSAiICsgcmV0KTsKCQl9CgkJdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCwgewoJCQkibG9jIjogbG9jLAoJCQkidXJsIjogdXJsLAoJCQkibmV0SWQiOiBuZXRJZCwKCQkJIm9ubGluZSI6IGZhbHNlLAoJCQkic2NvcmUiOiAwLAoJCQkidm90ZXMiOiAwCgkJfSk7CiAgICB9CgoJLy8gdXBkYXRlIHRoZSBpbmZvcm1hdGlvbiBvZiBhIHByb2R1Y2VyCiAgICBVcGRhdGVQcm9kdWNlcihhY2NvdW50LCBsb2MsIHVybCwgbmV0SWQpIHsKCQl0aGlzLl9yZXF1aXJlQXV0aChhY2NvdW50KTsKCQlpZiAoIXN0b3JhZ2UubWFwSGFzKCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCkpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJwcm9kdWNlciBub3QgZXhpc3RzIik7CgkJfQoJCWNvbnN0IHBybyA9IHRoaXMuX21hcEdldCgicHJvZHVjZXJUYWJsZSIsIGFjY291bnQpOwoJCXByby5sb2MgPSBsb2M7CgkJcHJvLnVybCA9IHVybDsKCQlwcm8ubmV0SWQgPSBuZXRJZDsKCQl0aGlzLl9tYXBQdXQoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50LCBwcm8pOwogICAgfQoKCS8vIHByb2R1Y2VyIGxvZyBpbiBhcyBvbmxpbmUgc3RhdGUKICAgIExvZ0luUHJvZHVjZXIoYWNjb3VudCkgewoJCXRoaXMuX3JlcXVpcmVBdXRoKGFjY291bnQpOwogICAgICAgIGlmICghc3RvcmFnZS5tYXBIYXMoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50KSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCBleGlzdHMsICIgKyBhY2NvdW50KTsKCQl9CiAgICAgICAgY29uc3QgcHJvID0gdGhpcy5fbWFwR2V0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCk7CgkJcHJvLm9ubGluZSA9IHRydWU7CiAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCwgcHJvKTsKICAgIH0KCgkvLyBwcm9kdWNlciBsb2cgb3V0IGFzIG9mZmxpbmUgc3RhdGUKICAgIExvZ091dFByb2R1Y2VyKGFjY291bnQpIHsKCQl0aGlzLl9yZXF1aXJlQXV0aChhY2NvdW50KTsKICAgICAgICBpZiAoIXN0b3JhZ2UubWFwSGFzKCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCkpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJwcm9kdWNlciBub3QgZXhpc3RzIik7CgkJfQoJCWlmICh0aGlzLl9nZXQoInBlbmRpbmdQcm9kdWNlckxpc3QiKS5pbmNsdWRlcyhhY2NvdW50KSB8fAogICAgICAgICAgICB0aGlzLl9nZXQoImN1cnJlbnRQcm9kdWNlckxpc3QiKS5pbmNsdWRlcyhhY2NvdW50KSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIGluIHBlbmRpbmcgbGlzdCBvciBpbiBjdXJyZW50IGxpc3QsIGNhbid0IGxvZ291dCIpOwoJCX0KICAgICAgICBjb25zdCBwcm8gPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBhY2NvdW50KTsKCQlwcm8ub25saW5lID0gZmFsc2U7CiAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCwgcHJvKTsKICAgIH0KCgkvLyByZW1vdmUgYWNjb3VudCBmcm9tIHByb2R1Y2VyIGxpc3QKCVVucmVnaXN0ZXJQcm9kdWNlcihhY2NvdW50KSB7CgkJdGhpcy5fcmVxdWlyZUF1dGgoYWNjb3VudCk7CiAgICAgICAgaWYgKCFzdG9yYWdlLm1hcEhhcygicHJvZHVjZXJUYWJsZSIsIGFjY291bnQpKSB7CgkJCXRocm93IG5ldyBFcnJvcigicHJvZHVjZXIgbm90IGV4aXN0cyIpOwoJCX0KICAgICAgICBpZiAodGhpcy5fZ2V0KCJwZW5kaW5nUHJvZHVjZXJMaXN0IikuaW5jbHVkZXMoYWNjb3VudCkgfHwKICAgICAgICAgICAgdGhpcy5fZ2V0KCJjdXJyZW50UHJvZHVjZXJMaXN0IikuaW5jbHVkZXMoYWNjb3VudCkpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJwcm9kdWNlciBpbiBwZW5kaW5nIGxpc3Qgb3IgaW4gY3VycmVudCBsaXN0LCBjYW4ndCB1bnJlZ2lzdCIpOwoJCX0KCQkvLyB3aWxsIGNsZWFyIHZvdGVzIGFuZCBzY29yZSBvZiB0aGUgcHJvZHVjZXIKCiAgICAgICAgdGhpcy5fbWFwRGVsKCJwcm9kdWNlclRhYmxlIiwgYWNjb3VudCk7CiAgICAgICAgdGhpcy5fbWFwRGVsKCJwcmVQcm9kdWNlck1hcCIsIGFjY291bnQpOwoKCQljb25zdCByZXQgPSBCbG9ja0NoYWluLndpdGhkcmF3KGFjY291bnQsIHByb2R1Y2VyUmVnaXN0ZXJGZWUpOwoJCWlmIChyZXQgIT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoIndpdGhkcmF3IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CgkJfQoJfQoKCS8vIHZvdGUsIG5lZWQgdG8gcGxlZGdlIHRva2VuCglWb3RlKHByb2R1Y2VyLCB2b3RlciwgYW1vdW50KSB7CgkJdGhpcy5fcmVxdWlyZUF1dGgodm90ZXIpOwoJCWFtb3VudCA9IE1hdGguZmxvb3IoYW1vdW50KTsKCiAgICAgICAgaWYgKCFzdG9yYWdlLm1hcEhhcygicHJvZHVjZXJUYWJsZSIsIHByb2R1Y2VyKSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCBleGlzdHMiKTsKCQl9CgoJCWNvbnN0IHJldCA9IEJsb2NrQ2hhaW4uZGVwb3NpdCh2b3RlciwgYW1vdW50ICogc29mdEZsb2F0UmF0ZSk7CgkJaWYgKHJldCAhPT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInZvdGUgZGVwb3NpdCBmYWlsZWQuIHJldCA9ICIgKyByZXQpOwoJCX0KCgkJbGV0IHZvdGVSZXMgPSB7fTsKICAgICAgICBpZiAoc3RvcmFnZS5tYXBIYXMoInZvdGVUYWJsZSIsIHZvdGVyKSkgewoJCSAgICB2b3RlUmVzID0gdGhpcy5fbWFwR2V0KCJ2b3RlVGFibGUiLCB2b3Rlcik7CgkJfQoJCS8vIHJlY29yZCB0aGUgYW1vdW50IGFuZCB0aW1lIG9mIHRoZSB2b3RlCgkJaWYgKHZvdGVSZXMuaGFzT3duUHJvcGVydHkocHJvZHVjZXIpKSB7CgkJCXZvdGVSZXNbcHJvZHVjZXJdLmFtb3VudCArPSBhbW91bnQ7CgkJfSBlbHNlIHsKICAgICAgICAgICAgdm90ZVJlc1twcm9kdWNlcl0gPSB7fTsKCQkJdm90ZVJlc1twcm9kdWNlcl0uYW1vdW50ID0gYW1vdW50OwoJCX0KCQl2b3RlUmVzW3Byb2R1Y2VyXS50aW1lID0gdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKTsKICAgICAgICB0aGlzLl9tYXBQdXQoInZvdGVUYWJsZSIsIHZvdGVyLCB2b3RlUmVzKTsKCgkJLy8gaWYgcHJvZHVjZXIncyB2b3RlcyA+PSBwcmVQcm9kdWNlclRocmVzaG9sZCwgdGhlbiBpbnNlcnQgaW50byBwcmVQcm9kdWNlciBtYXAKICAgICAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBwcm9kdWNlcik7CgkJcHJvUmVzLnZvdGVzICs9IGFtb3VudDsKCQlpZiAocHJvUmVzLnZvdGVzIC0gYW1vdW50IDwgIHByZVByb2R1Y2VyVGhyZXNob2xkICYmCgkJCQlwcm9SZXMudm90ZXMgPj0gcHJlUHJvZHVjZXJUaHJlc2hvbGQpIHsKCQkgICAgdGhpcy5fbWFwUHV0KCJwcmVQcm9kdWNlck1hcCIsIHByb2R1Y2VyLCB0cnVlKTsKCQl9CiAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgcHJvZHVjZXIsIHByb1JlcykKCX0KCgkvLyB1bnZvdGUKCVVudm90ZShwcm9kdWNlciwgdm90ZXIsIGFtb3VudCkgewogICAgICAgIGFtb3VudCA9IE1hdGguZmxvb3IoYW1vdW50KTsKCQl0aGlzLl9yZXF1aXJlQXV0aCh2b3Rlcik7CgoJCWlmICghc3RvcmFnZS5tYXBIYXMoInZvdGVUYWJsZSIsIHZvdGVyKSkgewogICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCB2b3RlZCIpOwogICAgICAgIH0KICAgICAgICBjb25zdCB2b3RlUmVzID0gdGhpcy5fbWFwR2V0KCJ2b3RlVGFibGUiLCB2b3Rlcik7CgkJaWYgKCF2b3RlUmVzLmhhc093blByb3BlcnR5KHByb2R1Y2VyKSkgewogICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoInByb2R1Y2VyIG5vdCB2b3RlZCIpCiAgICAgICAgfQogICAgICAgIGlmICh2b3RlUmVzW3Byb2R1Y2VyXS5hbW91bnQgPCBhbW91bnQpIHsKCQkJdGhyb3cgbmV3IEVycm9yKCJ2b3RlIGFtb3VudCBsZXNzIHRoYW4gZXhwZWN0ZWQiKQoJCX0KCQlpZiAodm90ZVJlc1twcm9kdWNlcl0udGltZSArIHZvdGVMb2NrVGltZT4gdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKSkgewoJCQl0aHJvdyBuZXcgRXJyb3IoInZvdGUgc3RpbGwgbG9ja2VkIikKCQl9CgkJdm90ZVJlc1twcm9kdWNlcl0uYW1vdW50IC09IGFtb3VudDsKCQl0aGlzLl9tYXBQdXQoInZvdGVUYWJsZSIsIHZvdGVyLCB2b3RlUmVzKTsKCgkJLy8gaWYgcHJvZHVjZXIgbm90IGV4aXN0LCBpdCdzIGJlY2F1c2UgcHJvZHVjZXIgaGFzIHVucmVnaXN0ZXJlZCwgZG8gbm90aGluZwoJCWlmIChzdG9yYWdlLm1hcEhhcygicHJvZHVjZXJUYWJsZSIsIHByb2R1Y2VyKSkgewoJCSAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBwcm9kdWNlcik7CgkJCWNvbnN0IG9yaSA9IHByb1Jlcy52b3RlczsKCQkJcHJvUmVzLnZvdGVzID0gTWF0aC5tYXgoMCwgb3JpIC0gYW1vdW50KTsKCQkJdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgcHJvZHVjZXIsIHByb1Jlcyk7CgoJCQkvLyBpZiBwcm9kdWNlcidzIHZvdGVzIDwgcHJlUHJvZHVjZXJUaHJlc2hvbGQsIHRoZW4gZGVsZXRlIGZyb20gcHJlUHJvZHVjZXIgbWFwCgkJCWlmIChvcmkgPj0gcHJlUHJvZHVjZXJUaHJlc2hvbGQgJiYKCQkJCQlwcm9SZXMudm90ZXMgPCBwcmVQcm9kdWNlclRocmVzaG9sZCkgewoJCQkgICAgdGhpcy5fbWFwRGVsKCJwcmVQcm9kdWNlck1hcCIsIHByb2R1Y2VyKTsKCQkJfQoJCX0KCgkJY29uc3QgcmV0ID0gQmxvY2tDaGFpbi53aXRoZHJhdyh2b3RlciwgYW1vdW50ICogc29mdEZsb2F0UmF0ZSk7CgkJaWYgKHJldCAhPT0gMCkgewoJCQl0aHJvdyBuZXcgRXJyb3IoIndpdGhkcmF3IGZhaWxlZC4gcmV0ID0gIiArIHJldCk7CgkJfQoKICAgICAgICBjb25zdCBzZXJ2aSA9IE1hdGguZmxvb3IoYW1vdW50ICogdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKSAvIHZvdGVMb2NrVGltZSk7CgkJY29uc3QgcmV0MiA9IEJsb2NrQ2hhaW4uZ3JhbnRTZXJ2aSh2b3Rlciwgc2VydmkpOwoJCWlmIChyZXQyICE9PSAwKSB7CgkJICAgIHRocm93IG5ldyBFcnJvcigiZ3JhbnQgc2VydmkgZmFpbGVkLiByZXQgPSAiICsgcmV0Mik7CiAgICAgICAgfQoJfQoKCS8vIGNhbGN1bGF0ZSB0aGUgdm90ZSByZXN1bHQsIG1vZGlmeSBwZW5kaW5nUHJvZHVjZXJMaXN0CglTdGF0KCkgewoJCS8vIGNvbnRyb2xsIGF1dGgKCQljb25zdCBibiA9IHRoaXMuX2dldEJsb2NrTnVtYmVyKCk7CgkJY29uc3QgcGVuZGluZ0Jsb2NrTnVtYmVyID0gdGhpcy5fZ2V0KCJwZW5kaW5nQmxvY2tOdW1iZXIiKTsKCQlpZiAoYm4gJSB2b3RlU3RhdEludGVydmFsIT09IDAgfHwgYm4gPD0gcGVuZGluZ0Jsb2NrTnVtYmVyKSB7CgkJCXRocm93IG5ldyBFcnJvcigic3RhdCBmYWlsZWQuIGJsb2NrIG51bWJlciBtaXNtYXRjaC4gcGVuZGluZyBibiA9ICIgKyBwZW5kaW5nQmxvY2tOdW1iZXIgKyAiLCBibiA9ICIgKyBibik7CgkJfQoKCQkvLyBhZGQgc2NvcmVzIGZvciBwcmVQcm9kdWNlck1hcAoJCWNvbnN0IHByZUxpc3QgPSBbXTsJLy8gbGlzdCBvZiBwcm9kdWNlcnMgd2hvc2Ugdm90ZSA+IHRocmVzaG9sZAogICAgICAgIGNvbnN0IHByZVByb2R1Y2VyTWFwS2V5cyA9IHN0b3JhZ2UubWFwS2V5cygicHJlUHJvZHVjZXJNYXAiKTsKCiAgICAgICAgY29uc3QgcGVuZGluZ1Byb2R1Y2VyTGlzdCA9IHRoaXMuX2dldCgicGVuZGluZ1Byb2R1Y2VyTGlzdCIpOwoKCQlmb3IgKGxldCBpIGluIHByZVByb2R1Y2VyTWFwS2V5cykgewoJCSAgICBjb25zdCBrZXkgPSBwcmVQcm9kdWNlck1hcEtleXNbaV07CgkJICAgIGNvbnN0IHBybyA9IHRoaXMuX21hcEdldCgicHJvZHVjZXJUYWJsZSIsIGtleSk7CiAgICAgICAgICAgIC8vIGRvbid0IGdldCBzY29yZSBpZiBpbiBwZW5kaW5nIHByb2R1Y2VyIGxpc3Qgb3Igb2ZmbGluZQoJCSAgICBpZiAoIXBlbmRpbmdQcm9kdWNlckxpc3QuaW5jbHVkZXMoa2V5KSAmJgogICAgICAgICAgICAgICAgcHJvLnZvdGVzID49IHByZVByb2R1Y2VyVGhyZXNob2xkICYmCiAgICAgICAgICAgICAgICBwcm8ub25saW5lID09PSB0cnVlKSB7CiAgICAgICAgICAgICAgICBwcmVMaXN0LnB1c2goewogICAgICAgICAgICAgICAgICAgICJrZXkiOiBrZXksCiAgICAgICAgICAgICAgICAgICAgInByaW9yIjogMCwKICAgICAgICAgICAgICAgICAgICAidm90ZXMiOiBwcm8udm90ZXMsCiAgICAgICAgICAgICAgICAgICAgInNjb3JlIjogcHJvLnNjb3JlCiAgICAgICAgICAgICAgICB9KTsKICAgICAgICAgICAgfQogICAgICAgIH0KICAgICAgICBmb3IgKGxldCBpID0gMDsgaSA8IHByZUxpc3QubGVuZ3RoOyBpKyspIHsKCQkJY29uc3Qga2V5ID0gcHJlTGlzdFtpXS5rZXk7CgkJCWNvbnN0IGRlbHRhID0gcHJlTGlzdFtpXS52b3RlcyAtIHByZVByb2R1Y2VyVGhyZXNob2xkOwogICAgICAgICAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBrZXkpOwoKICAgICAgICAgICAgcHJvUmVzLnNjb3JlICs9IGRlbHRhOwogICAgICAgICAgICB0aGlzLl9tYXBQdXQoInByb2R1Y2VyVGFibGUiLCBrZXksIHByb1Jlcyk7CgkJCXByZUxpc3RbaV0uc2NvcmUgKz0gZGVsdGE7CgkJfQoKCQkvLyBzb3J0IGFjY29yZGluZyB0byBzY29yZSBpbiByZXZlcnNlZCBvcmRlcgoJCWNvbnN0IHNjb3JlQ21wID0gZnVuY3Rpb24oYSwgYikgewoJCQlpZiAoYi5zY29yZSAhPSBhLnNjb3JlKSB7CgkJCSAgICByZXR1cm4gYi5zY29yZSAtIGEuc2NvcmU7CgkJCX0gZWxzZSBpZiAoYi5wcmlvciAhPSBhLnByaW9yKSB7CgkJCSAgICByZXR1cm4gYi5wcmlvciAtIGEucHJpb3I7CgkJCX0gZWxzZSBpZiAoYi5rZXkgPCBhLmtleSkgewoJCQkgICAgcmV0dXJuIDE7CgkJCX0gZWxzZSB7CgkJCSAgICByZXR1cm4gLTE7CgkJCX0KCQl9OwoJCXByZUxpc3Quc29ydChzY29yZUNtcCk7CgoJCS8vIHVwZGF0ZSBwZW5kaW5nIGxpc3QKICAgICAgICBjb25zdCBwcm9kdWNlck51bWJlciA9IHRoaXMuX2dldCgicHJvZHVjZXJOdW1iZXIiKTsKCQljb25zdCByZXBsYWNlTnVtID0gTWF0aC5taW4ocHJlTGlzdC5sZW5ndGgsIE1hdGguZmxvb3IocHJvZHVjZXJOdW1iZXIgLyA2KSk7CgkJY29uc3Qgb2xkUHJlTGlzdCA9IFtdOwogICAgICAgIGZvciAobGV0IGtleSBpbiBwZW5kaW5nUHJvZHVjZXJMaXN0KSB7CgkJICAgIGNvbnN0IHggPSBwZW5kaW5nUHJvZHVjZXJMaXN0W2tleV07CgkJCW9sZFByZUxpc3QucHVzaCh7CgkJCQkia2V5IjogeCwKICAgICAgICAgICAgICAgICJwcmlvciI6IDEsCgkJCQkic2NvcmUiOiB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCB4KS5zY29yZQoJCQl9KTsKCQl9CgoJCS8vIHJlcGxhY2UgYXQgbW9zdCByZXBsYWNlTnVtIHByb2R1Y2VycwoJCWZvciAobGV0IGkgPSAwOyBpIDwgcmVwbGFjZU51bTsgaSsrKSB7CgkJCW9sZFByZUxpc3QucHVzaChwcmVMaXN0W2ldKTsKCQl9CgkJb2xkUHJlTGlzdC5zb3J0KHNjb3JlQ21wKTsKCQljb25zdCBuZXdMaXN0ID0gb2xkUHJlTGlzdC5zbGljZSgwLCBwcm9kdWNlck51bWJlcik7CgoJCWNvbnN0IGN1cnJlbnRMaXN0ID0gcGVuZGluZ1Byb2R1Y2VyTGlzdDsKCQl0aGlzLl9wdXQoImN1cnJlbnRQcm9kdWNlckxpc3QiLCBjdXJyZW50TGlzdCk7CgkJdGhpcy5fcHV0KCJwZW5kaW5nUHJvZHVjZXJMaXN0IiwgbmV3TGlzdC5tYXAoeCA9PiB4LmtleSkpOwoJCXRoaXMuX3B1dCgicGVuZGluZ0Jsb2NrTnVtYmVyIiwgdGhpcy5fZ2V0QmxvY2tOdW1iZXIoKSk7CgoJCWZvciAobGV0IGkgPSAwOyBpIDwgcHJvZHVjZXJOdW1iZXI7IGkrKykgewoJCQlpZiAoIXBlbmRpbmdQcm9kdWNlckxpc3QuaW5jbHVkZXMoY3VycmVudExpc3RbaV0pKSB7CiAgICAgICAgICAgICAgICBjb25zdCBwcm9SZXMgPSB0aGlzLl9tYXBHZXQoInByb2R1Y2VyVGFibGUiLCBjdXJyZW50TGlzdFtpXSk7CiAgICAgICAgICAgICAgICBwcm9SZXMuc2NvcmUgPSAwOwogICAgICAgICAgICAgICAgdGhpcy5fbWFwUHV0KCJwcm9kdWNlclRhYmxlIiwgY3VycmVudExpc3RbaV0sIDApOwoJCQl9CgkJfQoJfQoKfQoKbW9kdWxlLmV4cG9ydHMgPSBWb3RlQ29udHJhY3Q7Cg=="]'},
                    {'contract': 'iost.vote', 'actionName': 'InitProducer',
                     'data': '["IOSTfQFocqDn7VrKV7vvPqhAQGyeFU9XMYo5SNn5yQbdbzC75wM7C"]'},
                    {'contract': 'iost.vote', 'actionName': 'InitAdmin',
                     'data': '["IOSTbbKmaZi1QRMfd7K8bK22KQSFuKadLhSNBw6tmyCHCRSvTr9QN"]'},
                    {'contract': 'iost.system', 'actionName': 'InitSetCode',
                     'data': '["iost.bonus", "Cgppb3N0LmJvbnVzEmUKBm5hdGl2ZRIFMS4wLjAaJwoKQ2xhaW1Cb251cxoGCGQQZBhkIOgHKgZzdHJpbmcqBm51bWJlchoYCgtjb25zdHJ1Y3RvchoGCGQQZBhkIOgHGhEKBGluaXQaBghkEGQYZCDoBxoFY29kZXM="]'}
                ],
                'publisher': {
                    'algorithm': 2,
                    'sig': b'}\x1c\x024\x18\x19\xa9+\x87\x8c\xb2t\xf7+L\xc2s\xfe8\xc0\xd0Lt\xbc\xb7*\xf8\xc1\x89\x91\x91\xa8\x88\xdd\xfa\x19S9\x8b\xb6\xcbJ\x95)\xeeN9\xea\x94#\x069\xca$u\xd9.\xf0(\xa7\xd4\x04\xed\x00',
                    'pubKey': b"\xa5UN\xfd\x0b\x1d\x10\x91y\x7f'\xcf\xea\xeaA\xfe\x0b\xeb\x9d\xc9Fw\x03\xe4\t\x99p:S\xe7\xd6C"
                }
            }]
        }
        self.assertDictEqual(block_info, compare_dict)

    def test_get_balance(self):
        account_id = '6d8jQzRcxawmTebQQhrWvBvbjpSp9CnPFCFQsuBoMWQc'
        balance = self.iost.get_balance(account_id, False)
        self.assertEqual(balance, 4000000000000)

    def test_get_net_id(self):
        id = self.iost.get_net_id()
        self.assertEqual(id, '12D3KooWGPpGc8gbaHGJ6BywPrUoUKpPUKPmbCyr3ZLfgQRqj9m5')

    def test_get_state(self):
        key = ''
        value = self.iost.get_state(key)
        print(value)


if __name__ == '__main__':
    tester = TestIOST()
    tester.setUp()
    tester.test_get_tx_by_hash()
