from __future__ import annotations
from typing import List
import json
from pprint import pformat
from protobuf_to_dict import protobuf_to_dict
from pyost.rpc.pb import rpc_pb2 as pb
from pyost.transaction import AmountLimit


class Contract:
    """Contains a contract's code and ABI.

    Attributes:
        id: The contract id.
        code: The source code of the contract as a JSONified string.
        language: The programming language of the contract, such as ``javascript``.
        version: The version of the ABI.
        abis: The list of functions ABI.
    """

    class ABI:
        """Describes a function of a `Contract`'s ABI.

        Attributes:
            name: The name of the function.
            args: The list of the function's argument names.
            amount_limit: A list of `AmountLimit` objects.
        """
        def __init__(self):
            self.name: str = ''
            self.args: List[str] = []
            self.amount_limit: List[AmountLimit] = []

        def __str__(self) -> str:
            return pformat(protobuf_to_dict(self.to_raw()))

        def from_raw(self, abi: pb.Contract.ABI) -> Contract.ABI:
            """Deserializes a protobuf object to update this object's members.

            Args:
                abi: The protobuf object.

            Returns:
                Itself.
            """
            self.name = abi.name
            self.args = abi.args
            self.amount_limit = [AmountLimit().from_raw(al) for al in abi.amount_limit
                                 ] if abi.amount_limit is not None else []
            return self

        def to_raw(self) -> pb.Contract.ABI:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.Contract.ABI(
                name=self.name,
                args=self.args,
                amount_limit=[al.to_raw() for al in self.amount_limit]
            )

        def from_json(self, d: dict) -> Contract.ABI:
            """Deserializes a dictionary to update this object's members.

            Warnings:
                This seems to use an old format as input: ``amount_limit`` is written ``amountLimit``
                    and ``value`` is written ``val``.

            Args:
                d: The dictionary.

            Returns:
                Itself.
            """
            self.name = d['name'] if 'name' in d else ''
            self.args = d['args'] if 'args' in d else []
            if 'amountLimit' in d:
                for al in d['amountLimit']:
                    token = al['token'] if 'token' in al else ''
                    value = al['val'] if 'val' in al else ''
                    self.amount_limit.append(AmountLimit(token, value))
            return self

        def to_dict(self) -> dict:
            """Serializes this object into a dictionary.

            Warnings:
                This seems to use an old format as output: ``amount_limit`` is written ``amountLimit``
                    and ``value`` is written ``val``.

            Returns:
                A dictionary.
            """
            d = {
                'name': self.name,
                'args': self.args,
            }
            if len(self.amount_limit) > 0:
                d['amountLimit'] = [{'token': al.token, 'val': al.value} for al in self.amount_limit]
            return d

    def __init__(self, id: str = '', code: str = '', language: str = '', version: str = ''):
        self.id: str = id
        self.code: str = code
        self.language: str = language
        self.version: str = version
        self.abis: List[Contract.ABI] = []

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, c: pb.Contract) -> Contract:
        """Deserializes a protobuf object to update this object's members.

        Args:
            c: The protobuf object.

        Returns:
            Itself.
        """
        self.id = c.id
        self.code = c.code
        self.language = c.language
        self.version = c.version
        self.abis = [Contract.ABI().from_raw(abi) for abi in c.abis
                     ] if c.abis is not None else []
        return self

    def to_raw(self) -> pb.Contract:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.Contract(
            id=self.id,
            code=self.code,
            language=self.language,
            version=self.version,
            abis=[abi.to_raw() for abi in self.abis]
        )

    def from_json(self, d: dict) -> Contract:
        """Deserializes a dictionary to update this object's members.

        Warnings:
            This seems to use an old format as input: ``language`` is written ``lang``.

        Args:
            d: The dictionary.

        Returns:
            Itself.
        """
        self.language = d['lang'] if 'lang' in d else ''
        self.version = d['version'] if 'version' in d else ''
        if 'abi' in d:
            for abi in d['abi']:
                self.abis.append(Contract.ABI().from_json(abi))
        return self

    def to_json(self) -> str:
        """Serializes this object to a JSON string.
        This is used to publish a contract on the blockchain.

        Warnings:
            This seems to use an old format as input: ``language`` is written ``lang``,
                ``id`` is written ``ID`` and ``lang``, ``version`` and ``abi`` are packed
                into a sub dictionary named ``info``.

        Returns:
            A JSON string.
        """
        return json.dumps({
            'ID': self.id,
            'info': {
                'lang': self.language,
                'version': self.version,
                'abi': [abi.to_dict() for abi in self.abis]
            },
            'code': self.code
        })


if __name__ == '__main__':
    with open('../examples/contract/lucky_bet.js.abi', 'r') as f:
        import json

        data = json.load(f)
    contract = Contract().from_json(data)
    print(contract)
    print(contract.to_json())
