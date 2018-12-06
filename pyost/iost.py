import grpc

from pyost.grpc.github.com.iost_official.go_iost.rpc import apis_pb2_grpc
from google.protobuf import empty_pb2


class IOST():
    def __init__(self, url):
        self._channel = grpc.insecure_channel(url)
        self._stub = apis_pb2_grpc.ApisStub(self._channel)

    def get_net_id(self):
        return self._stub.GetNetID(empty_pb2.Empty())
