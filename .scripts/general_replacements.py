# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd 
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")
import Hoi4Converter
from Hoi4Converter.mappings import *
from Hoi4Converter.converter import *

HOI4_FOLDER = HOME + ".local/share/Steam/steamapps/common/Hearts of Iron IV/"
KR_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/1521695605/"
KX_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/2076426030/"
RT56_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/820260968/"

# Set for mod in question
KX = True

OUT_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_diff"
MAIN_MOD = KX_FOLDER if KX is True else KR_FOLDER

IDEA_PATH = "common/ideas"
HISTORY_COUNTRY_PATH = "history/countries"
# RULES_PATH = 

ideologies = {"fascism": ("national_populist", "paternal_autocrat"),
                  "democratic": ("social_democrat", "social_liberal",
                                 "market_liberal", "social_conservative"),
                  "communism": ("radical_socialist", "syndicalist", "totalist"),
                  "neutrality": ("authoritarian_democrat",)
                  }

rt56_techs = {
    "etax_doctrine",   # special research division
    "camo",            # Camouflagetech
    "sniper_rifle",    # Sniper Rifle
    "transport_plane1",
    "steel_production_1",
    "aluminum_production_1",
    "shocktroops",
    "jaegers",
    "desertinfantry_at",
    "jngdst_clothes_gw", # jungle clothing
    "winter_clothes_gw", 
    }


def ideology_map():
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
    trait_list = ["communist_revolutionary", "democratic_reformer", "fascist_demagogue", "womens_figurehead"]
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

    # Add RadSoc when anarchist Commune is there
    val = ['has_country_leader', [['name', ['"Anarchist Commune"']], ['ruling_only', [True]]]]
    mapping = [[has_value, val],
               [add_multiple, [["has_government",["radical_socialist"]]]]
               ]
    maps.append(mapping)
    if KX is False:
        mapping = [[has_value, val],
               [remove, val]
               ]
        maps.append(mapping)

    # Remove ideas
    ideas = ["nationalism", "internationalism","SPR_collectivized_society"]
    ideas_items = [["has_idea", [idea]] for idea in ideas]
    for item in ideas_items:
        maps.append([[has_key_and_val, item],[remove,item]])
    
    return maps

def apply_ideology_map(maps):
    file_list = os.listdir(RT56_FOLDER + IDEA_PATH)
    file_list = [fname for fname in file_list if fname.startswith("r56i_laws_")]
    
    for file in file_list:
        os.makedirs(os.path.join(OUT_FOLDER, IDEA_PATH), exist_ok=True)

        apply_maps_on_file(os.path.join(RT56_FOLDER, IDEA_PATH, file),
                           os.path.join(OUT_FOLDER, IDEA_PATH, file),
                           maps)

def remove_obsolete_equipment_maps():
    maps = []
    key_and_val = ["cv_naval_bomber1", [1]]
    maps.append([[has_key_and_val, key_and_val],
                 [remove, key_and_val]])

    return maps

def create_equipment_table():
    country_folder56 = os.path.join(RT56_FOLDER, HISTORY_COUNTRY_PATH)
    country_folder = os.path.join(MAIN_MOD, HISTORY_COUNTRY_PATH)
    countries = [fname[:3] for fname in os.listdir(country_folder)]
    
    
    
def apply_equipment_maps(maps):
    in_folder = os.path.join(MAIN_MOD, HISTORY_COUNTRY_PATH)
    out_folder = os.path.join(OUT_FOLDER, HISTORY_COUNTRY_PATH) 
    file_list = os.listdir(in_folder)
    #file_list = ["FRA - France.txt"]
    os.makedirs(out_folder,exist_ok=True)

    for file in file_list:
        try:
            #import pdb; pdb.set_trace()

            apply_maps_on_file(os.path.join(in_folder, file),
                           os.path.join(out_folder, file),
                           maps)
        except:
            import pdb; pdb.set_trace()
    
    
if __name__ == "__main__":
    os.makedirs(OUT_FOLDER, exist_ok=True)
    maps = ideology_map()
    apply_ideology_map(maps)
    maps = remove_obsolete_equipment_maps()
    apply_equipment_maps(maps)
