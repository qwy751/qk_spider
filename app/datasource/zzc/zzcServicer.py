# -*- coding: utf-8 -*-
import grpc

from .data_sources_pb2 import QueryServiceStub, Condition, Result


class ZccServicer():

    channel = grpc.insecure_channel('localhost:6565')
    stub = QueryServiceStub(channel)

    def __init__(self):
        pass

    def Query(self, condition):
        c = Condition(condition=condition)
        response = self.stub.Query(c)
        print("received:", response.message)
