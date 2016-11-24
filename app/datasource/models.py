# -*- coding: utf-8 -*-
from app import db


class OriginData(db.Model):
    """
    用于存输入输出的原始数据
    """
    def __init__(self, **kwargs):
        super(OriginData, self).__init__(**kwargs)
    id = db.Column(db.Integer, primary_key=True)
    request_time = db.column(db.TIMESTAMP)
    source = db.column(db.String)
    source_request = db.column(db.Text)
    source_result = db.column(db.Text)
