# -*- coding: utf-8 -*-

"""
File to test Indexing Techniques
"""

__created__ = "2009-09-14"
__updated__ = "2009-09-14"
__author__  = "João Chaves <joaochaves@gpr.com.br>"

from os.path import join, exists
from os import remove, getcwd
from sys import platform, path
from pyisis.files import MasterFile
from pyisis.config import config as base_config
from pyisis.engine import Engine
import gettext

path.append('../../')
path.append('../')

FIXTURES_DIR = 'fixtures'

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
    
# global setup
config = initialize()
    
def invcb(total,current):
    pass

def test_inv_it_0_4():
    """Test Indexing Techniques 0-4 """

    db = join(FIXTURES_DIR,'cds.mst')
    mf = MasterFile(db)
    #Remove old indexes files
    for ext in ('.idx','.idx.index','.idx.lock','.idx.old','.idx.tmp'):
        fname = join(FIXTURES_DIR,'cds.%s' % ext)
        if exists(fname):
            remove(fname)
    mf.invertdb(fst=join(FIXTURES_DIR,'it_0-4.fst') ,callback = invcb)

    post = mf.search('ABEYWICKRAMA, B.A.').next()
    assert post.mfn == 60, 'Failed IT 0'
    post = mf.search('BOSIAN, G.').next()
    assert post.mfn == 2, 'Failed IT 0'

    post = mf.search('CENTER FOR NORTHERN EDUCATIONAL RESEARCH, UNIVERSITY OF ALAS').next()
    assert post.mfn == 89, 'Failed IT 1'
    post = mf.search('HUMANITIES PRESS').next()
    assert post.mfn == 143, 'Failed IT 1'

    post = mf.search('AGRICULTURE').next()
    assert post.mfn == 17, 'Failed IT 2/3'
    post = mf.search("CHILDREN'S BOOKS").next()
    assert post.mfn == 114, 'Failed IT 2/3'

    post = mf.search('EXPERIMENTAL').next()
    assert post.mfn == 130, 'Failed IT 4'
    post = mf.search("MONOLITHS").next()
    assert post.mfn == 20, 'Failed IT 4'


def test_inv_it_5_8():
    """Test Indexing Techniques 5-8"""

    db = join(FIXTURES_DIR,'cds.mst')
    mf = MasterFile(db)
    #Remove old indexes files
    for ext in ('.idx','.idx.index','.idx.lock','.idx.old','.idx.tmp'):
        fname = join(FIXTURES_DIR,'cds.%s' % ext)
        if exists(fname):
            remove(fname)
    mf.invertdb(fst=join(FIXTURES_DIR,'it_5-8.fst') ,callback = invcb)

    post = mf.search('AU_CHAPMAN, VALENTINE J.').next()
    assert post.mfn == 62, 'Failed IT 0 (Prefix)'
    post = mf.search('AU_HOLLERWOGER, F.').next()
    assert post.mfn == 47, 'Failed IT 0 (Prefix)'

    post = mf.search('TECHNIQUE TEST 5: CENTER FOR THE ADVANCED STUDY OF EDUCATION').next()
    assert post.mfn == 113, 'Failed IT 5'
    post = mf.search('TECHNIQUE TEST 5: LANSING, MICH.').next()
    assert post.mfn == 138, 'Failed IT 5'

    post = mf.search('TECHNIQUE TEST 6: BRACKISH WATER').next()
    assert post.mfn == 48, 'Failed IT 6/7'
    post = mf.search('TECHNIQUE TEST 6: INFORMATION/LIBRARY FINANCING').next()
    assert post.mfn == 136, 'Failed IT 6/7'

    post = mf.search('TECHNIQUE TEST 8: DOCUMENTATION').next()
    assert post.mfn == 105, 'Failed IT 8'
    post = mf.search('TECHNIQUE TEST 8: YUGOSLAVIA').next()
    assert post.mfn == 90, 'Failed IT 8'


def test_inv_it_1000_1008():
    """Test Indexing Techniques 1000-1008"""

    db = join(FIXTURES_DIR,'cds.mst')
    mf = MasterFile(db)
    #Remove old indexes files
    for ext in ('.idx','.idx.index','.idx.lock','.idx.old','.idx.tmp'):
        fname = join(FIXTURES_DIR,'cds.%s' % ext)
        if exists(fname):
            remove(fname)
    mf.invertdb(fst=join(FIXTURES_DIR,'it_1000-1008.fst') ,callback = invcb)

    post = mf.search('MUELLER-DOMBOIS, D.').next()
    assert post.mfn == 12, 'Failed IT 1000'
    post = mf.search('OHYA, MASAHIKO').next()
    assert post.mfn == 111, 'Failed IT 1000'
    post = mf.search('SIMMONS, MELVIN K.').next()
    assert post.mfn == 16, 'Failed IT 1000'

    post = mf.search('A. PEDONE').next()
    assert post.mfn == 8, 'Failed IT 1001'
    post = mf.search('BRUXELLES').next()
    assert post.mfn == 36, 'Failed IT 1001'
    post = mf.search('UNIVERSITY OF ZAMBIA').next()
    assert post.mfn == 29, 'Failed IT 1001'

    post = mf.search('DEMOCRATIC KAMPUCHEA').next()
    assert post.mfn == 111, 'Failed IT 1002'
    post = mf.search('TAIWAN').next()
    assert post.mfn == 111, 'Failed IT 1002'
    post = mf.search('ZAMBIA').next()
    assert post.mfn == 29, 'Failed IT 1002'

    post = mf.search('ARMAMENTS').next()
    assert post.mfn == 8, 'Failed IT 1004'
    post = mf.search('BEHAVIOUR').next()
    assert post.mfn == 20, 'Failed IT 1004'
    post = mf.search('COMPARATIVE').next()
    assert post.mfn == 111, 'Failed IT 1004'

    post = mf.search('TECHNIQUE TEST 5: 25 JUNE 1976').next()
    assert post.mfn == 28, 'Failed IT 1005'
    post = mf.search('TECHNIQUE TEST 5: CENTER FOR RESEARCH ON UTILIZATION OF SCIE').next()
    assert post.mfn == 16, 'Failed IT 1005'
    post = mf.search('TECHNIQUE TEST 5: GENEVE').next()
    assert post.mfn == 11, 'Failed IT 1005'

    post = mf.search('TECHNIQUE TEST 6: DEMOCRATIC KAMPUCHEA').next()
    assert post.mfn == 111, 'Failed IT 1006'
    post = mf.search('TECHNIQUE TEST 6: ECONOMY').next()
    assert post.mfn == 22, 'Failed IT 1006'
    post = mf.search('TECHNIQUE TEST 6: EDUCATIONAL HISTORY').next()
    assert post.mfn == 11, 'Failed IT 1006'

    post = mf.search('TECHNIQUE TEST 8: ALLUVIONS').next()
    assert post.mfn == 111, 'Failed IT 1008'
    post = mf.search('TECHNIQUE TEST 8: ANNOTATED').next()
    assert post.mfn == 17, 'Failed IT 1008'
    post = mf.search('TECHNIQUE TEST 8: BROADCASTING').next()
    assert post.mfn == 29, 'Failed IT 1008'

    
if __name__ == '__main__':
    test_inv_it_0_4()
    