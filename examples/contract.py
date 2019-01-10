from pyost.iost import IOST

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    print('token.iost contract:')
    for abi in iost.get_contract('token.iost').abis:
        print(abi.name, abi.args)
