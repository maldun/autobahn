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
                                           [['x', [1425]],
                                            ['y', [1000]],
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


def patch_infantry_equipment(kx_path, rt56_folder, out_folder):
    equipment_path = os.path.join("common", "units", "equipment")
    infant_file = "infantry.txt"
    in_file, out_file = make_folder_in_out_file(equipment_path, infant_file,
                                                kx_path, out_folder)

    rt56_file = os.path.join(rt56_folder, equipment_path, infant_file)
    rt56_obj = paradox2list(rt56_file)
    kx_obj = paradox2list(in_file)

    rt56_keys = [rt56_obj[0][1][k][0] for k in range(len(rt56_obj[0][1]))]
    kx_keys = [kx_obj[0][1][k][0] for k in range(len(kx_obj[0][1]))]
    new_keys = set(kx_keys).difference(rt56_keys)

    new_items = [ob for ob in kx_obj[0][1] if ob[0] in new_keys]
    rt56_obj[0][1] += new_items

    new_convertables = [["mau_mau_equipment_0"], ["reservation_equipment_0"], ["simba_spears_0"],
                        ["aztec_club_0"], ["jezail_equipment_0"]]

    for ob in rt56_obj[0][1]:
        for sub in ob[1]:
            if sub[0] == 'can_convert_from':
                sub[1] += new_convertables

    new_code = list2paradox(rt56_obj)
    with open(out_file, 'w') as fp:
        fp.write(new_code)


def patch(kx_path, rt56_path, out_folder):
    patch_main_menu(kx_path, out_folder)
    path_idea_tags(kx_path, out_folder)
    patch_infantry_equipment(kx_path, rt56_path, out_folder)
    # Is removed in KX for now
    #patch_naval_ai_equipment(kx_path, out_folder)
