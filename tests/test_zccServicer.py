# -*- coding: utf-8 -*-
from unittest import TestCase

from app.datasource.zzc.zzcServicer import ZccServicer


class TestZccServicer(TestCase):
    zzcServicer = ZccServicer()

    def Query(self):
        self.zzcServicer.Query("sun")


if __name__ == '__main__':
    tzs = TestZccServicer()
    tzs.Query()
