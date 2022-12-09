#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################################################################
# Generic Patch snippets                                              #
#######################################################################

gen_ai_patch = """
               ai_will_do = {
                 factor = 1
               }
               """

gen_ai_major_patch = """
                ai_will_do = {
                  factor = 1
                  modifier = { factor = 2
                               is_major = yes} }
                 """

#######################################################################
# Patches for Air tech                                                #
#######################################################################

air_snippets = []
air_patches = []

air_snippets += ["""
              ai_will_do = {
                 factor = 1
                 modifier = {
                  factor = 2
                   tag = RUS }
                modifier = {
                  factor = 2
                  tag = GER }
               modifier = {
                 factor = 2
                 tag = ENG
                 }}
              """]
air_patches += [gen_ai_major_patch]
air_snippets += ["""
                  ai_will_do = {
                      factor = 1
                      modifier = {
                      factor = 2
                      tag = USA }
                  modifier = {
                  factor = 2
                  tag = GER }
                  modifier = {
                  factor = 2
                  tag = ENG } }
                  """]
air_patches += [air_patches[0]]
air_snippets += ["""
                    ai_will_do = {
                    factor = 1
                    modifier = {
                    factor = 2
                    tag = AST }
                    modifier = {
                       factor = 2
                       tag = GER }
                    modifier = {
                         factor = 2
                         tag = ENG }
                    modifier = {
                         factor = 2
                         tag = JAP } }
                    """]
air_patches += [air_patches[0]]
air_snippets += ["""
ai_will_do = {
            factor = 1
            modifier = {
                factor = 3
                tag = USA
            }
            modifier = {
                factor = 2
                tag = AST
            }
            modifier = {
                factor = 2
                tag = GER
            }
            modifier = {
                factor = 2
                tag = ENG
            }
            modifier = {
                factor = 3
                tag = JAP
            }         
        }
"""]
air_patches += [air_patches[0]]
air_snippets += ["""
        ai_will_do = {
            factor = 1
            modifier = {
                factor = 2
                tag = AST
            }
            modifier = {
                factor = 2
                tag = ENG
            }
            modifier = {
                factor = 2
                tag = USA
            }
        }
        """]
air_patches += [air_patches[0]]
air_snippets += ["""
ai_will_do = {
            factor = 1
            modifier = {
                factor = 2
                tag = AST
            }
            modifier = {
                factor = 2
                tag = ENG
            }
        }
        """]
air_patches += [gen_ai_patch]
air_snippets += ["""
           modifier = {
                factor = 2
                tag = USA
                
            }"""]
air_patches += ['']
air_snippets += [air_snippets[-1].replace('2','3')]
air_patches += ['']

#######################################################################
# Patches for Armor tech                                              #
#######################################################################

tank_snippets = []
tank_patches = []
tank_snippets += ["""
                 modifier = {
				factor = 20
				tag = BEL 
				has_completed_focus = tblra_light_tank_destroyers
			}
                  """]
tank_patches += ['']

tank_snippets += ["""
                   OR = {
		          original_tag = USA
			  original_tag = JAP
			 }
                  """]
tank_patches += ["""
                  OR = { original_tag = JAP }
                """]


#######################################################################
# Patches for MTG Naval tech                                          #
#######################################################################

mtg_naval_snippets = []
mtg_naval_patches = []
mtg_naval_snippets += ["""
                       OR = { tag = GER
			      tag = USA
			    }
                       """]
mtg_naval_patches += ["""
                      OR = { tag = GER
			      tag = GEA
			    }
                      """]
mtg_naval_snippets += ["""
                      OR = { tag = ENG
			     tag = JAP
			     tag = USA }
                      """]
mtg_naval_patches += ["is_major = yes"]
mtg_naval_snippets += ["""
                      OR = { original_tag = ENG
			     original_tag = JAP
			     original_tag = USA }
                      """]
mtg_naval_patches += ["is_major = yes"]
mtg_naval_snippets += ["""
                      OR = { tag = ENG
			     tag = USA }
                      """]
mtg_naval_patches += ["is_major = yes"]
mtg_naval_snippets += ["tag = HOL"]
mtg_naval_patches += ["tag = GEA"]
mtg_naval_snippets += ["has_War_with = USA"]
mtg_naval_patches += ["has_War_with = JAP"]

#######################################################################
# Patches for MTG Naval support tech                                  #
#######################################################################
mtg_support_snippets = []
mtg_support_patches = []

mtg_support_snippets += ["""
                        OR = {
				tag = ENG
				tag = USA
				tag = JAP
				}"""]
mtg_support_patches += ["is_major = yes"]
mtg_support_snippets +=["""
                        OR = {
				tag = JAP
				tag = USA
				tag = GER
				}"""]
mtg_support_patches += ["is_major = yes"]
mtg_support_snippets += ["""
                        ai_will_do = {
			factor = 3
			modifier = {
				is_historical_focus_on = yes
				tag = JAP
				factor = 0.25
			}
			modifier = {
				tag = USA
				factor = 3
			}
			modifier = {
				has_war = yes
				factor = 2
			}
		        }"""]
mtg_support_patches += ["""
                        ai_will_do = {
			factor = 3
			modifier = {
				has_war = yes
				factor = 2
			     }
		        }"""]
mtg_support_snippets += ["""
                       OR = {
				tag = GER
				tag = USA
				tag = ENG
				tag = RUS
				}
                       """]
mtg_support_patches += ["is_major = yes"]
# Replace Rest USA entries with GEA
mtg_support_snippets += ["tag = USA"]
mtg_support_patches += ["tag = GEA"]
