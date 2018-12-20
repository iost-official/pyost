from unittest import main, TestCase
import base58
from pyost.transaction import Transaction, Action


class TestTransaction(TestCase):
    def setUp(self):
        pass

    def test_new_action(self):
        action = Action('iost.system', 'Transfer',
                        '["IOSTfQFocqDn7VrKV7vvPqhAQGyeFU9XMYo5SNn5yQbdbzC75wM7C", "6d8jQzRcxawmTebQQhrWvBvbjpSp9CnPFCFQsuBoMWQc", 1000000000000]')
        raw = action.encode()
        print(raw)
        action.decode(raw)


if __name__ == '__main__':
    tester = TestTransaction()
    tester.setUp()
    tester.test_new_action()
