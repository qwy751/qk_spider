# -*- coding: utf-8 -*-

from app.util.logger import logger

import pydevd
pydevd.settrace('licho.iok.la', port=44957, stdoutToServer=True, stderrToServer=True)

logger.error("abc")
