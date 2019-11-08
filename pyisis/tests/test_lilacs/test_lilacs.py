# -*- coding: utf-8 -*-

"""
File to test Formatting Language - database Lilacs
"""

__created__ = "2009-08-24"
__updated__ = "2009-08-24"
__author__  = "João Chaves <joaochaves@gpr.com.br>"

from os.path import join, exists
from os import remove, getcwd
from sys import platform, path
from pyisis.files import MasterFile
from pyisis.config import config as base_config
from pyisis.engine import Engine

path.append('../../')
path.append('../')

from mxpy import *

FIXTURES_DIR = 'fixtures'

def initialize():
    """Prepare test environment"""
    set_i18n(base_config)
    Engine.setup(base_config)
    return Engine.config

def set_i18n(config):
    """Activate i18n in the test environment"""
    localedir = join('..','..','locale')
    gettext.install('pyisis',localedir=localedir)
    lang1 = gettext.translation('pyisis', languages=[config.LANGUAGE],localedir=localedir)
    lang1.install(unicode=1)
    
# global setup
config = initialize()
    
def invcb(total,current):
    pass

def test_inverting_ntitle():
    """Test inverting ntitle database """
    db = join('fixtures','ntitle.mst')
    mf = MasterFile(db)
    #Remove old indexes files
    for ext in ('.idx','.idx.index','.idx.lock','.idx.old','.idx.tmp'):
        fname = join('fixtures','ntitle.%s' % ext)
        if exists(fname):
            remove(fname)
    mf.invertdb(callback = invcb)
    post = mf.search('0000-0019').next()
    assert post.mfn == 12222, 'Failed inverting ntitle database'
    
    
def test_inverting_MAIL():
    """Test inverting MAIL database """
    db = join('fixtures','MAIL.mst')
    mf = MasterFile(db)
    #Remove old indexes files
    for ext in ('.idx','.idx.index','.idx.lock','.idx.old','.idx.tmp'):
        fname = join('fixtures','MAIL.%s' % ext)
        if exists(fname):
            remove(fname)
    mf.invertdb(callback = invcb)
    post = mf.search('AR1.1').next()
    assert post.mfn == 63, 'Failed inverting MAIL database'
    
    
def test_lilthtm():
    """Test lilthtm.pft database lilacs"""
        
    config.load(join('fixtures','lilacs.ini'))
    current_path = join(os.getcwd(),'fixtures')
    collection = pyisis.files.IsisCollection('fixtures',[current_path],config=config)
    database = collection['lilacs']
    
    expr = ''.join(open(join('fixtures','lilthtm.pft')).readlines())
    result_mx = open(join('fixtures','mx-lilthtm')).read()
    session = session = Session(config)
    result_mxpy = format(session, expr, database, 1, 3226, config, stdout=0)
    
    assert result_mxpy == result_mx, "Failed for lilthtm.pft"
    
    
def test_lilchtm():
    """Test lilchtm.pft database lilacs"""
        
    config.load(join('fixtures','lilacs.ini'))
    current_path = join(os.getcwd(), 'fixtures')
    collection = pyisis.files.IsisCollection('fixtures',[current_path],config=config)
    database = collection['lilacs']
    
    expr = ''.join(open(join('fixtures','lilchtm.pft')).readlines())
    result_mx = open(join('fixtures','mx-lilchtm')).read()
    session = Session(config)
    result_mxpy = format(session, expr, database, 1, 3226, config, stdout=0)
    #open('mxpyc.txt','w').write(result_mxpy)
    assert result_mxpy == result_mx, "Failed for lilchtm.pft"
    
    
def test_lillhtm():
    """Test lillhtm.pft database lilacs"""
        
    config.load(join('fixtures','lilacs.ini'))
    current_path = join(os.getcwd(),'fixtures')
    collection = pyisis.files.IsisCollection('fixtures',[current_path],config=config)
    database = collection['lilacs']
    
    expr = ''.join(open(join('fixtures','lillhtm.pft')).readlines())
    result_mx = open(join('fixtures','mx-lillhtm')).read()
    session = Session(config)
    result_mxpy = format(session, expr, database, 1, 3226, config, stdout=0)
    #open('mxpyl.txt','w').write(result_mxpy)
    assert result_mxpy == result_mx, "Failed for lillhtm.pft"    
   

def test_lildhtm():
    """Test lildhtm.pft database lilacs"""
        
    config.load(join('fixtures','lilacs.ini'))
    current_path = join(os.getcwd(),'fixtures')
    collection = pyisis.files.IsisCollection('fixtures',[current_path],config=config)
    database = collection['lilacs']
    
    expr = ''.join(open(join('fixtures','lildhtm.pft')).readlines())
    result_mx = open(join('fixtures','mx-lildhtm')).read()
    session = Session(config)
    result_mxpy = format(session, expr, database, 1, 3226, config, stdout=0)
    #open('mxpyd.txt','w').write(result_mxpy)
    assert result_mxpy == result_mx, "Failed for lildhtm.pft"    

   
    
if __name__ == '__main__':
    test_lilchtm()
    #test_inverting_ntitle()
    #test_inverting_MAIL()
    