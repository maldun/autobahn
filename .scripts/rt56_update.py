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

TECHNOLOGY_PATH = "common/technologies"
AI_KEY = "ai_will_do"
TECHNOLOGY_KEY = "technologies"

def replace_string(str1, str2, out_dir):
    for subdir, dirs, files in os.walk(out_dir):
        for file in files:
            fname = os.path.join(out_dir, subdir, file)
            if '~' in fname:
                continue
            with open(fname, 'r+', encoding='utf-8') as fp:
                txt = fp.read()
                fp.seek(0)
                fp.write(txt.replace(str1, str2))


def patch_nonMTG_navy(mod_path, r56_path, out_path):
    navy_file = os.path.join(TECHNOLOGY_PATH, "naval.txt")
    org_file = os.path.join(mod_path, navy_file)
    r56_file = os.path.join(r56_path, navy_file)
    out_file = os.path.join(out_path, navy_file)
    # make temp file and replace descriptors
    sm = "semi_modern_"
    esm = "etat_semi_modern_"
    adv = "advanced_"
    with open(r56_file, 'r') as r56_fp:
        r56_text = r56_fp.read()
        r56_text = r56_text.replace(sm, esm)
        with open(out_file, 'w') as tmp_fp:
            tmp_fp.write(r56_text)
    
    def get_obj_and_tech_map(file):
        obj = paradox2list(file)
        # Get techs
        inds = [0,1]
        techs = get_object_from_inds(obj, inds)
        tech_map = {tech[0]: k for k, tech in enumerate(techs)}
        return obj, tech_map, techs
    
    org_obj, org_tech_map, org_techs = get_obj_and_tech_map(org_file)
    r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(out_file)

    # get ai settings from main mod
    for tech_key, ind in org_tech_map.items():
        found, inds = has_key.search(org_techs[ind], AI_KEY)
        mapping = [[has_key, AI_KEY], [replace, [found]]]
        tech_r56 = r56_techs[r56_tech_map[tech_key]]
        
        r56_techs[r56_tech_map[tech_key]] = apply_map(tech_r56, mapping)
        if tech_key.startswith(adv):
            sm_tech_key = esm + tech_key[len(adv):]
            sm_tech = r56_techs[r56_tech_map[sm_tech_key]]
            r56_techs[r56_tech_map[sm_tech_key]] = apply_map(sm_tech, mapping)
        
    # set_new_object and file
    with open(out_file, 'w') as fp:
        new_obj = [[TECHNOLOGY_KEY,r56_techs]]
        fp.write(list2paradox(new_obj))

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

            
def copy_files(fname):
    def cdecorator(func):
        def new_func(rt56_path, out_path, *args, **kwargs):
            copy_json(fname, rt56_path, out_path)
            return func(rt56_path, out_path, *args, **kwargs)
        return new_func
    return cdecorator


@copy_files("rt56_copy_infantry.json")
def update_infantry(rt56_path, out_path):
    pass

@copy_files("rt56_copy_air.json")
def update_air(rt56_path, out_path):
    pass


@copy_files("rt56_copy_tank.json")
def update_tanks(rt56_path, out_path):
    pass


@copy_files('rt56_copy_navy.json')
def update_navy(rt56_path, out_path):
    pass


@copy_files('rt56_copy_civ.json')
def update_civ(rt56_path, out_path):
    pass


@copy_files("rt56_copy_post.json")
def update_post_steps(rt56_path, out_path):
    pass


def copy_update(rt56_path, out_path):
    update_infantry(rt56_path, out_path)
    update_air(rt56_path, out_path)
    update_tanks(rt56_path, out_path)
    update_navy(rt56_path, out_path)
    update_civ(rt56_path, out_path)
    update_post_steps(rt56_path, out_path)
