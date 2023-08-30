#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Hoi4Converter.converter import *
from Hoi4Converter.mappings import *
import Hoi4Converter
import os
import sys
import pandas as pd
import shutil
from Hoi4Converter.parser import parse_grammar as code2obj
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")

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
            [add_multiple, [["iconType", [["name", ['"autobahn_logo"']],
                                          ["spriteType", ['"GFX_autobahn_logo"']],
                                          ["position",
                                           [['x', [1700]],
                                            ['y', [1400]],
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


def path_idea_tags(kx_path, out_folder):
    idea_tag_path = os.path.join("common", "idea_tags")
    idea_tag_file = "00_idea.txt"
    in_file, out_file = make_folder_in_out_file(idea_tag_path, idea_tag_file,
                                                kx_path, out_folder)

    obj = paradox2list(in_file)
    _, inds = has_key.search(obj, "research_production")

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

    new_item = obj[0][1][:main_id] + [to_insert] + obj[0][1][main_id:]
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


def patch(kx_path, out_folder):
    patch_main_menu(kx_path, out_folder)
    path_idea_tags(kx_path, out_folder)
    # Is removed in KX for now
    #patch_naval_ai_equipment(kx_path, out_folder)
