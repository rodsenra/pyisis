# -*- coding: utf-8 -*-

"""
Error Messages
"""

__updated__ = "2008-07-16"
__created__ = "2008-07-16"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"



# Error messages
invalid_collection = "\n"+\
_("ERROR: config file %s with invalid entry: %s.\n")+\
_("Expecting <typename>,<path>.\n")

invalid_bool = "\n"+\
_("ERROR: config file %s with invalid entry: %s.\n")+\
_("Expecting True or False.\n")

invalid_encoding = "\n"+\
_("ERROR: config file %s with invalid encoding entry: %s.\n")+\
_("This codec is either not registered or it is spelled incorrectly.\n")

