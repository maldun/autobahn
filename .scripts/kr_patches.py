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
from Hoi4Converter.parser import parse_grammar as code2obj

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

def path_idea_tags(kx_path, out_folder):
    idea_tag_path = os.path.join("common", "idea_tags")
    idea_tag_file = "00_idea.txt"
    in_file, out_file = make_folder_in_out_file(idea_tag_path, idea_tag_file,
                                                kx_path, out_folder)

    obj = paradox2list(in_file)
    _, inds = has_key.search(obj, "military_staff")

    inds = inds[0]
    main_id = inds[-1]
    code = """
    	etgi_ideas = {
		slot = r56i_laws_category_security
		slot = r56i_laws_leadership
		slot = r56i_laws_category_gender
		slot = r56i_laws_social
		slot = r56i_laws_war

		ledger = civilian
		
		cost = 150
		removal_cost = 0
	}	
    """
    to_insert = code2obj(code)

    new_item = obj[0][1][:main_id+1] + to_insert + obj[0][1][main_id+1:]
    obj[0][1] = new_item

    #item, inds = has_key.search(obj, "slot_ledgers")
    #_, inds2 = has_key.search(obj, "theorist")
    #main_ind = inds2[0][-1]
    # new_item = obj[1][1][:main_ind] + \
    #    [["high_command", ['invalid']]] + obj[1][1][main_ind:]
    #obj[1][1] = new_item

    new_code = list2paradox(obj)
    with open(out_file, 'w') as fp:
        fp.write(new_code)



def patch(mod_folder, out_folder):
    patch_USA_tech(mod_folder, out_folder)
    path_idea_tags(mod_folder, out_folder)
