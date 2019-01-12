from __future__ import annotations
from typing import List
from enum import Enum
from pprint import pformat
from protobuf_to_dict import protobuf_to_dict
from pyost.rpc.pb import rpc_pb2 as pb


class Event:
    """Describes an event.

    Attributes:
        topic: The topic, such as ``CONTRACT_RECEIPT`` or ``CONTRACT_EVENT``.
        data: The data of the event.
        time: The timestamp of the event.
    """

    class Topic(Enum):
        CONTRACT_RECEIPT = pb.Event.CONTRACT_RECEIPT  #: Contract receipt.
        CONTRACT_EVENT = pb.Event.CONTRACT_EVENT  #: Contract event.
        UNKNOWN = -1  #: Unknown topic.

    def __init__(self):
        self.topic: Event.Topic = Event.Topic.UNKNOWN
        self.data: str = ''
        self.time: int = 0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, e: pb.Event) -> Event:
        """Deserializes a protobuf object to update this object's members.

        Args:
            e: The protobuf object.

        Returns:
            Itself.
        """
        self.topic = e.topic
        self.data = e.data
        self.time = e.time
        return self

    def to_raw(self) -> pb.Event:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.Event(
            topic=self.topic,
            data=self.data,
            time=self.time
        )


class SubscribeRequest:
    """Used to send event subscription request to the API.

    Args:
        topics: The list of `Topic` to monitor.
        contract_id: Filter the events to this contract id.

    Attributes:
        topics: The list of `Topic` to monitor.
        filter: A `Filter` object that contains the contract id to filter.
    """

    class Filter:
        """Contains a contract id to filter events.

        Args:
            contract_id: Filter events for this contract id.

        Attributes:
            contract_id: Filter events for this contract id.
        """

        def __init__(self, contract_id: str = ''):
            self.contract_id: str = contract_id

        def from_raw(self, f: pb.SubscribeRequest.Filter) -> SubscribeRequest.Filter:
            """Deserializes a protobuf object to update this object's members.

            Args:
                f: The protobuf object.

            Returns:
                Itself.
            """
            self.contract_id = f.contract_id
            return self

        def to_raw(self) -> pb.SubscribeRequest.Filter:
            """Serializes this object's members to a protobuf object.

            Returns:
                A protobuf object.
            """
            return pb.SubscribeRequest.Filter(
                contract_id=self.contract_id
            )

    def __init__(self, topics: List[Event.Topic] = None, contract_id: str = ''):
        self.topics: List[Event.Topic] = topics or []
        self.filter = SubscribeRequest.Filter(contract_id)

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, sr: pb.SubscribeRequest) -> SubscribeRequest:
        """Deserializes a protobuf object to update this object's members.

        Args:
            sr: The protobuf object.

        Returns:
            Itself.
        """
        self.topics = Event.Topic(sr.topics)
        self.filter = SubscribeRequest.Filter().from_raw(sr.filter)
        return self

    def to_raw(self) -> pb.SubscribeRequest:
        """Serializes this object's members to a protobuf object.

        Returns:
            A protobuf object.
        """
        return pb.SubscribeRequest(
            topics=[topic.value for topic in self.topics],
            filter=self.filter.to_raw() if self.filter is not None else None
        )
