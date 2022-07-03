# -*- coding: utf-8 -*-
import os
import sys
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")
import Hoi4Converter
from Hoi4Converter.mappings import *
from Hoi4Converter.converter import *

HOI4_FOLDER = HOME + ".local/share/Steam/steamapps/common/Hearts of Iron IV/"
KR_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/1521695605/"
KX_FOLDER = ".local/share/Steam/steamapps/workshop/content/394360/2076426030/"
RT56_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/820260968/"

KX = True
OUT_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_diff"
MAIN_MOD = KX_FOLDER if KX is True else KR_FOLDER

IDEA_PATH = "common/ideas"

ideologies = {"fascism": ("national_populist", "paternal_autocrat"),
                  "democratic": ("social_democrat", "social_liberal",
                                 "market_liberal", "social_conservative"),
                  "communism": ("radical_socialist", "syndicalist", "totalist"),
                  "neutrality": ("authoritarian_democrat",)
                  }

def ideology_map():
    file_list = os.listdir(RT56_FOLDER + IDEA_PATH)
    file_list = [fname for fname in file_list if fname.startswith("r56i_laws_")]

    maps = []
    # update fascist
    key = "has_government"
   
    ideology_objs = {(key, (ikey,)): [[key, [ival]] for ival in ivals]
                     for ikey, ivals in ideologies.items()}

    for ikey, ivals in ideology_objs.items():
        # turn into list
        ikey = list(ikey)
        ikey[1] = list(ikey[1])
        maps.append([[has_key_and_val, ikey], [add_multiple, ivals]])
        maps.append([[has_key_and_val, ikey], [remove, ikey]])

    # remove traits which are obsolete
    trait_list = ["communist_revolutionary", "democratic_reformer", "fascist_demagogue" ]
    traits = [["has_idea_with_trait" , [trait]] for trait in trait_list]
    for ikey in traits:
        maps.append([[has_key_and_val, ikey], [remove, ikey]])

    # remove political relations
    for ikey in ideologies.keys():
        mapping = [[is_relation_with_key, ikey], [remove, ikey]]
        maps.append(mapping)

    # change country tags
    key = "original_tag"
    vals = ["SHX", "PER"]
    for val in vals:
        maps.append([[has_key_and_val, [key, [val]]], [remove, [key, [val]]]])
    val = "TUR"
    val2 = "OTT"
    maps.append([[has_key_and_val, [key, [val]]], [add_multiple, [[key, [val2]]]]])
    
    for file in file_list:
        os.makedirs(os.path.join(OUT_FOLDER, IDEA_PATH), exist_ok=True)

        apply_maps_on_file(os.path.join(RT56_FOLDER, IDEA_PATH, file),
                           os.path.join(OUT_FOLDER, IDEA_PATH, file),
                           maps)

    
    
if __name__ == "__main__":
    os.makedirs(OUT_FOLDER, exist_ok=True)
    ideology_map()
