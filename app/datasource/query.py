# -*- coding: utf-8 -*-
import json
import sys

import concurrent

from app.util.jvm import start_jvm

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from config import DevelopmentConfig

if sys.version[0] == '2':
    import Queue as queue
else:
    import queue

import threading
from abc import ABCMeta, abstractmethod

from app.datasource.cup.cup import ChinaUnionPay
from app.datasource.pengyuan.pengyuan import PengYuan
from app.datasource.zzc.zzc import Zzc
from app.util.logger import logger
from multiprocessing.pool import ThreadPool
from app.util.logger import logger
from app.info import Person
from sqlalchemy.exc import StatementError


class Query:
    data_sources = [Zzc, PengYuan]  # , ChinaUnionPay]
    data_queue = queue.Queue()

    def query(self, *args, **kwargs):
        name = kwargs['user_name_cn']
        identity = kwargs['personal_id']
        self.create_person(name, identity)
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.data_sources) * 5) as executor:

            future_func = {executor.submit(source().query, *args, **kwargs) for source in self.data_sources}
            try:
                for future in concurrent.futures.as_completed(future_func, 30):
                    try:
                        data = future.result()
                        self.data_queue.put(data)
                    except Exception as exc:
                        logger.error('查询异常: %s' % exc)
            except TimeoutError as te:
                logger.error(te)

        final_result = {}
        while True:
            try:
                data, source = self.data_queue.get_nowait()
                final_result[source] = data
            except queue.Empty:
                break

        result_j = final_result
        print("结果" + repr(result_j))
        return result_j

    @staticmethod
    def create_person(name, identity):
        person = Person.query.filter_by(identity=identity).first()

        if person is None:
            person = Person(identity=identity)
        person.name = name
        try:
            from app import db
            db.session.add(person)
            db.session.commit()
        except Exception as e:
            logger.error(e)
        return person
