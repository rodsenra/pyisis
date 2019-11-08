# -*- coding: utf-8 -*-

"""Sample data used in regression test cases."""

__created__ = "2007-04-30"
__updated__ = "2008-04-30"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

import gettext
from os.path import join
from pyisis.config import config as base_config
from pyisis.session import format
from pyisis.engine import Engine

test_data = {
     44: "Methodology of plant eco-physiology:"+\
         " proceedings of the Montpellier Symposium",
     50: "Incl. bibl.",
     69: "Paper on: <plant physiology><plant transpiration>"+\
         "<measurement and instruments>",
     24: "Techniques for the measurement of transpiration"+\
         " of individual plants",
     26: "^aParis^bUnesco^c-1965",
     30: "^ap. 211-224^billus.",
     70: ["Magalhaes, A.C.", "Franco, C.M."]
}

def initialize():
    """Prepare test environment"""
    set_i18n(base_config)
    Engine.setup(base_config)
    return Engine.config

def set_i18n(config):
    """Activate i18n in the test environment"""
    localedir = join('..','locale')
    gettext.install('pyisis',localedir=localedir)
    lang1 = gettext.translation('pyisis', languages=[config.LANGUAGE],localedir=localedir)
    lang1.install(unicode=1)

class Lyer(object):
    """Class that generates attributes on demand"""
    def __getattr__(self, name):
        s = Lyer()
        setattr(self, name, s)
        return s

def run_list(expr_list, record):
    """Function to iterate over the expression list,
    displaying details about the failed assertions.
    The expr_list should be a list of pairs (expr, outcome).
    This functions tests if format(expr,record)==outcome.
    """
    for pos, (expr, result) in enumerate(expr_list):
        try:
            fmt = format(expr, record)
        except Exception, ex:
            fmt=''
            print str(ex)
            print "Failed for %d == <<%s>> "%(pos,expr_list[pos])
        assert fmt==result, "Failed for %d == <<%s>>:\n %r != %r"%(pos,expr_list[pos],
                                                           fmt, result)
