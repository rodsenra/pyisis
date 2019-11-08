# -*- coding: utf-8 -*-

"""
File to test Formatting Language Parser
"""

__created__ = "2008-05-27"
__updated__ = "2008-05-26"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

import tempfile
from pyisis.records import MasterRecord
from pyisis.lexer import PftLexer
from pyisis.parser import PftParser
from pyisis.ast import  *


from pyisis.tests.config_tests import test_data, Lyer, initialize, run_list
config = initialize()

tmpdir = tempfile.gettempdir()
lexer = PftLexer()
parser = PftParser(lexer=lexer.lexer, debug=False, outputdir=tmpdir)
compiler = PftCompiler()

def setup():
    "Fixture: Called before every test to reset the lexer"
    pass

def test_empty():
    """Parse empty expression"""
    try:
        pft_ast = parser.parse("")
    except RuntimeError:
        assert False, "Incorrect handling of empty expression"
    else:
        pass

def test_field():
    """Parse field access"""
    ast = parser.parse("V70")
    assert type(ast)==Field, "AST has no FieldAccess node as first node"


def test_compile_code():
    """Compile a simple ast into Python executable code"""
    rec = MasterRecord()
    data = "Paper on: <plant physiology><plant transpiration><measurement and instruments>"
    rec.v69 = data
    ast = parser.parse("V69")
    chain = flatten(ast)
    pft = compiler.compile_code(chain)
    result = pft(rec=rec, mst=None)
    #print "result=", repr(result), "\ndata=", repr(data)
    # remove line braks prior to comparison with original data
    assert result.replace("\n","")==data

def test_ilit():
    """Test Inconditional literal"""
    rec = MasterRecord()
    rec.v26 = "^aParis^bUnesco^c-1965"
    rec.v30 = "^ap. 211-224^billus."
    ast = parser.parse("'Pais:'v26^a,v30^a")


def debug_format(fmt):
    lexer.input(fmt)
    print "Lexer\n"
    for tok in lexer:
        print tok
    print "Parser\n"
    ast = parser.parse(fmt)
    print ast


if __name__ == "__main__":
    #test_empty()
    #test_field()
    #test_ilit()
    #test_compile_code()
    pass