#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import shutil
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")
import Hoi4Converter
from Hoi4Converter.mappings import *
from Hoi4Converter.converter import *


def patch_naval_ai_equipment(kx_path, out_folder):
    ai_equipment_folder = os.path.join("common", "ai_equipment")
    os.makedirs(os.path.join(out_folder, ai_equipment_folder), exist_ok=True)
    naval_path = os.path.join(ai_equipment_folder,
                              "generic_naval.txt")
    in_file = os.path.join(kx_path, naval_path)
    out_file = os.path.join(out_folder, naval_path)

    tmap1 = [[has_key_and_val, ["has_tech", ["dp_secondary_battery"]]],
             [add_multiple, [["has_tech", ["basic_dp_medium_battery"]]]]]
    tmap2 = [[has_key_and_val, ["has_tech", ["dp_secondary_battery"]]],
             [remove, ["has_tech", ["dp_secondary_battery"]]]]
    
    apply_maps_on_file(in_file, out_file, [tmap1, tmap2])
    

def patch(kx_path, out_folder):
    patch_naval_ai_equipment(kx_path, out_folder)
