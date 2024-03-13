#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2022 HalfMarble LLC
# Copyright 2019 Hiroshi Murayama <opiopan@gmail.com>

import os
from hm_gerber_tool.common import loads as loads_org
from hm_gerber_tool.exceptions import ParseError
from hm_gerber_tool.utils import detect_file_format
import hm_gerber_tool.rs274x
import hm_gerber_tool.ipc356
import hm_gerber_ex.rs274x
import hm_gerber_ex.excellon
#import hm_gerber_ex.dxf


def read(filename, format=None):
    with open(filename, 'r') as f:
        data = f.read()
    return loads(data, filename, format=format)


def loads(data, filename=None, format=None):
    if os.path.splitext(filename if filename else '')[1].lower() == '.dxf':
        return hm_gerber_ex.dxf.loads(data, filename)

    fmt = detect_file_format(data)
    if fmt == 'rs274x':
        file = hm_gerber_ex.rs274x.loads(data, filename=filename)
        return hm_gerber_ex.rs274x.GerberFile.from_gerber_file(file)
    elif fmt == 'excellon':
        return hm_gerber_ex.excellon.loads(data, filename=filename, format=format)
    elif fmt == 'ipc_d_356':
        return ipc356.loads(data, filename=filename)
    else:
        raise ParseError('Unable to detect file format')


def rectangle(width, height, left=0, bottom=0, units='metric', draw_mode=None, filename=None):
    return hm_gerber_ex.dxf.DxfFile.rectangle(
        width, height, left, bottom, units, draw_mode, filename)
