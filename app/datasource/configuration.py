# -*- coding: utf-8 -*-
import yaml
import os


def config():
    """
    读取第三方数据源的配置
    :return:
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    stream = open(basedir + '/config.yml', 'r', encoding='utf8')
    configuration = yaml.load(stream)
    return configuration

config = config()

