class Account():
    def __init__(self, id):
        self._id = id
        self._key_id = {}
        self._key_pair = {}

    def add_key_pair(self, kp, permission=''):
        if permission == '':
            if kp.id not in self._key_id:
                raise KeyError(f'Key {kp.id} does not exist.')
            permission = self._key_id[kp.id]
        self._key_pair[permission] = kp

    def get_id(self):
        return self._id

    def get_key_pair(self, permission):
        return self._key_pair[permission]

    def sign(self, tx, permission):
        tx.add_sign(self._key_pair[permission])

    def sign_tx(self, tx):
        tx.add_publish_sign(self._id, self._key_pair['active'])
