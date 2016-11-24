# -*- coding: utf-8 -*-

import os
import jpype

from app.datasource.third import Third
from app.util.logger import logger
from . import cupGrpcClient


class ChinaUnionPay(Third):
    """
    银联智策
    """
    source = 'cup'

    def query(self, *args, **kwargs):
        result = None
        try:
            result = cupGrpcClient.query(bakCardId=kwargs['card_id'],
                                         phone=kwargs['mobile_num'],
                                         name=kwargs['user_name_cn'],
                                         IDCard=kwargs['personal_id'])
        except Exception as ex:
            logger.error(ex)

        return result, ChinaUnionPay.source




