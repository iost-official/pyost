from pyost.iost import IOST

if __name__ == '__main__':
    iost = IOST('192.168.99.100:30002')
    print(iost.get_node_info())
    print(iost.get_chain_info())
    print(iost.get_ram_info())
    print(iost.get_gas_ratio())