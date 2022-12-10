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
# Patches for Infantry tech                                           #
#######################################################################
infantry_snippets =[]
infantry_patches =[]

infantry_snippets += ["""OR = {
				    tag = CHI
				    tag = PRC
				    tag = XSM
				    tag = SIK
				    tag = GXC
				    tag = SHX
				    tag = YUN
				}
                       """]
infantry_patches += ['']
infantry_snippets += ["tag = USA"]
infantry_patches += ['original_tag = USA']
infantry_snippets += ["""
                      OR = {
				tag = BRA
				tag = VEN
				tag = COG
				tag = INS
				tag = MAL
				tag = SIA
				tag = RAJ
				tag = AST
				tag = SAF
				}"""]
infantry_patches += ["""
                      OR = {
				tag = BRA
				tag = VEN
				tag = COG
				tag = INS
				tag = MAL
				tag = SIA
				tag = RAJ
				tag = AST
				tag = SAF
                                tag = GEA
                                tag = PRF
                                tag = HND
                                tag = MAF
				}"""]
infantry_snippets += ["""
                     OR = {
                    original_tag = CAN
                    original_tag = SWE
                    original_tag = FIN
                    original_tag = SAM
                    original_tag = GRL
                    original_tag = ICE
                    original_tag = QBC
                    original_tag = RUS }
                    """]
infantry_patches += ["""
                     OR = {
                    original_tag = CAN
                    original_tag = SWE
                    original_tag = FIN
                    original_tag = ICE
                    original_tag = RUS
                    original_tag = BAT
                    original_tag = TRM
                    } """]
infantry_snippets += ["""
                      OR = { 
                        original_tag = SWE
                        original_tag = FIN
                        original_tag = SAM
                        original_tag = GRL
                        original_tag = ICE
                        original_tag = QBC
                }
                      """]
infantry_patches += ["""
                      OR = { 
                        original_tag = SWE
                        original_tag = FIN
                        original_tag = ICE
                      }
                      """]
infantry_snippets += ["""
                     OR = {
                    tag = SAU
                    tag = IRQ
                    tag = EGY
                    tag = SAF
                    tag = SYR
                    tag = OMA
                    tag = LBA
                    tag = YEM
                     }
                     """]
infantry_patches += ["""
                     OR = {
                       tag = SAU
                       tag = IRQ
                       tag = JBS
                       tag = EGY
                       tag = SAF
                       tag = SYR
                       tag = OMA
                       tag = LIB
                       tag = YEM
                       tag = TUR
                       tag = NFA
                     }
                     """]
infantry_snippets += ["""
                      modifier = {
                factor = 3
                OR = {
                    original_tag = IRQ
                    original_tag = KUR
                    original_tag = PER
                    original_tag = SAU
                    original_tag = OMA
                    original_tag = UAE
                    original_tag = QAT
                    original_tag = KUW
                    original_tag = JOR
                    original_tag = PAL
                    original_tag = ISR
                    original_tag = SYR
                    original_tag = LEB
                    original_tag = YEM
                    original_tag = RAJ
                    original_tag = SRL
                    original_tag = PAK
                    original_tag = BAN
                    original_tag = HYD
                    original_tag = BYA
                    original_tag = SIA
                    original_tag = LAO
                    original_tag = CAM
                    original_tag = VIN
                    original_tag = INS
                    original_tag = PHI
                    original_tag = PNG
                    original_tag = MAL
                    original_tag = FRI
                    original_tag = AST
                    original_tag = MOR
                    original_tag = ALG
                    original_tag = TUN
                    original_tag = LBA
                    original_tag = EGY
                    original_tag = SUD
                    original_tag = ETH
                    original_tag = DJI
                    original_tag = ERI
                    original_tag = SOM
                    original_tag = SEN
                    original_tag = MLI
                    original_tag = NGA
                    original_tag = TZN
                    original_tag = MLW
                    original_tag = RWA
                    original_tag = BRD
                    original_tag = CAR
                    original_tag = CHA
                    original_tag = CMR
                    original_tag = GAB
                    original_tag = RCG
                    original_tag = ANG
                    original_tag = ZAM
                    original_tag = ZIM
                    original_tag = BOT
                    original_tag = NMB
                    original_tag = SAF
                    original_tag = MZB
                    original_tag = MAD
                    original_tag = KEN
                    original_tag = UGA
                    original_tag = COG
                    original_tag = BRA
                    original_tag = VEN
                    original_tag = CAY
                    original_tag = SUR
                    original_tag = GYA
                    original_tag = PAR
                    original_tag = BOL
                    
                }
                
            }"""]
infantry_patches += ['']


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

#######################################################################
# Patches for R56 Vehicles                                            #
#######################################################################
vehicle_snippet1 = """
                   AND = { OR = { #We get it. Everyone else is dumb
			        original_tag = USA
				original_tag = GER
				original_tag = SOV }
                                date > "1939.1.1" }
                     """
vehicle_snippet2 =  """
                     AND = { OR = {
                        original_tag = FRA
                        original_tag = ENG
                        original_tag = JAP }
                        date > "1940.1.1" }
                    """
vehicle_snippet3 = """
                    ai_will_do = {
                    factor = 2
                     modifier = { tag = USA
                         factor = 2 }
                     modifier = { tag = CAN
                         factor = 2 }}
                    """
vehicle_patch3 = """
                    ai_will_do = {
                    factor = 2
                    }
                    """
vehicle_snippet4 = "has_war_with = USA"
vehicle_snippet5 = """
                     modifier = { tag = USA
                         factor = 2 }
                   """
vehicle_patch5 = ""
