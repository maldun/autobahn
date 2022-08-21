#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import json
import shutil
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")
import Hoi4Converter
from Hoi4Converter.mappings import *
from Hoi4Converter.converter import *


def copy_json(json_file, rt56_path, out_path):
    with open(json_file, 'r') as fp:
        dic = json.load(fp)
    for folder, file_list in dic.items():
        os.makedirs(out_path, exist_ok=True)
        for org_file, out_list in file_list.items():
            in_file = os.path.join(rt56_path, folder, org_file)
            if len(out_list) == 0:
                out_file = os.path.join(out_path, folder, org_file)
            elif len(out_list) == 1:
                out_file = os.path.join(out_path, folder, out_list[-1])
            elif len(out_list) == 2:
                out_file = os.path.join(out_path, out_list[0], out_list[-1])
            else:
                import pdb; pdb.set_trace()
            os.makedirs(os.path.split(out_file)[0], exist_ok=True)
            shutil.copy2(in_file, out_file)


TANK_COPY_JSON = "rt56_copy_tank.json"
def tanks(rt56_path, out_path):
    copy_json(TANK_COPY_JSON, rt56_path, out_path)
