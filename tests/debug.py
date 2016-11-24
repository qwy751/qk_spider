# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
import pydevd
pydevd.settrace('licho.iok.la', port=44957, stdoutToServer=True, stderrToServer=True)
