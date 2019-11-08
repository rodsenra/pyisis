# -*- coding: utf-8 -*-

"""
File to test Formatting Language Lexer
"""

__created__ = "2008-05-20"
__updated__ = "2008-05-20"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

# Setup test environment
from pyisis.tests.config_tests import test_data, Lyer, initialize
config = initialize()

from pyisis.lexer import PftLexer
lexer = PftLexer()

def setup():
    "Fixture: Called before every test to reset the lexer"
    pass

def test_xspacer():
    """Tokenize Xn """
    lexer.input("x3")
    tokens = list(lexer)
    assert tokens[0].type=='XSPACER', "Found %s instead of XSPACER"%tokens[0].type
    assert tokens[0].value==3


def test_empty():
    """Tokenize empty expression"""
    lexer.input("")
    tokens = list(lexer)
    assert len(tokens)==0

def test_fields():
    """Tokenize fields"""
    fields = {
    "v1": {'tag':1, 'type':'v'},
    "v1^a": {'tag':1, 'subfield': 'a', 'type':'v'},
    "v1^a[1..10]": {'tag':1, 'subfield': 'a', 'occurence':(1,10), 'type':'v'},
    "v1^a[1..LAST]": {'tag':1, 'subfield': 'a', 'occurence':(1,'LAST'), 'type':'v'},
    "v1^a[1]": {'tag':1, 'subfield': 'a', 'occurence':(1,''), 'type':'v'},
    "v1^a[LAST]": {'tag':1, 'subfield': 'a', 'occurence':('LAST',''), 'type':'v'},
    "v1^a[1..]*3.5":{'tag':1, 'subfield': 'a', 'occurence':(1,''),'slicer':(3,5), 'type':'v'},
    "v1^a[1..]*3.5(5,7)":{'tag':1, 'subfield': 'a', 'occurence':(1,''),
                          'slicer':(3,5),'alignment':(5,7), 'type':'v'},
    "v1^a[1..](5,7)":{'tag':1, 'subfield': 'a', 'occurence':(1,''),'alignment':(5,7), 'type':'v'},
    "v1^a(5,7)":{'tag':1, 'subfield': 'a', 'alignment':(5,7), 'type':'v'},
    "v1(5,7)":{'tag':1, 'alignment':(5,7), 'type':'v'},
    "v1(5)":{'tag':1, 'alignment':(5,0), 'type':'v'},
    "v1^a[1..](5,7)":{'tag':1, 'subfield': 'a', 'occurence':(1,''), 'alignment':(5,7), 'type':'v'},
    "v1[1..]*3.5(5,7)":{'tag':1, 'occurence':(1,''), 'slicer':(3,5),'alignment':(5,7), 'type':'v'},
    "v1[1..]*3.5":{'tag':1, 'occurence':(1,''), 'slicer':(3,5), 'type':'v'},
    "v1*3.5":{'tag':1, 'slicer':(3,5), 'type':'v'},
    "v1^*":{'tag':1, 'subfield':'*', 'type':'v'}
    }
    for expr, struct in fields.items():
        lexer.input(expr)
        tokens = list(lexer)
        assert len(tokens)==1, "Received more tokens than expected for %s -> %s"%(expr,tokens)
        tok = tokens[0]
        assert tok.type=="VFIELD"
        assert tok.value==struct,\
         "Invalid field %s expected %s != struct %s"%(expr, tok.value, struct)

def test_repeatable_literal():
    """Tokenize expression with repeatable literal"""
    lexer.input("v2, |Title: |v1")
    tokens = list(lexer)
    print tokens
    assert len(tokens)==4
    tok = tokens[2]
    assert tok.type=="REPEATABLELITERAL"
    assert tok.value=='Title: '

def test_conditional_literal():
    """Tokenize expression with conditional literal"""
    lexer.input('"_Autor_"v1')
    tokens = list(lexer)
    print tokens
    assert len(tokens)==2
    tok = tokens[0]
    assert tok.type=="CONDITIONALLITERAL"
    assert tok.value=='_Autor_'

def test_inconditional_literal():
    """Tokenize expression with inconditional literal"""
    lexer.input("""'Data->'v1""")
    tokens = list(lexer)
    print tokens
    assert len(tokens)==2
    tok = tokens[0]
    assert tok.type=="INCONDITIONALLITERAL"
    assert tok.value=='Data->'

def test_nested_literals():
    """Tokenize expression with nested literals"""
    lexer.input("""'"Data"'v1""")
    tokens = list(lexer)
    lexer.input(''' "'Data'"'v1 ''')
    tokens = list(lexer)

test_sequence = """
v2/,v3^a| - |,v1/,
(|; |+v3^s)/,
v5[3..]/,/* equals to ,v5[3..LAST], */
|Title: |v1^n(5,5)/,
v1^n*0.3,
v20[4],
v10[2..7]/,
v1[LAST]*2.7/,
v1(5,5)/,
"""

def test_field_sequence():
    """Tokenize field sequences"""
    for text in test_sequence.splitlines():
        lexer.input(text)
        try:
            for tok in lexer:
                print tok
        except SyntaxError, ex:
            assert False, ex.message

def test_mode():
    """Tokenize mode strings"""
    modes = """
    mpl,V24
    mhl,V24
    mdl,V24
    mdu,V24
    mpl,V26
    mhl,V26
    mdu,V26
    mpl,V69
    mdl,V69
    """
    for text in modes.splitlines():
        lexer.input(text)
        for tok in lexer:
            if tok.type=='MODE':
                assert len(tok.value)==2
                assert tok.value[0] in 'phd', "Mode not set"
                assert tok.value[1] in 'ul', "Conversion not set"

def test_mfn():
    """Tokenize mfn strings"""
    samples = {"MFN":6,
               "mfn":6,
               "mfn(3)":3,
               "MFN(2)":2
               }
    for expr, size in samples.items():
        lexer.input(expr)
        for tok in [t for t in lexer]:
            assert tok.type=='MFN', "Failed for %s type==%s"%(expr, tok.type)
            assert tok.value==samples['expr']


def dump_tokens(text):
    lexer.input(text)
    for tok in lexer:
        print tok

if __name__=="__main__":
    test_xspacer()