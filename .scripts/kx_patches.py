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

INTERFACE_FOLDER = "interface"

def make_folder_in_out_file(folder_name, filename, in_path, out_path):
    os.makedirs(os.path.join(out_path, folder_name), exist_ok=True)
    in_file = os.path.join(in_path, folder_name, filename)
    out_file = os.path.join(out_path, folder_name, filename)

    return in_file, out_file

def patch_main_menu(kx_path, out_folder):
    filename = "frontendmainview.gui"
    in_file, out_file = make_folder_in_out_file(INTERFACE_FOLDER, filename,
                                                kx_path, out_folder)
    
    tmap = [[has_key_and_val, ["name", ['"frontend_background"']]],
             [add_multiple, [["iconType", [["name",['"autobahn_logo"']],
                                            ["spriteType",['"GFX_autobahn_logo"']],
                                            ["position",
                                             [['x',[50]],
                                              ['y',[150]],
                                              ]
                                           ]
                                           ]
                              ]
              ]]
            ]
    apply_maps_on_file(in_file, out_file, [tmap])

    
def patch_naval_ai_equipment(kx_path, out_folder):
    ai_equipment_folder = os.path.join("common", "ai_equipment")
    naval_path = "generic_naval.txt"
    in_file, out_file = make_folder_in_out_file(ai_equipment_folder, naval_path,
                                                kx_path, out_folder)

    tmap1 = [[has_key_and_val, ["has_tech", ["dp_secondary_battery"]]],
             [add_multiple, [["has_tech", ["basic_dp_medium_battery"]]]]]
    tmap2 = [[has_key_and_val, ["has_tech", ["dp_secondary_battery"]]],
             [remove, ["has_tech", ["dp_secondary_battery"]]]]
    
    apply_maps_on_file(in_file, out_file, [tmap1, tmap2])
    

def patch(kx_path, out_folder):
    patch_main_menu(kx_path, out_folder)
    patch_naval_ai_equipment(kx_path, out_folder)
