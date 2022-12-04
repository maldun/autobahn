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

from update_script import SCRIPTED_EFFECTS_PATH, SET_TECH_KEY



def make_folder_in_out_file(folder_name, filename, in_path, out_path):
    os.makedirs(os.path.join(out_path, folder_name), exist_ok=True)
    in_file = os.path.join(in_path, folder_name, filename)
    out_file = os.path.join(out_path, folder_name, filename)

    return in_file, out_file


def patch_USA_tech(mod_folder, out_folder):
    fname = "01_American Civil War effects.txt"
    in_file, out_file = make_folder_in_out_file(SCRIPTED_EFFECTS_PATH, fname,
                                                mod_folder, out_folder) 
    ### New Tech##################
    new_tech = {"aluminum_production_1",
                    "camo",
                    "etax_doctrine",
                    "r56_gw_railway_gun",
                    "r56_railway_mortar_subtech",
                    "steel_production_1",
                    "transport_plane1"
                    }
    ### New Tech end #############
    vals = [[tech, [1]] for tech in new_tech]
    maps = [[has_key, SET_TECH_KEY],
               [add_multiple_values, vals]
               ]
    apply_maps_on_file(in_file, out_file, [maps])


def patch(mod_folder, out_folder):
    patch_USA_tech(mod_folder, out_folder)
