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
COMMON_FOLDER = "common"

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
    ai_equipment_folder = os.path.join(COMMON_FOLDER, "ai_equipment")
    naval_path = "generic_naval.txt"
    in_file, out_file = make_folder_in_out_file(ai_equipment_folder, naval_path,
                                                kx_path, out_folder)

    tmap1 = [[has_key_and_val, ["has_tech", ["dp_secondary_battery"]]],
             [add_multiple, [["has_tech", ["basic_dp_medium_battery"]]]]]
    tmap2 = [[has_key_and_val, ["has_tech", ["dp_secondary_battery"]]],
             [remove, ["has_tech", ["dp_secondary_battery"]]]]

    apply_maps_on_file(in_file, out_file, [tmap1, tmap2])


def path_idea_tags(kx_path, out_folder):
    idea_tag_path = os.path.join(COMMON_FOLDER, "idea_tags")
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
    equipment_path = os.path.join(COMMON_FOLDER, "units", "equipment")
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

def patch_airships_techtree(kx_path, rt56_folder, out_folder):
    interface_path = INTERFACE_FOLDER
    snippet = """
    gridboxtype = {
				name = "airships1_tree"
				position = { x = 1075 y = 32 }
				size = { width = 200 height = 1000 }
				slotsize = { width = 70 height = 70 }
				format = "UP"
			}
    """
    obj = code2obj(snippet)
    fname = "countrytechtreeview.gui"
    in_file, out_file = make_folder_in_out_file(interface_path, fname, rt56_folder, out_folder)
    with open(in_file,'r') as f:
        text = f.read()
    text = text.replace("%%","%")
    for k in range(10):
        text = text.replace(str(k) + "K",str(k))
    techtree = code2obj(text)
    _, inds = has_key_and_val.search(techtree,["name",['"early_fighter_tree"']])
    inds = inds[0]
    liste = techtree[inds[0]][inds[1]][inds[2]][inds[3]][inds[4]][inds[5]]
    liste = liste[:inds[6]+1] + obj + liste[inds[6]+1:]
    techtree[inds[0]][inds[1]][inds[2]][inds[3]][inds[4]][inds[5]] = liste
    new_code = list2paradox(techtree)
    with open(out_file, 'w') as fp:
        fp.write(new_code)
    

def patch_combat_tactics(kx_path, rt56_path, out_folder):
    """
    Merges combat tactics
    """
    fname = os.path.join(COMMON_FOLDER,"combat_tactics.txt")
    rt56_fname = os.path.join(rt56_path,fname)
    kx_fname = os.path.join(kx_path,fname)
    out_fname = os.path.join(out_folder,fname)
    
    with open(rt56_fname,'r') as fp: rt56_code = fp.read()
    with open(kx_fname,'r') as fp: kx_code = fp.read()
    rt56_tactics = code2obj(rt56_code)
    kx_tactics = code2obj(kx_code)
    

    
    tactic_names_rt56 = [tactic[0] for tactic in rt56_tactics]
    tactic_names_kx = [tactic[0] for tactic in kx_tactics]
    uniqe_kx_tactic_names = set(tactic_names_kx) - set(tactic_names_rt56)
    unique_kx_tactics = [tactic for tactic in kx_tactics if tactic[0] in uniqe_kx_tactic_names]
    
    # kx specific settings
    # add countertactic
    overwrites = {'tactic_banzai_charge':None,'tactic_basic_attack':None}
    BASIC_NAME = 'tactic_basic_attack'
    BANZAI_NAME = "tactic_banzai_charge"
    for tactic in kx_tactics:
        tname = tactic[0]
        if  tname in overwrites:
            overwrites[tname] = tactic
    for ind, tactic in enumerate(rt56_tactics):
        tname = tactic[0]
        if  tname in overwrites:
            rt56_tactics[ind] = overwrites[tname]
            
    all_tactics = rt56_tactics + unique_kx_tactics
    new_code = list2paradox(all_tactics)
    with open(out_fname, 'w') as fp:
        fp.write(new_code)
    

def patch_countrystateview(kx_path, out_folder):
    """
    Normally copy is enough 
    """
    fname = os.path.join(INTERFACE_FOLDER,"countrystateview.gui")
    shutil.copy2(os.path.join(kx_path,fname),os.path.join(out_folder,fname))
    

def patch(kx_path, rt56_path, out_folder):
    patch_main_menu(kx_path, out_folder)
    path_idea_tags(kx_path, out_folder)
    patch_infantry_equipment(kx_path, rt56_path, out_folder)
    #patch_airships_techtree(kx_path,rt56_path,out_folder)
    # Is removed in KX for now
    #patch_naval_ai_equipment(kx_path, out_folder)
    patch_countrystateview(kx_path, out_folder)
    patch_combat_tactics(kx_path, rt56_path, out_folder)
