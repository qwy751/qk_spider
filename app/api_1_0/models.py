# -*- coding: utf-8 -*-

from app import db


class InnerResult(db.Model):
    """
    内部使用的数据格式
    """
    def __init__(self, **kwargs):
        super(InnerResult, self).__init__(**kwargs)
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.Text, unique=True)
    result = db.Column(db.Binary)
    received_time = db.Column(db.TIMESTAMP)

    def __repr__(self):
        return 'condition:{}, received_time:{}, result:{}'\
            .format(self.condition, self.received_time, self.result)


