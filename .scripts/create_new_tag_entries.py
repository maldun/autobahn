# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import shutil
import copy

HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")

import Hoi4Converter
from Hoi4Converter.converter import *
from Hoi4Converter.mappings import *

ORG_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn"
OUT_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_diff"


INTERFACE_PATH = "interface"
GFX_SUFF = '.gfx'
NAME_KEY = "name"
GFX_PREFIX = "GFX_"
full_interface_path = os.path.join(ORG_FOLDER, INTERFACE_PATH)
out_interface_path = os.path.join(OUT_FOLDER, INTERFACE_PATH)


def duplicate_tags(fname, tag1, tag2):
    with open(fname, 'r') as fp:
        content = fp.read()
        if not (GFX_PREFIX + tag1 in content):
            return 
    
    try:
        obj = paradox2list(fname)
    except:
        raise Exception("Error: could not parse {}".format(fname))
    new_sprites = []
    sprite_types = obj[0][1]
    for num, stype in enumerate(sprite_types):
       for num2, sub_obj in enumerate(stype[1]):
           if sub_obj[0] == NAME_KEY:
               cname = sub_obj[1][0]
               if GFX_PREFIX + tag1 in cname:
                   ntype = copy.deepcopy(stype)
                   ntype[1][num2][1][0] = cname.replace(tag1, tag2)
                   new_sprites.append(ntype)
    obj[0][1] += new_sprites
    content = list2paradox(obj)
    return content


def duplicate_gfx_files(tag1, tag2, suffix, in_path, out_path):
    for root, _, files in os.walk(in_path):
        for file in files:
            if file.endswith(suffix):
                fname = os.path.join(root,file)
                content = duplicate_tags(fname, tag1, tag2)
                out_fname = os.path.join(root.replace(in_path, out_path),
                                         file)
                if content is not None:
                    with open(out_fname, 'w') as fp:
                        fp.write(content)

if __name__ == "__main__":
    duplicate_gfx_files("CAN", "IMP", GFX_SUFF,
                        full_interface_path, out_interface_path)
