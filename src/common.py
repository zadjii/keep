import os, sys
from os import path
from datetime import datetime
import json
from box import Box

from collections import namedtuple
ResultAndData = namedtuple('ResultAndData', 'success, data')

def Error(data=None):
    return ResultAndData(False, data)
def Success(data=None):
    return ResultAndData(True, data)

KEEP_ROOT = path.abspath(path.dirname(path.dirname(__file__)))
KEEP_BACKEND_ROOT = os.path.join(KEEP_ROOT, '.keep')

INVALID_ID = -1
