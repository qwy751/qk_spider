import grpc

from . import cup_query_pb2


def query(bakCardId, name, IDCard, phone):
    """
    调用远端银联查询函数
    :return: 银联返回的结果
    """
    channel = grpc.insecure_channel('192.168.1.20:6565')
    stub = cup_query_pb2.CupQueryServiceStub(channel)
    response = stub.Query(cup_query_pb2.CupCondition(bakCardId=bakCardId,
                                                     name=name,
                                                     IDCard=IDCard,
                                                     phone=phone))
    return response

