import os, sys
from os import path
from datetime import datetime
import json
from collections import namedtuple

__author__ = 'zadjii'

ResultAndData = namedtuple('ResultAndData', 'success, data')

def Error(data=None):
    return ResultAndData(False, data)
def Success(data=None):
    return ResultAndData(True, data)

KEEP_ROOT = path.abspath(path.dirname(path.dirname(__file__)))
KEEP_BACKEND_ROOT = os.path.join(KEEP_ROOT, '.keep')

INVALID_ID = -1
GLOBALS_ID = 0
FIRST_VALID_ID = GLOBALS_ID+1

################################################################################
# Turns VT output support on
def enable_vt_support():
    if os.name == 'nt':
        import ctypes
        hOut = ctypes.windll.kernel32.GetStdHandle(-11)
        out_modes = ctypes.c_uint32()
        ENABLE_VT_PROCESSING = ctypes.c_uint32(0x0004)
        # ctypes.addressof()
        ctypes.windll.kernel32.GetConsoleMode(hOut, ctypes.byref(out_modes))
        out_modes = ctypes.c_uint32(out_modes.value | 0x0004)
        ctypes.windll.kernel32.SetConsoleMode(hOut, out_modes)
################################################################################

def normalize_path(some_path):
    new_path = os.path.abspath(some_path)
    new_path = os.path.realpath(new_path)
    return new_path

def get_working_workspace():
    if 'KEEP_WORKSPACE' in os.environ:
        return int(os.environ['KEEP_WORKSPACE'])
    else:
        return GLOBALS_ID


def parse_id(id_token):
    rd = Error()

    if '/' in id_token:
        parts = id_token.split('/')
        if len(parts) > 2:
            rd = Error('Invalid arg {}'.format(id_token))
        else:
            try:
                workspace_id = int(parts[0]) if len(parts[0]) > 0 else get_working_workspace()
                element_id = int(parts[1]) if len(parts[1]) > 0 else None
                rd = Success(workspace_id, element_id)
            except Exception as e:
                rd = Error('Error parsing arg {}'.format(id_token))
                print parts
    else:
        rd = Success((get_working_workspace(), int(id_token)))
    return rd
