from __future__ import annotations
from typing import List
from enum import Enum
from pprint import pformat
from protobuf_to_dict import protobuf_to_dict
from pyost.api.rpc.pb import rpc_pb2 as pb


class Event:
    class Topic(Enum):
        CONTRACT_RECEIPT = pb.Event.CONTRACT_RECEIPT
        CONTRACT_EVENT = pb.Event.CONTRACT_EVENT
        UNKNOWN = -1

    def __init__(self):
        self.topic: Event.Topic = Event.Topic.UNKNOWN
        self.data: str = ''
        self.time: int = 0

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, e: pb.Event) -> Event:
        self.topic = e.topic
        self.data = e.data
        self.time = e.time
        return self

    def to_raw(self) -> pb.Event:
        return pb.Event(
            topic=self.topic,
            data=self.data,
            time=self.time
        )


class SubscribeRequest:
    class Filter:
        def __init__(self, contract_id: str = ''):
            self.contract_id: str = contract_id

        def from_raw(self, f: pb.SubscribeRequest.Filter) -> SubscribeRequest.Filter:
            self.contract_id = f.contract_id
            return self

        def to_raw(self) -> pb.SubscribeRequest.Filter:
            return pb.SubscribeRequest.Filter(
                contract_id=self.contract_id
            )

    def __init__(self, topics: List[Event.Topic] = None, contract_id: str = ''):
        self.topics: List[Event.Topic] = topics or []
        self.filter = SubscribeRequest.Filter(contract_id)

    def __str__(self) -> str:
        return pformat(protobuf_to_dict(self.to_raw()))

    def from_raw(self, sr: pb.SubscribeRequest) -> SubscribeRequest:
        self.topics = Event.Topic(sr.topics)
        self.filter = SubscribeRequest.Filter().from_raw(sr.filter)
        return self

    def to_raw(self) -> pb.SubscribeRequest:
        return pb.SubscribeRequest(
            topics=[topic.value for topic in self.topics],
            filter=self.filter.to_raw() if self.filter is not None else None
        )
