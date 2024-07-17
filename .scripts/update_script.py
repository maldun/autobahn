# -*- coding: utf-8 -*-
import rt56_update
from Hoi4Converter.converter import *
from Hoi4Converter.mappings import *
import Hoi4Converter
import os
import sys
import pandas as pd
import shutil
HOME = os.path.expanduser("~/")
sys.path.append(HOME + "prog/Python/hoi4_converter/")


HOI4_FOLDER = HOME + "SSD/SteamLibrary/steamapps/common/Hearts of Iron IV/"
KR_FOLDER = HOME + "SSD/SteamLibrary/steamapps/workshop/content/394360/1521695605/"
KX_FOLDER = HOME + "SSD/SteamLibrary/steamapps/workshop/content/394360/2076426030/"
#RT56_FOLDER = HOME + ".local/share/Steam/steamapps/workshop/content/394360/820260968/"
RT56_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/1956_beta/"

# Set for mod in question

KX = False

OUT_FOLDER = HOME + ".local/share/Paradox Interactive/Hearts of Iron IV/mod/autobahn_diff"
MAIN_MOD = KX_FOLDER if KX is True else KR_FOLDER

IDEA_PATH = "common/ideas"
INTERFACE_PATH = "interface"
SCRIPTED_EFFECTS_PATH = "common/scripted_effects"
HISTORY_COUNTRY_PATH = "history/countries"
DECISION_PATH = "common/decisions"
# RULES_PATH =
SET_TECH_KEY = "set_technology"
HAS_TECH_KEY = "has_tech"
SPIRIT_KEYS = {"air_spirits.txt": ("air_force_spirit",
                                   "air_force_command_spirit"),
               "army_spirits.txt": ("academy_spirit", "army_spirit",
                                    "division_command_spirit"),
               "navy_spirits.txt": ("naval_academy_spirit",
                                    "navy_spirit",
                                    "naval_command_spirit"),
               }

ideologies = {"fascism": ("national_populist", "paternal_autocrat"),
              "democratic": ("social_democrat", "social_liberal",
                             "market_liberal", "social_conservative"),
              "communism": ("radical_socialist", "syndicalist", "totalist"),
              "neutrality": ("authoritarian_democrat",)
              }

TECH_CRITS = {"air_spirits.txt": ['available',
                                  [['OR', [['has_tech', ['air_superiority']],
                                           ['has_tech', ['formation_flying']],
                                           ['has_tech', ['force_rotation']]]]]],
              "army_spirits.txt": ['available',
                                   [['OR', [['has_tech', ['mobile_warfare']],
                                            ['has_tech', ['superior_firepower']],
                                            ['has_tech', ['trench_warfare']],
                                            ['has_tech', ['mass_assault']],
                                            ['has_tech', ['r56_guerilla_warfare']]]]]],
              "navy_spirits.txt": ['available',
                                   [['OR', [['has_tech', ['fleet_in_being']],
                                            ['has_tech', ['trade_interdiction']],
                                            ['has_tech', ['base_strike']]]]]]
              }

KR_SPIRIT_MAP = {"air_spirits.txt": "01 Air Spirits.txt",
                 "army_spirits.txt": "01 Army Spirits.txt", "navy_spirits.txt": "01 Navy Spirits.txt"}
KR_REV_SPIRIT_MAP = {val: key for key, val in KR_SPIRIT_MAP.items()}
KR_TECH_CRITS = {}
KR_SPIRIT_KEYS = {}
for kx_file, kr_file in KR_SPIRIT_MAP.items():
    KR_SPIRIT_KEYS[kr_file] = SPIRIT_KEYS[kx_file]
    KR_TECH_CRITS[kr_file] = TECH_CRITS[kx_file]

KX_SPIRIT_FILTER = {"ideological_loyalty_spirit_KR"}
KR_SPIRIT_FILTER = {}
SPIRIT_FILTER = KX_SPIRIT_FILTER if KX is True else KR_SPIRIT_FILTER

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
    "jngdst_clothes_gw",  # jungle clothing
    "winter_clothes_gw",
    "r56_gw_railway_gun",
    "r56_railway_mortar_subtech",
    "r56_militia_tech",
    "r56_guerilla_warfare",  # Docrtine
    "jungletroops",
}

country_inheritance = {"TUR": ("OTT",),
                       "USA": ("CSA",),
                       "SOV": ("RUS",),
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
    trait_list = ["communist_revolutionary", "democratic_reformer",
                  "fascist_demagogue", "womens_figurehead"]
    traits = [["has_idea_with_trait", [trait]] for trait in trait_list]
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
    #val = "TUR"
    #val2 = "OTT"
    #maps.append([[has_key_and_val, [key, [val]]], [add_multiple, [[key, [val2]]]]])

    # Add RadSoc when anarchist Commune is there
    val = ['has_country_leader', [
        ['name', ['"Anarchist Commune"']], ['ruling_only', [True]]]]
    mapping = [[has_value, val],
               [add_multiple, [["has_government", ["radical_socialist"]]]]
               ]
    maps.append(mapping)
    if KX is False:
        mapping = [[has_value, val],
                   [remove, val]
                   ]
        maps.append(mapping)

    # Remove ideas
    ideas = ["nationalism", "internationalism", "SPR_collectivized_society"]
    ideas_items = [["has_idea", [idea]] for idea in ideas]
    for item in ideas_items:
        maps.append([[has_key_and_val, item], [remove, item]])

    return maps


def apply_ideology_map(maps):
    file_list = os.listdir(RT56_FOLDER + IDEA_PATH)
    file_list = [
        fname for fname in file_list if fname.startswith("r56i_laws_")]

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


def create_equipment_table(out_file):
    country_folder56 = os.path.join(RT56_FOLDER, HISTORY_COUNTRY_PATH)
    country_folder = os.path.join(MAIN_MOD, HISTORY_COUNTRY_PATH)
    countries = [fname[:3] for fname in os.listdir(country_folder)]
    countries56 = [fname[:3] for fname in os.listdir(country_folder56)]
    common_countries = set(countries).intersection(countries56)
    rest_countries = set(countries).difference(countries56)
    df = pd.DataFrame(columns=sorted(list(rt56_techs)),
                      dtype=pd.Int64Dtype())

    for fname in sorted(os.listdir(country_folder56)):
        tag = fname[:3]
        if tag in common_countries:
            try:
                obj = paradox2list(os.path.join(country_folder56, fname))
            except:
                import pdb
                pdb.set_trace()

            found, inds = has_key(obj, SET_TECH_KEY)
            if len(found) == 0:
                df.loc[tag] = float("nan")
            else:
                for tech in rt56_techs:
                    found2, inds = has_key(found, tech)
                    if len(found2) == 0:
                        df.loc[tag, tech] = float("nan")
                    elif len(found2) == 1:
                        val = found2[0][1][0]
                        df.loc[tag, tech] = val
                    else:
                        import pdb
                        pdb.set_trace()

    for tag in sorted(rest_countries):
        # set defaults
        df.loc[tag, "camo"] = 1
        df.loc[tag, "etax_doctrine"] = 1
    df.to_csv(out_file)


def apply_equipment_table(file_name):
    df = pd.read_csv(file_name, header=0, index_col=0)
    techs = list(df.columns)
    country_folder = os.path.join(MAIN_MOD, HISTORY_COUNTRY_PATH)
    file_dict = {fname[:3]: fname for fname in os.listdir(country_folder)}
    maps = {}
    for fname in os.listdir(country_folder):
        tag = fname[:3]
        vals = [[tech, [df.loc[tag, tech] if pd.isna(df.loc[tag, tech]) else int(df.loc[tag, tech])]]
                for tech in techs if not pd.isna(df.loc[tag, tech])]
        mapping = [[has_key_and_max_level, [SET_TECH_KEY, 1]],
                   [add_multiple_values, vals]
                   ]
        maps[tag] = mapping
    return maps


def apply_equipment_maps(general_maps, specific_maps):
    in_folder = os.path.join(MAIN_MOD, HISTORY_COUNTRY_PATH)
    out_folder = os.path.join(OUT_FOLDER, HISTORY_COUNTRY_PATH)
    file_list = os.listdir(in_folder)
    #file_list = ["FRA - France.txt"]
    os.makedirs(out_folder, exist_ok=True)

    for file in file_list:
        tag = file[:3]
        maps = general_maps + [specific_maps[tag]]
        try:
            apply_maps_on_file(os.path.join(in_folder, file),
                               os.path.join(out_folder, file),
                               maps)
        except:
            import pdb
            pdb.set_trace()


def filter_spirits(fname, keys):
    idea_path = os.path.join(MAIN_MOD, IDEA_PATH)
    rt56_idea_path = os.path.join(RT56_FOLDER, IDEA_PATH)
    rt56_fname = fname if KX is True else KR_REV_SPIRIT_MAP[fname]

    obj1 = paradox2list(os.path.join(rt56_idea_path, rt56_fname))
    obj2 = paradox2list(os.path.join(idea_path, fname))
    new_obj = [["ideas", []]]
    tech_crit = TECH_CRITS[fname] if KX is True else KR_TECH_CRITS[fname]

    skeys = [None]*2
    for key in keys:
        for k, obj in enumerate([obj1, obj2]):
            _, inds = has_key(obj, key)
            spirits = get_object_from_inds(obj, inds[0])
            skeys[k] = {o[0] for o in spirits[1]}

        diff = skeys[1].difference(skeys[0])
        diff = {d for d in diff if d not in SPIRIT_FILTER}
        missing = []
        exceptions = {'KR_whampoa_academy_spirit'}
        for dkey in diff:
            o1, inds = has_key(obj2, dkey)
            ava, _ = has_key(o1, "available")
            if len(ava) == 0:
                o1[0][1] += [tech_crit]
            elif o1[0][0] in exceptions:
                pass
            else:
                import pdb
                # pdb.set_trace()
                pass

            missing += o1

        if len(missing) > 0:
            new_obj[0][1].append([key, missing])
    prefix = "kx_" if KX is True else "kr_"
    out_path = os.path.join(OUT_FOLDER, IDEA_PATH)
    os.makedirs(out_path, exist_ok=True)
    out_file = os.path.join(out_path, prefix+fname)

    with open(out_file, 'w', encoding=UTF8) as file:
        content = list2paradox(new_obj)
        file.write(content)

    # copy rt56 file
    orig_in_file = os.path.join(rt56_idea_path, rt56_fname)
    orig_out_file = os.path.join(out_path, fname)
    shutil.copy2(orig_in_file, orig_out_file)


def update_chinese_army_reform(file="China_decisions.txt"):
    in_folder = os.path.join(MAIN_MOD, DECISION_PATH)
    out_folder = os.path.join(OUT_FOLDER, DECISION_PATH)
    os.makedirs(out_folder, exist_ok=True)
    tech_dic = {"delay": ("r56_double_envelopment",),
                "mobile_infantry": ("r56_infiltration_assault", "r56_milita_formation"),
                "mass_motorization": ("r56_infiltration_in_depth", "r56_nd_conscription"),
                "mechanised_offensive": ("r56_backhand_blow", "r56_peoples_army"),
                "volkssturm": ("r56_prepared_defense", "r56_breakout")
                }
    maps = []
    for key, techs in tech_dic.items():
        values = [[HAS_TECH_KEY, [tech]] for tech in techs]
        maps += [[[has_value, [HAS_TECH_KEY, [key]]],
                  [add_multiple, values]]]

    obj = paradox2list(os.path.join(in_folder, file))
    try:
        apply_maps_on_file(os.path.join(in_folder, file),
                           os.path.join(out_folder, file),
                           maps)
    except Exception as exc:
        print(exc)
        import pdb
        pdb.set_trace()


if __name__ == "__main__":
    os.makedirs(OUT_FOLDER, exist_ok=True)
    # update rt56 techs
    update_keys = [key for key in rt56_update.__dict__.keys()
                   if key.startswith("update_")]
    for func in update_keys:
        rt56_update.__dict__[func](RT56_FOLDER, OUT_FOLDER)

    rt56_update.copy_update(RT56_FOLDER, OUT_FOLDER)
    # some simple post hacks
    # Change SOV --> RUS
    rt56_update.replace_string('SOV', 'RUS', OUT_FOLDER)
    # Change r56_tech_RUS --> r56_tech_SOV to get gfx_files back on track
    rt56_update.replace_string('r56_tech_RUS', 'r56_tech_SOV', OUT_FOLDER)
    rt56_update.patch_ai(MAIN_MOD, RT56_FOLDER, KR_FOLDER, OUT_FOLDER, KX)
    rt56_update.patch_bugs(MAIN_MOD, RT56_FOLDER, KR_FOLDER, OUT_FOLDER, KX)

    if KX is True:
        import kx_patches as patches
    else:
        import kr_patches as patches
    patches.patch(MAIN_MOD, OUT_FOLDER)

    # add missing spirits

    for fname, keys in SPIRIT_KEYS.items() if KX is True else KR_SPIRIT_KEYS.items():
        filter_spirits(fname, keys)
    # update China Army Reform
    chn_fname = "China_decisions.txt" if KX is True else "01 China decisions.txt"
    update_chinese_army_reform(chn_fname)
    # create_equipment_table(os.path.join(OUT_FOLDER,"equipment.csv"))
    maps = ideology_map()
    # apply_ideology_map(maps)
    maps = remove_obsolete_equipment_maps()
    country_maps = apply_equipment_table(
        "KX_equipment.csv" if KX is True else "equipment.csv")
    apply_equipment_maps(maps, country_maps)
