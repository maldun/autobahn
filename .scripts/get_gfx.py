# -*- coding: utf-8 -*-
import shutil
import pandas as pd
import sys
import os
import shutil
import rt56_update
import json
from Hoi4Converter.parser import parse_grammar as code2obj
from Hoi4Converter.converter import *
from Hoi4Converter.mappings import *
import Hoi4Converter
from multiprocessing.pool import ThreadPool
HOME = os.path.expanduser("~/")
# sys.path.append(HOME + "prog/Python/hoi4_converter/")

NR_PROCESSES = 16
JSON_SUF = '.json'

HOI4_FOLDER = HOME + ".local/share/Steam/steamapps/common/Hearts of Iron IV/"
KR_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/1521695605/"
KX_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/2076426030/"
# RT56_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/820260968/"
RT56_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/1956_beta/"

# Set for mod in question
KX = True

AUTOBAHN_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn"
AUTOBAHN_KX_FOLDER = HOME + \
    ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_KX"


OUT_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_diff"
MAIN_MOD = KX_FOLDER if KX is True else KR_FOLDER
MOD_FOLDER = AUTOBAHN_KX_FOLDER if KX is True else AUTOBAHN_FOLDER
INTERFACE_PATH = "interface"

NAME = 'name'
TEXTURE = "texturefile"


def get_gfx_info(item):
    info, inds = has_key(item, NAME)
    if len(inds) == 0:
        return None, None
    key = get_object_from_inds(item, inds[0])[1][0]
    info, inds = has_key(item, TEXTURE)
    if len(inds) == 0:
        code = list2paradox([item])
        if TEXTURE in code.lower():
            ind = code.lower().index(TEXTURE)
            new_key = code[ind:ind+len(TEXTURE)]
            info, inds = has_key(item, new_key)
        else:
            pass

    if len(inds) > 0:
        val = get_object_from_inds(item, inds[0])[1][0]
    else:
        val = None

    return key, val


def create_gfx_dict_from_file(root, name):
    fname = os.path.join(root, name)
    dic = {}
    print("Current File: ", name)
    try:
        obj = paradox2list(fname)
    except:
        print("Not parsable, skip!")
        return dic

    # for item in obj[0][1]:
    with ThreadPool(NR_PROCESSES) as p:
        dic = dict(p.map(get_gfx_info, obj[0][1]))
        # dic[key] = val

    return dic


def create_gfx_dict(folder):
    for root, dirs, files in os.walk(folder):
        files_filt = [name for name in files if name.endswith('.gfx')]
        def hlper(name): return create_gfx_dict_from_file(root, name)
        result = map(hlper, files_filt)

        dic = {}
        for r in result:
            dic.update(r)
        return dic


def write_jsons(folder, out_folder):
    for root, dirs, files in os.walk(folder):
        files_filt = [name for name in files if name.endswith('.gfx')]
        def hlper(name): return create_gfx_dict_from_file(root, name)
        for name in files_filt:
            out_name = name[:-len('.gfx')] + '.json'
            if not os.path.exists(os.path.join(out_folder, out_name)):
                dic = hlper(name)
                if None in dic.keys():
                    del dic[None]
                with open(os.path.join(out_folder, out_name), 'w') as fp:
                    try:
                        json.dump(dic, fp)
                    except:
                        import pdb
                        pdb.set_trace()


def compare_gfx(folder1, folder2):
    dict1 = create_gfx_dict(folder1)
    dict2 = create_gfx_dict(folder2)
    diff = {}
    for key, value in dict1.items():
        if key in dict2.keys():
            diff[key] = dict2[key]

    return diff


def create_collection_dict(json_folder):
    main_dic = {}
    for root, dirs, files in os.walk(json_folder):
        for file in files:
            if not file.endswith(JSON_SUF):
                continue
            name = os.path.join(root, file)
            with open(name, 'r') as fp:
                dic = json.load(fp)
                main_dic.update(dic)

    return main_dic


def create_new_gfx_dict(out_folder, main_mod_jsons, r56_jsons):
    main_mod_dic = create_collection_dict(main_mod_jsons)
    r56_dic = create_collection_dict(r56_jsons)

    main_keys = set(main_mod_dic.keys())
    r56_keys = set(r56_dic.keys())
    keys = r56_keys.difference(main_keys)

    copy_dict = {key: r56_dic[key] for key in keys}

    return copy_dict


def copy_gfx(mod_folder, copy_dict, out_folder):
    for key, val in copy_dict.items():
        if val is None:
            continue
        name = val.replace('"', '').replace("'", "")
        fname_org = os.path.join(mod_folder, name)
        fname_out = os.path.join(out_folder, name)
        out_path = os.path.dirname(fname_out)
        os.makedirs(out_path, exist_ok=True)
        try:
            shutil.copy2(fname_org, fname_out)
        except FileNotFoundError:
            org_path = os.path.dirname(fname_org)
            if not os.path.exists(org_path):
                continue
            file_list = os.listdir()
            file_list = [f for f in file_list if fname_org.lower()
                         == f.lower()]
            if len(file_list) == 1:
                fname_cor = os.path.join(out_path, file_list[0])
                shutil.copy2(fname_cor, fname_out)


def check_gfx(keys, item):
    info, inds = has_key(item, NAME)
    if len(inds) == 0:
        return True
    key = get_object_from_inds(item, inds[0])[1][0]
    if key in keys:
        return True

    return False


def create_new_gfx_files(out_folder, main_folder, r56_gfx_files, copy_dict):
    keys = copy_dict.keys()
    for root, dirs, files in os.walk(r56_gfx_files):
        for file in files:
            if not file.endswith('.gfx'):
                continue
            out_root = root.replace(main_folder, out_folder + os.sep)
            os.makedirs(out_root, exist_ok=True)
            filter_gfx_file(out_root, root, file, keys)


def filter_gfx_file(out_root, root, name, keys):
    fname = os.path.join(root, name)
    print("Current File: ", name)
    try:
        obj = paradox2list(fname)
    except:
        print("Not parsable, skip!")
        return

    # for item in obj[0][1]:

    new_items = list(filter(lambda x: check_gfx(keys, x), obj[0][1]))
    if len(new_items) > 0:
        obj[0][1] = list(new_items)
        with open(os.path.join(out_root, name), 'w') as fp:
            content = list2paradox(obj)
            fp.write(content)


if __name__ == "__main__":
    os.makedirs(OUT_FOLDER, exist_ok=True)
    os.makedirs(os.path.join(OUT_FOLDER, INTERFACE_PATH), exist_ok=True)
    json_out_org = os.path.join(OUT_FOLDER,  '.' + INTERFACE_PATH+'_org_items')
    json_out = os.path.join(OUT_FOLDER,  '.' + INTERFACE_PATH+'_items')
    json_out_r56 = os.path.join(OUT_FOLDER,  '.' + INTERFACE_PATH+'r56_items')
    os.makedirs(json_out, exist_ok=True)
    os.makedirs(json_out_org, exist_ok=True)
    os.makedirs(json_out_r56, exist_ok=True)

    key = '"GFX_goal_SLO_slovak_birth"'
    dir = "/home/maldun/.local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_KX/interface/"
    name = "aut56_goals.gfx"
    mod1 = os.path.join(MOD_FOLDER, INTERFACE_PATH)
    mod2 = os.path.join(MAIN_MOD, INTERFACE_PATH)
    mod3 = os.path.join(RT56_FOLDER, INTERFACE_PATH)
    # result = compare_gfx(mod1, mod2)
    write_jsons(mod1, json_out)
    write_jsons(mod2, json_out_org)
    write_jsons(mod3, json_out_r56)
    copy_dict = create_new_gfx_dict(OUT_FOLDER, json_out_org, json_out_r56)
    create_new_gfx_files(OUT_FOLDER, RT56_FOLDER, mod3, copy_dict)
    copy_gfx(RT56_FOLDER, copy_dict, OUT_FOLDER)
