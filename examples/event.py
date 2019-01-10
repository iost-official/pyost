from pyost.iost import IOST
from pyost.event import Event

if __name__ == '__main__':
    iost = IOST('35.180.171.246:30002')

    topics = [Event.Topic.CONTRACT_RECEIPT, Event.Topic.CONTRACT_EVENT]
    contract_id = 'token.iost'

    for event in iost.subscribe(topics, contract_id):
        print(event)
