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
