#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rt56_patches
import pyparsing
from Hoi4Converter.parser import parse_grammar as code2obj
from Hoi4Converter.converter import *
from Hoi4Converter.mappings import *
import Hoi4Converter
import os
import sys
import pandas as pd
import json
import shutil
import copy
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")


COMMON_PATH = "common/"
TECHNOLOGY_PATH = "common/technologies"
EQUIPMENT_PATH = "common/units/equipment"
AI_KEY = "ai_will_do"
TECHNOLOGY_KEY = "technologies"
SUB_TECH_KEY = 'sub_technologies'
EMPTY_SEARCH = ([], [])
ALLOW_KEY = "allow"


def replace_string(str1, str2, out_dir):
    for subdir, dirs, files in os.walk(out_dir):
        for file in files:
            fname = os.path.join(out_dir, subdir, file)
            if '~' in fname:
                continue
            try:
                with open(fname, 'r+', encoding='utf-8') as fp:
                    txt = fp.read()
                    fp.seek(0)
                    fp.write(txt.replace(str1, str2))
            except UnicodeDecodeError:
                with open(fname, 'r+', encoding='latin-1') as fp:
                    txt = fp.read()
                    fp.seek(0)
                    fp.write(txt.replace(str1, str2))

###############################################################################
# Copy Files                                                                 #
##############################################################################


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
                import pdb
                pdb.set_trace()
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


###############################################################################
# Update AI settings                                                         #
##############################################################################

def get_obj_and_tech_map(file):
    obj = paradox2list(file)
    # Get techs
    inds = [0, 1]
    techs = get_object_from_inds(obj, inds)
    tech_map = {tech[0]: k for k, tech in enumerate(techs)}
    return obj, tech_map, techs


class CarryOverAISettings:
    def __init__(self, filename, method):
        self.filename = filename
        self._post_steps = method

    def post_steps(self, r56_techs, *args, **kwargs):
        return self._post_steps(self, r56_techs, *args, **kwargs)

    @staticmethod
    def _carry_over_ai_settings(mod_file, r56_file):
        org_obj, org_tech_map, org_techs = get_obj_and_tech_map(mod_file)
        r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(r56_file)
        if mod_file.endswith('infantry.txt'):
            import pdb
            pdb.set_trace()
        # get ai settings from main mod
        for tech_key, ind in org_tech_map.items():

            found, inds = has_key.search(org_techs[ind], AI_KEY)
            mapping = [[has_key, AI_KEY], [replace, [found]]]
            try:
                tech_r56 = r56_techs[r56_tech_map[tech_key]]
                r56_techs[r56_tech_map[tech_key]] = apply_map(tech_r56, mapping)
            except KeyError:
                pass

        return org_obj, org_tech_map, org_techs, r56_obj, r56_tech_map, r56_techs

    def __call__(self, mod_path, out_path, *args, **kwargs):
        self.org_file = os.path.join(mod_path, self.filename)
        self.out_file = os.path.join(out_path, self.filename)

        (self.org_obj, self.org_tech_map, self.org_techs,
         self.r56_obj, self.r56_tech_map, r56_techs) = \
            self._carry_over_ai_settings(self.org_file, self.out_file)

        result = self.post_steps(r56_techs, *args, **kwargs)
        if result is None:
            pass
        else:
            r56_techs = result
        # set_new_object and file
        with open(self.out_file, 'w') as fp:
            new_obj = [[TECHNOLOGY_KEY, r56_techs]]
            fp.write(list2paradox(new_obj))
        return


def carry_over_ai_settings(filename):
    def carry_over_dec(method):
        carry_obj = CarryOverAISettings(filename, method)
        return carry_obj
    return carry_over_dec


def patch_nonMTG_navy(mod_path, r56_path, out_path):
    navy_file = os.path.join(TECHNOLOGY_PATH, "naval.txt")
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

    @carry_over_ai_settings(navy_file)
    def navy_post(self, r56_techs):
        for tech_key, ind in self.org_tech_map.items():
            if tech_key.startswith(adv):
                found, inds = has_key.search(self.org_techs[ind], AI_KEY)
                mapping = [[has_key, AI_KEY], [replace, [found]]]
                sm_tech_key = esm + tech_key[len(adv):]
                sm_tech = r56_techs[self.r56_tech_map[sm_tech_key]]
                r56_techs[self.r56_tech_map[sm_tech_key]
                          ] = apply_map(sm_tech, mapping)
        return r56_techs
    navy_post(mod_path, out_path)


@carry_over_ai_settings(os.path.join(TECHNOLOGY_PATH, "artillery.txt"))
def patch_artillery(self, r56_techs):
    mapping = [[has_key_and_val, ["has_war_with", ["USA"]]],
               [replace, ["has_war_with", ["GER"]]]]
    r56_techs = apply_map(r56_techs, mapping)
    return r56_techs


def patch_object(r56_obj, org_code, patched_code):
    key_val = code2obj(org_code)[0]
    if isinstance(patched_code, str) and len(patched_code) > 0:
        key_val_replace = code2obj(patched_code)[0]
        mapping = [[has_key_and_val, key_val], [replace, key_val_replace]]
    else:
        mapping = [[has_key_and_val, key_val], [remove, key_val]]

    r56_obj = apply_map(r56_obj, mapping)
    return r56_obj


def patch_tech_code(out_file, org_code, patched_code):
    r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(out_file)
    r56_obj = patch_object(r56_obj, org_code, patched_code)
    with open(out_file, 'w') as fp:
        fp.write(list2paradox(r56_obj))


def patch_rt56_vehicles(mod_path, out_path):
    vehicle_file = os.path.join(TECHNOLOGY_PATH, "r56_vechicles.txt")
    out_file = os.path.join(out_path, vehicle_file)
    snippet = rt56_patches.vehicle_snippet1
    patch_tech_code(out_file, snippet, snippet.replace('1939', '1940'))
    snippet2 = rt56_patches.vehicle_snippet2
    patch_tech_code(out_file, snippet2, snippet2.replace('1940', '1939'))
    snippet3 = rt56_patches.vehicle_snippet3
    patch3 = rt56_patches.vehicle_patch3
    patch_tech_code(out_file, snippet3, patch3)
    snippet4 = rt56_patches.vehicle_snippet4
    patch_tech_code(out_file, snippet4, snippet4.replace('USA', 'CSA'))
    snippet5 = rt56_patches.vehicle_snippet5
    patch5 = rt56_patches.vehicle_patch5
    patch_tech_code(out_file, snippet5, patch5)
    patch_tech_code(out_file, snippet5.replace("2", "5"), patch5)


def multi_patch(obj, snippets, patches):
    for snippet, patch in zip(snippets, patches):
        obj = patch_object(obj, snippet, patch)
    return obj


def patch_mtg_navy(out_path):
    navy_file = os.path.join(TECHNOLOGY_PATH, "MTG_naval.txt")
    out_file = os.path.join(out_path, navy_file)
    r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(out_file)
    snippets = rt56_patches.mtg_naval_snippets
    patches = rt56_patches.mtg_naval_patches
    r56_techs = multi_patch(r56_techs, snippets, patches)
    with open(out_file, 'w') as fp:
        new_obj = [[TECHNOLOGY_KEY, r56_techs]]
        fp.write(list2paradox(new_obj))
    return


def patch_mtg_support(out_path):
    navy_file = os.path.join(TECHNOLOGY_PATH, "MTG_naval_Support.txt")
    out_file = os.path.join(out_path, navy_file)
    r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(out_file)
    snippets = rt56_patches.mtg_support_snippets
    patches = rt56_patches.mtg_support_patches
    r56_techs = multi_patch(r56_techs, snippets, patches)
    with open(out_file, 'w') as fp:
        new_obj = [[TECHNOLOGY_KEY, r56_techs]]
        fp.write(list2paradox(new_obj))
    return


@carry_over_ai_settings(os.path.join(TECHNOLOGY_PATH, "air_techs.txt"))
def patch_air(self, r56_techs):
    snippets = rt56_patches.air_snippets
    patches = rt56_patches.air_patches
    r56_techs = multi_patch(r56_techs, snippets, patches)
    return r56_techs


@carry_over_ai_settings(os.path.join(TECHNOLOGY_PATH, "armor.txt"))
def patch_armor(self, r56_techs):
    snippets = rt56_patches.tank_snippets
    patches = rt56_patches.tank_patches
    r56_techs = multi_patch(r56_techs, snippets, patches)
    return r56_techs


@carry_over_ai_settings(os.path.join(TECHNOLOGY_PATH, "bba_air_techs.txt"))
def patch_bba_air(self, r56_techs):
    pass


def patch_infantry(mod_path, r56_path, out_path, KX):
    infantry_file = os.path.join(TECHNOLOGY_PATH, "infantry.txt")
    r56_file = os.path.join(r56_path, infantry_file)
    out_file = os.path.join(out_path, infantry_file)
    # make temp file and replace descriptors
    with open(out_file, 'r') as r56_fp:
        r56_text = r56_fp.read()
        r56_text = r56_text.replace('1930', '1918')
    with open(out_file, 'w') as tmp_fp:
        tmp_fp.write(r56_text)

    r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(out_file)
    snippets = rt56_patches.infantry_snippets
    patches = rt56_patches.infantry_patches
    # change KX tags
    if KX is True:
        patches = [patch.replace("HND", "BHC") for patch in patches]
        patches = [patch.replace("LIB", "LBA") for patch in patches]
    r56_techs = multi_patch(r56_techs, snippets, patches)
    with open(out_file, 'w') as fp:
        new_obj = [[TECHNOLOGY_KEY, r56_techs]]
        fp.write(list2paradox(new_obj))
    return


def patch_electrical_engineering(mod_path, out_path):
    fname = "electronic_mechanical_engineering.txt"
    out_file = os.path.join(out_path, TECHNOLOGY_PATH, fname)
    with open(out_file, 'r') as fp:
        txt = fp.read()
        # Germany is brain now
        txt = txt.replace("USA", "GER")
    with open(out_file, 'w') as fp:
        fp.write(txt)


def patch_industry(mod_path, out_path):
    industry_file = os.path.join(TECHNOLOGY_PATH, "industry.txt")
    out_file = os.path.join(out_path, industry_file)

    r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(out_file)
    snippets = rt56_patches.industry_snippets
    patches = rt56_patches.industry_patches
    r56_techs = multi_patch(r56_techs, snippets, patches)

    with open(out_file, 'w') as fp:
        new_obj = [[TECHNOLOGY_KEY, r56_techs]]
        fp.write(list2paradox(new_obj))
    return


def patch_ai(mod_path, r56_path, kr_path, out_path, KX):
    patch_air(mod_path, out_path)
    patch_artillery(mod_path, out_path)
    patch_armor(mod_path, out_path)
    patch_electrical_engineering(mod_path, out_path)
    patch_infantry(mod_path, r56_path, out_path, KX)
    patch_industry(mod_path, out_path)
    patch_rt56_vehicles(mod_path, out_path)

    # Use KR tech for these
    patch_bba_air(kr_path, out_path)
    patch_nonMTG_navy(kr_path, r56_path, out_path)

    # Custom AI settings
    patch_mtg_navy(out_path)
    patch_mtg_support(out_path)

    # No operations necessary:
    # NSB armor
    # infantry extra tech
    # r56_techs
    # r56e_etax.txt

###############################################################################
# Patches for Bugfixes                                                        #
###############################################################################


def patch_code(out_file, org_code, patched_code):
    try:
        r56_obj = paradox2list(out_file)
        r56_obj = patch_object(r56_obj, org_code, patched_code)
        with open(out_file, 'w') as fp:
            fp.write(list2paradox(r56_obj))
    except pyparsing.exceptions.ParseException as excp:
        if "found end of text" in str(excp):
            print(f"Warning File {out_file} empty!")
        else:
            raise excp


def patch_missing_BUL_idea(out_path):
    snippet = rt56_patches.BUL_army_restrictions_snippet
    patch = rt56_patches.BUL_army_restrictions_patch
    for root, _, files in os.walk(os.path.join(out_path, EQUIPMENT_PATH)):
        for file in files:
            current_file = os.path.join(root, file)
            with open(current_file, 'r') as fp:
                txt = fp.read()
            if "BUL_army_restrictions" in txt:
                patch_code(current_file, snippet, patch)


def patch_missing_mtg_naval_subtechs(mod_path, out_path):
    navy_file = os.path.join(TECHNOLOGY_PATH, "MTG_naval.txt")
    mod_file = os.path.join(mod_path, navy_file)
    out_file = os.path.join(out_path, navy_file)
    mod_obj, mod_tech_map, mod_techs = get_obj_and_tech_map(mod_file)
    r56_obj, r56_tech_map, r56_techs = get_obj_and_tech_map(out_file)

    # remove old subtechs:
    for tech, index in r56_tech_map.items():
        tech_obj = r56_techs[index]
        found = has_key.search(tech_obj, SUB_TECH_KEY)
        if found != EMPTY_SEARCH:
            sub_index = found[1][0][1]
            del r56_obj[0][1][index][1][sub_index]

    has_sub_techs = {}
    for tech, index in mod_tech_map.items():
        tech_obj = mod_techs[index]
        found = has_key.search(tech_obj, SUB_TECH_KEY)
        if found != EMPTY_SEARCH:
            has_sub_techs[tech] = found[0][0][1][0][0]
            r56_index = r56_tech_map[tech]
            r56_tech = r56_techs[r56_index]
            # add subtech
            r56_tech[1] += found[0]
            # just to be sure ...
            r56_obj[0][1][r56_index] = r56_tech
            # activate sub-tech
            subtech = has_sub_techs[tech]
            sub_index = r56_tech_map[subtech]
            r56_sub_tech = r56_obj[0][1][sub_index]
            obj_to_remove = code2obj("allow = { always = no }")[0]
            r56_sub_tech = apply_map(
                r56_sub_tech, [[has_key_and_val, obj_to_remove], [remove, obj_to_remove]])
            r56_obj[0][1][sub_index] = r56_sub_tech

    with open(out_file, 'w') as fp:
        fp.write(list2paradox(r56_obj))

def patch_script_enum(mod_path, r56_path, out_path):
    fname = "script_enums.txt"
    r56_file = os.path.join(r56_path,COMMON_PATH,fname)
    mod_file = os.path.join(mod_path,COMMON_PATH,fname)
    out_file = os.path.join(out_path,COMMON_PATH,fname)
    mod_objs = paradox2list(mod_file)
    r56_objs = paradox2list(r56_file)
    for i, obj in enumerate(mod_objs):
        key = obj[0]
        for j, r56_obj in enumerate(r56_objs):
            key2 = r56_obj[0]
            if key == key2:
                for item in r56_obj[1]:
                    if not item in obj[1]:
                        obj[1].append(item)
                        
        mod_objs[i] = obj
    code = list2paradox(mod_objs)
    with open(out_file,'w') as fp:
        fp.write(code)
    

def patch_bugs(mod_path, r56_path, kr_path, out_path, KX):
    patch_missing_BUL_idea(out_path)
    patch_missing_mtg_naval_subtechs(mod_path, out_path)
    patch_script_enum(mod_path, r56_path, out_path)
