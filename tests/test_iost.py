from pyost.iost import IOST


def test_iost():
    iost = IOST('localhost:30002')
    print(iost.get_net_id())


if __name__ == '__main__':
    test_iost()
