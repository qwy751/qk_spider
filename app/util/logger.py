# -*- coding: utf-8 -*-
import logging
import logging.config
import os

up_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

logging.config.fileConfig(up_path + '/log.ini')

logger = logging.getLogger('spider')

