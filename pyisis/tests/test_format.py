# -*- coding: utf-8 -*-

"""
File to test Formatting Language - format
"""

__created__ = "2009-07-31"
__updated__ = "2008-07-30"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

from os.path import join, exists
from os import remove, getcwd
from sys import platform

from pyisis.files import Collection, MasterFile
from pyisis.records import MasterRecord
from pyisis.session import format

# global setup
from pyisis.tests.config_tests import test_data, Lyer, initialize, run_list
config = initialize()

# Adjust parser options
from pyisis.session import initialize as init_session
import tempfile
config.YACC_DEBUG = False
config.PARSER_AUXFILES_DIR = tempfile.gettempdir()
init_session(config)
config.SEARCH_PATH = join(getcwd(), 'fixtures')

def test_first_subfield():
    """Test sub-field acessor ^* in field with several subfields"""
    record = MasterRecord()
    record.update(test_data)
    first_subfield = format("v26^*", record)
    assert first_subfield=='Paris', 'Failed to extract first subfield'

def test_first_subfield_default():
    """Test sub-field acessor ^* in field without subfields"""
    record = MasterRecord()
    record.update(test_data)
    first_subfield = format("v50^*", record)
    assert first_subfield=='Incl. bibl.', 'Failed to extract first subfield'
    record.v13 = "First ^ok"
    assert format("v13^*", record)=='First ', 'Failed during first subfield extraction'

def test_max_width():
    """Test max width and field alignment"""
    record = MasterRecord()
    record.update(test_data)
    # Fake config and change default param MAX_LINE_WIDTH
    record.mst = Lyer()
    record.mst.config.INPUT_ENCODING = 'utf-8'
    record.mst.config.OUTPUT_ENCODING = 'utf-8'    
    record.mst.config.MAX_LINE_WIDTH = 40
    record.mst.config.YACC_DEBUG = False
    expr_list = (
                 ("v44",'Methodology of plant eco-physiology: \nproceedings of the Montpellier \nSymposium'),
                 ("v44(0,0)", 'Methodology of plant eco-physiology: \nproceedings of the Montpellier \nSymposium'),
                 ("v44(10)", '          Methodology of plant \neco-physiology: proceedings of the \nMontpellier Symposium'),
                 ("v44(0,5)",'Methodology of plant eco-physiology: \n     proceedings of the Montpellier \n     Symposium'),
                 ("v44(10,5)", '          Methodology of plant \n     eco-physiology: proceedings of the \n     Montpellier Symposium'),
                 # special case of unbreakable line
                 ("'%s'"%('a'*120), u'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'),
                 )
    run_list(expr_list, record)

def test_max_width_off():
    """Test max width==0 and field alignment"""
    record = MasterRecord()
    record.update(test_data)
    # Fake config and change default param MAX_LINE_WIDTH
    record.mst = Lyer()
    record.mst.config.INPUT_ENCODING = 'utf-8'
    record.mst.config.OUTPUT_ENCODING = 'utf-8'
    record.mst.config.MAX_LINE_WIDTH = 0
    record.mst.config.YACC_DEBUG = False
    expr_list = (
                 ("v44",'\nMethodology of plant eco-physiology: proceedings of the Montpellier Symposium'),
                 ("v44(0,0)", ''),
                 ("v44(10)",''),
                 ("v44(0,5)",''),
                 ("v44(10,5)",''),
                 )
    run_list(expr_list, record)

def test_field_expressions():
    """Test field access expressions"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (("v30^a,v30^b", 'p. 211-224illus.'),
                 ("v26^a", 'Paris'),
                 ("v26^a*2", 'ris'),
                 ("v26^a.2", 'Pa'),
                 ("v26^a*1.3", 'ari'),
                 )
    run_list(expr_list, record)


def test_field_index():
    """Test field index"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("v70[1]",'Magalhaes, A.C.'),
                 ("v70[2]",'Franco, C.M.'),
                 ("v70[1..2]",'Magalhaes, A.C.Franco, C.M.'),
                 ("v70[LAST]",'Franco, C.M.'),
                 ("v70[1..LAST]",'Magalhaes, A.C.Franco, C.M.'),
                 )
    run_list(expr_list, record)


def test_strfuncs():
    record = MasterRecord(mfn=1)
    record.update(test_data)

    if platform == 'linux2':
        value = '1.131400E+00'
    else:
        value = '1.131400E+000'

    expr_list = (("f(1.1314,2)", value),
                 ("f(3.1415,10,5)", '   3.14150'),
                 ("f(1.1314,3,0)", '  1'),
                 ("s('Pa','ris')",'Paris'),
                 ("s(mfn,v26)",'000001^aParis^bUnesco^c-1965'),
                )
    run_list(expr_list, record)

def test_unconditional_literals():
    """Test unconditional literals"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (("v30^a,' Belex ', v30^b", 'p. 211-224 Belex illus.'),
                 ("v26^a,' Belex'", 'Paris Belex'),
                 ("'Belex'",'Belex'),
                 ("mpu,'Belex'",'BELEX'),
                 ("'Belex ',v26^a","Belex Paris"),
                 ("'Belex 'v26^a","Belex Paris"),
                 ("v26^a' Belex'","Paris Belex"),
                 ("'Be''lex'","Belex"),
                 )
    run_list(expr_list, record)

def test_conditional_literals():
    """Test conditional literals"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (('"Do not show"v1', ''),
                 ('"Show"v26', 'Show^aParis^bUnesco^c-1965'),
                 ('mpu,"Show"v26', 'SHOW^APARIS^BUNESCO^C-1965'),
                 ('v1"Do not show"', ''),
                 ('v26"Show"', '^aParis^bUnesco^c-1965Show'),
                 ('"Do not show"v26^z', ''),
                 ('"Show"v26^a', 'ShowParis'),
                 ('v26^z"Do not show"', ''),
                 ('v26^b"Show"', 'UnescoShow'),
                 ('"Authors:"v70','Authors:Magalhaes, A.C.Franco, C.M.'),
                 ('v70" (authors)"','Magalhaes, A.C.Franco, C.M. (authors)'),
                 ('"->"x3v26','->   ^aParis^bUnesco^c-1965'),
                 )
    run_list(expr_list, record)

def test_repeatable_literals():
    """Test repeatable literals"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (('|Do not show|v1', ''),
                 ('|Show|v26', 'Show^aParis^bUnesco^c-1965'),
                 ('mpu,|Show|v26^a', 'SHOWPARIS'),
                 ('v1|Do not show|', ''),
                 ('v26|Show|', '^aParis^bUnesco^c-1965Show'),
                 ('|Do not show|v26^z', ''),
                 ('|Show|v26^a', 'ShowParis'),
                 ('v26^z|Do not show|', ''),
                 ('v26^b|Show|', 'UnescoShow'),
                 ('| Author:|v70',' Author:Magalhaes, A.C. Author:Franco, C.M.'),
                 ('| Author:|+v70','Magalhaes, A.C. Author:Franco, C.M.'),
                 ('|<Left> |v70| <Right>|',u'<Left> Magalhaes, A.C. <Right><Left> Franco, C.M. <Right>'),
                 ('|<Left> |+v70| <Right>|',u'Magalhaes, A.C. <Right><Left> Franco, C.M. <Right>'),
                 ('|<Left> |v70+| <Right>|',u'<Left> Magalhaes, A.C. <Right><Left> Franco, C.M.'),
                 ('|<Left> |+v70+| <Right>|',u'Magalhaes, A.C. <Right><Left> Franco, C.M.'),
                 ('|Show |v26^a|; |/', 'Show Paris; \n'),
                 ('|Show |+v26^a|; |/', 'Paris; \n'),
                 ('|Show |v26^a+|; |/', 'Show Paris\n'),
                 ('|Show |+v26^a+|; |/', 'Paris\n'),
                 ('|Show |v26^a(5,5)|; |/', '     Show Paris; \n'),
                 ('|Show |+v26^a(5,5)|; |/', '     Paris; \n'), 
                 ('|<antes>|+v70,|meio|+v26+|depois|/','Magalhaes, A.C.<antes>Franco, C.M.^aParis^bUnesco^c-1965\n'),
                )
    run_list(expr_list, record)


def test_spacing():
    """Test for vertical spacing commands: # / %"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (
                 ('v26^b v26^a','UnescoParis'),
                 ('v26^b  v26^a','UnescoParis'),
                 ('v26^b/v26^a','Unesco\nParis'),
                 ('v26^b///v26^a','Unesco\nParis'),
                 ('v26^b#v26^a','Unesco\nParis'),
                 ('v26^b/#v26^a','Unesco\n\nParis'),
                 ('v26^b##v26^a','Unesco\n\nParis'),
                 ('v26^b###%v26^a','Unesco\nParis'),
                 ('v26^bx10v26^a','Unesco          Paris'),
                 ('v26^bX10v26^a','Unesco          Paris'),
                 ('v26^bX100v26^a',"Unesco\nParis"),
                 ('v26^bC0v26^a',"Unesco\nParis"),                 
                 ("v26^bC7v26^a", "UnescoParis"),
                 ("v26^bC8v26^a", "Unesco Paris"),
                 # ignore tabulation that exceeds MAX_WIDTH
                 ("v26^bC120v26^a", "UnescoParis"),
                 ("v26^bC5v26^a","Unesco\n    Paris"),
                 ("### X3 v26^b","\n\n\n   Unesco"),
                 ("###,X3,v26^b","\n\n\n   Unesco"),
                 ("v26^a#","Paris\n"),
                 ("v26^a///","Paris\n"),
                 ("v26^a#","Paris\n"),
                 ("v26^a%##v26^b%##v26^c","Paris\nUnesco\n\n-1965"),
                 )
    run_list(expr_list, record)


def test_numfunc():
    """Test Numerical functions"""
    record = MasterRecord()
    record.update(test_data)
    record.v13 = ["a 10", "b 20", "c 30"]
    expr_list = (
                 ('val(26)','26'),
                 ('val(v26)','-1965'),
                 ('val(V26)','-1965'),
                 ("v26^c*1",'1965'),
                 ("val('xxxx7yyyy8zzzz')","7"),
                 ("val('water')","0"),
                 ("val(10)*val(2)", "20"),
                 ("val('10')*val('2')", "20"),
                 ("val('dfsdf sdfsdf sdfsdfds')=0", "True"),
                 ("val('dfsdf sdfsdf sdfsdfds')", "0"),
                 ("val(v26)/10*-1","196.5"),
                 ("val(val(1))","1"),
                 ("val(-1)","-1"),
                 ("rsum(10,20,30)","60"),
                 ("rmax(10,20,30)","30"),
                 ("rmin(10,20,30)","10"),
                 ("ravr(10,20,30)","20"),
                 ("RSUM(10,20,30)","60"),
                 ("RMAX(10,20,30)","30"),
                 ("RMIN(10,20,30)","10"),
                 ("RAVR(10,20,30)","20"),
                 ("rsum('10')","10"),
                 ("rsum(10)","10"),
                 ("rsum('10,20,30')","60"),
                 ("rsum('a,10,b,20,c,30')","60"),
                 ("rsum(v26)","-1965"),
                 ("rsum(v26,1965)","0"),
                 ("rsum(v70)","0"),
                 ("rsum(v13)","60"),
                 ("rmax(v13)","30"),
                 ("rmin(v13)","10"),
                 ("ravr(v13)","20"),
                 ("rsum(v30)","-13"),
                 )
    run_list(expr_list, record)


def test_numerical_expr():
    """Test Numerical expressions"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (
                 ('0.155e+3','155.0'),
                 ('1e-3','0.001'),
                 ('2*3+9','15'),
                 ("2*(3+9)",'24'),
                 ("10-(4*(2-1))","6"),
                 ("15*0.001","0.015"),
                 )
    run_list(expr_list, record)

def test_boolean_expr():
    """Test Boolean expressions"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (
                 ("1<>2","True"),
                 ("1=2","False"),
                 ("1>2","False"),
                 ("1 > 2","False"),
                 ("1> 2","False"),
                 ("1 >2","False"),
                 ("1<2","True"),
                 ("1>=2","False"),
                 ("2>=1","True"),
                 ("2<=1","False"),
                 ("2>=1","True"),
                 ("1 > 2","False"),
                 ("1>2 or 2>1","True"),
                 ("1>2 and 2>1","False"),
                 ("1<2 or 2>1","True"),
                 ("1<2 and 2>1","True"),
                 ("1<2 xor 2>1","False"),
                 ("1>2 xor 2>1","True"),
                 ("not 1<2", "False"),
                 ("not (1<2)", "False"),
                 )
    run_list(expr_list, record)


def test_mfn_expressions():
    """Test MFN expressions"""
    #record = MasterRecord(mfn=4)
    #record.update(test_data)
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[4]
    expr_list = (("mfn", '000004'),
                 ("MFN", '000004'),
                 ("mfn(0)", '4'),
                 ("mfn(1)", '4'),
                 ("mfn(2)", '04'),
                 ("mfn=1","False"),
                 ("MFN>1","True"),
                 ("mfn=4","True"),
                 ("mfn<>4","False"),
                 ("not mfn=4","False"),
                 ("not mfn<>4","True"),
                 # Format
                 ("mfn/","000004\n"),
                 ("f(mfn+1,0,0)/","5\n"),
                 ("s(mfn,' ',v24)","000004 <An> Electric hygrometer apparatus for measuring water-vapour loss from \nplants in the field"),
                 ("ref(mfn,v24)","<An> Electric hygrometer apparatus for measuring water-vapour loss from plants \nin the field"),
                 ("if mfn=4 then mfn,/, fi","000004\n"),
                 )
    run_list(expr_list, record)

def test_if():
    """Test IFs statements and boolean functions"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (
                 ('if p(v26) then v26^a fi','Paris'),
                 ('if p(v25) then v26^a fi',''),
                 ('if p(v26) then v26^a else v26^b fi','Paris'),
                 ('if p(v25) then v26^a else v26^b fi','Unesco'),
                 ('if a(v26) then v26^a fi',''),
                 ('if a(v25) then v26^a fi','Paris'),
                 ('if a(v26) then v26^a else v26^b fi','Unesco'),
                 ('if a(v25) then v26^a else v26^b fi','Paris'),
                 ('if p(v26) then v26^a fi','Paris'),
                 ('if p(v26) then v26^a,v26^b fi','ParisUnesco'),
                 ('if p(v26) then v26^a v26^b fi','ParisUnesco'),
                 # field expression
                 ("if v26>'' then v26^a fi",'Paris'),
                 ("if v50:'bib' then v26^a fi",'Paris'),
                 # test for heading and trailing spaces
                 ("if 1=1 then 'ok' fi ","ok"),
                 ("  if 1=1 then 'ok' fi","ok"),
                 ("   if 1=1 then 'ok' fi   ","ok"),
                 ("if nocc(v70)=2 then 'OK' else 'NOK' fi","OK"),
                 )
    run_list(expr_list, record)

def test_boolean_functions():
    """Test boolean evaluation functions P() and A()"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (
                 ('p(v26)','True'),
                 ('a(v26)','False'),
                 ('P(v26)','True'),
                 ('A(v26)','False'),
                 )
    run_list(expr_list, record)

def test_dummy_field():
    """Test Dummy field constructs Dt, Dt^x, Nt, Nt^x"""
    record = MasterRecord()
    record.update(test_data)
    expr_list = (
                 ('"Ola:"V26^a','Ola:Paris'),
                 ('"Ola:"D26^a','Ola:'),
                 ('"Ola:"N26^a',''),
                 ('"Ola:"D23^a',''),
                 ('"Ola:"N23^a','Ola:'),
                 ('"Ola:"v26^a','Ola:Paris'),
                 ('"Ola:"d26^a','Ola:'),
                 ('"Ola:"n26^a',''),
                 ('"Ola:"d23^a',''),
                 ('"Ola:"n23^a','Ola:'),
                 ('"Ola:"v26','Ola:^aParis^bUnesco^c-1965'),
                 ('"Ola:"d26','Ola:'),
                 ('"Ola:"n26',''),
                 ('"Ola:"d23',''),
                 ('"Ola:"n23','Ola:'),
                 )
    run_list(expr_list, record)

def test_ref():
    """Test ref() function"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("ref(1,v70)",'Magalhaes, A.C.Franco, C.M.'),
                 ("REF(1,v70)",'Magalhaes, A.C.Franco, C.M.'),
                 ("REF(2,v70)",'Bosian, G.'),
                 ("ref(1+1,v70)",'Bosian, G.'),
                 ("ref(mfn,v70)",'Magalhaes, A.C.Franco, C.M.'),
                 ("ref(val(v30)-200,v24)", 'Measurement of water stress in plants'),
                 )
    run_list(expr_list, record)

def test_mid():
    """Test mid() function"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (('mid(v24,1,1)','T'),
                 ('mid(v24,0,2)','Te'),
                 ('mid(v24,-1,1)','T'),
                 )
    run_list(expr_list, record)

def test_left():
    """Test left() function"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (('left(v24,0)',''),
                 ('left(v24,-1)',''),
                 ('left(v24,10)','Techniques'),
                 ('left(v24,14)','Techniques for'),
                 )
    run_list(expr_list, record)

def test_right():
    """Test right() function"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (('right(v24,0)', ''),
                 ('right(v24,-1)', ''),
                 ('right(v24,1)', 's'),
                 ('right(v24,6)', 'plants'),
                 ('right(v24,17)', 'individual plants'),
                 ('right(v24,68)', 'Techniques for the measurement of transpiration of individual plants'),
                 ('right(v24,268)','Techniques for the measurement of transpiration of individual plants'),
                 )
    run_list(expr_list, record)

def test_instr():
    """Test instr() function"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("instr(v24,'')", '0'),
                 ("instr('','')", '0'),
                 ("instr(v24,'T')", '1'),
                 ("instr(v24,'plants')", '63'),
                 ("instr(v24,'individual plants')",'52'),
                 ("instr(v24,'Techniques for the measurement of transpiration of individual plants')",'1'),
                 )
    run_list(expr_list, record)

def test_replace():
    """Test repalce() function"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("replace(v24,'plants','fruits')", 'Techniques for the measurement of transpiration of individual fruits'),
                 ("replace(v24,'','')", 'Techniques for the measurement of transpiration of individual plants'),
                 ("replace(v24,'measurement of ','')", 'Techniques for the transpiration of individual plants'),
                 ("mdu,v26,'!',replace(v26^b,'Unesco','UnEsCo')/","PARIS, UNESCO, -1965.  !UnEsCo\n"),
                 ("mdu,v26,'!',replace(v26,'Unesco','UnEsCo')/","PARIS, UNESCO, -1965.  !^aParis^bUnEsCo^c-1965\n"),
                 ("mhu,v26,'!',replace(v26^b,'Unesco','UnEsCo')/","PARIS, UNESCO, -1965!UnEsCo\n"),
                 ("mhu,v26,'!',replace(v26,'Unesco','UnEsCo')/","PARIS, UNESCO, -1965!^aParis^bUnEsCo^c-1965\n"),
                 ("mpu,v26,'!',replace(v26^b,'Unesco','UnEsCo')/","^APARIS^BUNESCO^C-1965!UnEsCo\n"),
                 ("mpu,v26,'!',replace(v26,'Unesco','UnEsCo')/","^APARIS^BUNESCO^C-1965!^aParis^bUnEsCo^c-1965\n"),
                 )
    run_list(expr_list, record)

def test_size():
    """Test size() function"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("size(v24)", '68'),
                 ("size(v70)", '27'),
                 ("size('teste')", '5'),
                 ("size('')",'0'),
                 ("size('\n')",'1'),
                 ("if size(v69) > 10 then 'OK' fi",'OK'),
                 ("size((v70))", '27'),
                 ("size((|AU|v70|AU|))", '35'),
                 )
    run_list(expr_list, record)

def test_seconds():
    """Test seconds() function"""
    from time import mktime
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("seconds('20080911')", str(mktime((2008,9,11,0,0,0,0,0,0)))),
                 ("seconds('20080911 01')", str(mktime((2008,9,11,1,0,0,0,0,0)))),
                 ("seconds('20080911 0120')", str(mktime((2008,9,11,1,20,0,0,0,0)))),
                 ("seconds('20080911 012030')", str(mktime((2008,9,11,1,20,30,0,0,0))))
                 )
    run_list(expr_list, record)

def test_date():
    """Test date() function"""
    from time import strftime
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("date(DATETIME)", strftime('%d/%m/%y %H:%M:%S')),
                 ("date(DATEONLY)", strftime('%d/%m/%y')),
                 ("date", strftime('%Y%m%d %H%M%S %w %j')),
                 )
    run_list(expr_list, record)

def test_datex():
    """Test datex() function"""
    from time import strftime, localtime
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("datex('1147780749')", strftime('%Y%m%d %H%M%S %w %j',localtime(1147780749))),
                 )
    run_list(expr_list, record)


def test_mode():
    """Test mode operator"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[47]
    
    expr_list = (("mpl,v30",'^ap. 347-355^billus., maps'),
                 ('mpu,v30','^AP. 347-355^BILLUS., MAPS'),
                 ('mhl,v30','p. 347-355, illus., maps'),
                 ('mhu,v30','P. 347-355, ILLUS., MAPS'),
                 ('mdl,v30','p. 347-355, illus., maps.  '),
                 ('mdu,v30','P. 347-355, ILLUS., MAPS.  '),
                 ('mdu,v24','THE PROGRESS OF THE RIVER DELTAS IN JAVA.  '),
                 ('mhu,v69','PAPER ON: RIVER BASINS; DELTAS; SEDIMENTATION; FORESTS; SOIL SURVEYS; \nCARTOGRAPHY; INDONESIA'),
                 ('mdu,v30,mpl,v24','P. 347-355, ILLUS., MAPS.  <The> Progress of the river deltas in Java'),
                 
                 #Mode and Functions
                 ("mdu,mid(v24,12,20)/","ess of the river del\n"),
                 ("mdu,mstname","CDS"),
                 ("mdl,f(instr(v24,'<The> Progress'),0,0)","1"),
                 ("mdu,f(instr(v24,'<The> Progress'),0,0)","1"),
                 ("mdu,s(v69,'transpiration')/","PAPER ON: RIVER BASINS; DELTAS; SEDIMENTATION; FORESTS; SOIL SURVEYS; \nCARTOGRAPHY; INDONESIA.  TRANSPIRATION\n"),                 
                 ("mdu,left(v69,10)/","Paper on: \n"),
                 ("mdl,left(v69,10)/","Paper on: \n"),
                 ("mdu,right(v69,10)/","Indonesia>\n"),
                 ("mdl,right(v69,10)/","Indonesia>\n"),
                 ("mdu,replace(v24,'The','THE')/","<THE> Progress of the river deltas in Java\n"),
                 ("mdl,replace(v24,'The','THE')/","<THE> Progress of the river deltas in Java\n"),                
                 ("mdu,'aAaAaAaAaAa'","AAAAAAAAAAA"),
                 ("mdu,(|a- |v70)","A- HOLLERWÖGER, F.  "),
                 ("mpl,proc('a98|Yet another Test Proc|'),v98","Yet another Test Proc"),
                 ("mdu,proc('a99|Yet another Test Proc|'),v99","YET ANOTHER TEST PROC.  "),
                 )
    
    run_list(expr_list, record)



def test_repeatable_groups():
    """Test repetable groups """
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[89]
    expr_list = (("(v70 X10 v71)", 'Kleinfeld, Judith S.          University of Alaska (USA). Center for Northern \nEducational ResearchBloom, Joseph          University of Alaska (USA). \nInstitute of Social, Economic and Government Research'),
                 ("(|autor=|v70/,|afiliacao=|v26/)",'autor=Kleinfeld, Judith S.\nafiliacao=^aFairbanks, Alaska^bCenter for Northern Educational Research, \nUniversity of Alaska^c1973\nautor=Bloom, Joseph\n'),
                 # Preserved 
                 ("v70|;|v70","Kleinfeld, Judith S.;Bloom, Joseph;Kleinfeld, Judith S.Bloom, Joseph"),
                 ("(v70|;|v70)","Kleinfeld, Judith S.;Kleinfeld, Judith S.Bloom, Joseph;Bloom, Joseph"),
                 )
    run_list(expr_list, record)


def test_repeatable_groups2():
    """Test repetable groups for record 85"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[85]
    expr_list = (
                 ("# v70 if p(v71) then ## v71 / fi","\nSanyal, Bikas C.Case, John H.Dow, Philip S.Jackman, Mary Elizabeth\n\nUniversity of ZambiaIIEP\n"),
                 ("(v70 # if p(v71) then v71,## fi)","Sanyal, Bikas C.\nUniversity of Zambia\n\nCase, John H.\nIIEP\n\nDow, Philip S.\nJackman, Mary Elizabeth\n"),
                 )
    run_list(expr_list, record)    

def test_cat():
    """Test cat command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    if platform == 'linux2':
        expr_list = (("(cat('../tools/__init__.py'))",'''# make this a package\n__all__ = ['pymx' ] \n'''),
                     ("cat('')",'')
                     )        

    else:
        expr_list = (("(cat('..\\tools\\__init__.py'))",'''# make this a package\n__all__ = ['pymx' ] \n'''),
                     ("cat('')",'')
                     )

    run_list(expr_list, record)


def test_type():
    """Test type command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[2]
    expr_list = (("type('ABCDEFGHIJKLMNOPQRSTUVXYZ')",'A'),
                 ("type(v26^c)",'N'),
                 ("type(v69)",'X'))
    run_list(expr_list, record)

def test_numeric_variables():
    """Test numeric variables"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("e0:=1,e0","1"),
                 ("e0:=1,e0:=2,e0","2"),
                 ("e0:=10,e0:=e0+12,e0","22"),
                 ("e0:=100,if e0 > 99 then 'OK' fi","OK"),
                 )

def test_string_variables():
    """Test string variables"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("s0:='text label',mdu,s0","TEXT LABEL"),
                 ("s0:='TEXT',if size(s0) > 3 then 'Print so:',s0 fi","Print so:TEXT"),
                 )

def test_l():
    """Test l command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    #Remove old indexes files
    for ext in ('.idx','.idx.index','.idx.lock','.idx.old','.idx.tmp'):
        fname = join("..","sample","cds"+ext)
        if exists(fname):
            remove(fname)

    mf.invertdb('mdu,v26')
    record = mf[2]
    expr_list = (("l('1966.')","28"),
                 ("l('PARIS, UNESCO , 1966.')","28"),
                 ("l('15 JUNE 1976.')","126"))


def test_npost():
    """Test npost command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("npost('1966.')","50"),
                 ("npost('PARIS, UNESCO , 1966.')","1"),
                 ("npost('PARIS, UNESCO, 1976.')","5"),
                 ("npost('BLA')","0"),
                )
    run_list(expr_list, record)

def test_newline():
    """Test newline command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("newline('<BR>'),v70#","Magalhaes, A.C.Franco, C.M.<BR>"),
                 ("newline('<BR>'),v70#newline('\r\n'),v70#","Magalhaes, A.C.Franco, C.M.<BR>Magalhaes, A.C.Franco, C.M.\r\n"),
                 ("newline('\n'),v70#","Magalhaes, A.C.Franco, C.M.\n"),
                )

    run_list(expr_list, record)


def test_nocc():
    """Test nocc command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("nocc(v70)","2"),
                 ("nocc(v26)","1"),
                 ("nocc(v26^a)","1"),
                 ("nocc(v26^b)","1"),
                 ("nocc(v26^e)","0"),
                 ("nocc(v13)","0"),
                 ("nocc(v13^a)","0"),
                )
    run_list(expr_list, record)

def test_iocc():
    """Test iocc command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("(f(iocc,3,0),'.',v70/)","  1.Magalhaes, A.C.\n  2.Franco, C.M.\n"),
                 ("(f(iocc,3,0),'.',v24/)","  1.Techniques for the measurement of transpiration of individual plants\n"),
                 ("(f(iocc,2,0),'-',v70/)"," 1-Magalhaes, A.C.\n 2-Franco, C.M.\n")
                )
    run_list(expr_list, record)

def test_linewidth():
    """Test lw command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("lw(40),v69","Paper on: <plant physiology><plant \ntranspiration><measurement and \ninstruments>"),
                 ("lw(20),v24","Techniques for the \nmeasurement of \ntranspiration of \nindividual plants"),
                 ("lw(80),v24","Techniques for the measurement of transpiration of individual plants")
                 )
    run_list(expr_list, record)

def test_mstname():
    """Test mstname command"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("mstname", 'cds'),
                 ("mdu,mstname", 'CDS'),
                 )
    run_list(expr_list, record)

def test_occurence():
    """Test vfield occurences"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("v70[1..2]","Magalhaes, A.C.Franco, C.M."),
                 ("v70[1..1]","Magalhaes, A.C."),
                 ("v70[1]","Magalhaes, A.C."),
                 ("v70[2]","Franco, C.M."),
                 ("v26[1]^a","Paris"),
                 ("v70[1..200]","Magalhaes, A.C.Franco, C.M."),
                 ("e1:=1,e2:=2,v70[e1..e2]","Magalhaes, A.C.Franco, C.M."),
                 )
    run_list(expr_list, record)

def test_comments():
    """Test c-style comments"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("v70,/* ok */v26",  u'Magalhaes, A.C.Franco, C.M.^aParis^bUnesco^c-1965'),
                 ("v70,/* ok */", u'Magalhaes, A.C.Franco, C.M.'),
                 ("/* ok */v26" , '^aParis^bUnesco^c-1965'),
                 ("/* ok */ ", ""),
                 ("/*  */ ", ""),
                 ("/**/ ", ""),
                 )
    run_list(expr_list, record)

def test_include():
    """Test include"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    test_pft  = join('fixtures','test.pft')
    test2_pft = join('fixtures','test2.pft')
    expr_list = (("@%s" % test2_pft,  u'P. 211-224, ILLUS.  \nUnEsCo\nTechnique\n'),
                 ("v70[1],' - ',@%s" % test_pft,  u'Magalhaes, A.C. - P. 211-224, ILLUS.  !UnEsCo!Technique\nCDS\n000001\n'),
                )
    run_list(expr_list, record)

def test_while():
    """Test while"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("e1:=1,e2:=2,while e1<=e2 (f(e1,2,0),'-',v70[e1],e1:=e1+1)",  u' 1-Magalhaes, A.C. 2-Franco, C.M.'),
                 ("e1:=1,e2:=5,while e1<=e2 (f(e1,2,0),'. Test Loop\n',e1:=e1+1)", u' 1. Test Loop\n 2. Test Loop\n 3. Test Loop\n 4. Test Loop\n 5. Test Loop\n'),
                 ("e1:=1,e2:=nocc(v70),while e1<=e2(f(e1,1,0),'. ', v70[e1]/e1:=e1+1,),","1. Magalhaes, A.C.\n2. Franco, C.M.\n"),
                )
    run_list(expr_list, record)

def test_select():
    """Test select"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("e1:=1,select e1 case 1:v70[e1], case 2:mstname, case 3:v24, endsel",  u'Magalhaes, A.C.'),
                 ("select nocc(v70) case 1:v26, case 2:if nocc(v24)=1 then v24 fi, case 3:v24, endsel",  u'Techniques for the measurement of transpiration of individual plants'),
                 ("select s(v26^a) case 'Paris':'Found!', case 'Unesco':v26^b, case '-1965':v26^c, endsel",  u'Found!'),
                 ("select nocc(v10) case 1:'One occurence', case 2:'Two occurence', elsecase 'No occurence!', endsel",  u'No occurence!'),
                 ("select mfn case 2:'Two', case 3:'three', elsecase e1:=0,while e1<6 (if nocc(v70)=e1 then lw(20),v24,/ else f(e1,1,1),/ fi,e1:=e1+1), endsel",
                 "0.0\n1.0\nTechniques for the \nmeasurement of \ntranspiration of \nindividual plants\n3.0\n4.0\n5.0\n"),
                )
    run_list(expr_list, record)

def test_proc():
    """Test proc a, h and d"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("proc('d91','a91#Simple Field#'),v91", u'Simple Field'),
                 ("proc('d93','h93 20 Fixed size text'),v93",  u'Fixed size text     '),
                 ("proc('d92','d93','a93#content field 93#'),v93", 'content field 93'),
                 ("proc('h92 10 ^aaaaaa^bbbbbb^cccccc'),v92",u'^aaaaaa^bbbbbb^cccccc'),
                 ("proc('d92','d93','d91')",''),
                 )
    run_list(expr_list, record)

def test_proc_gsplit():
    """Test proc gsplit"""
    record = MasterRecord()
    record.v1 = 'Perez, J.; Garcia, Maria; Machado, A.'
    expr_list = (("proc('gsplit=1=;'),v1", u'Perez, J. Garcia, Maria Machado, A.'),
                 ("proc('Gsplit=1=;'),v1", u'Perez, J. Garcia, Maria Machado, A.'),
                 )
    run_list(expr_list, record)

def test_proc_gizmo():
    """Test proc gizmo"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    test_db = join('fixtures','test')
    expr_list = (("proc('G%s,24'),v24" % test_db, u'Techniques for the measurement of xxx of individual yyys'),
                 ("proc('G%s,69'),v69" % test_db, u'Paper on: <yyy physiology><yyy xxx><measurement and instruments>'),
                 )
    run_list(expr_list, record)

def test_break():
    """Test break"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("(f(iocc,1,0),'=',v70,break),",  u'1=Magalhaes, A.C.'),
                 ("(v70,ref(mfn,break))",'Magalhaes, A.C.'),
                 ("(if iocc=1 and p(v70) then '+ occ'/,break else v26^a|-|,v26^b,/, fi,)",'+ occ\n'),
                 ("(if iocc=2 and p(v70) then '+ occ'/,break else v26^a|-|,v26^b,/, fi,)",'Paris-Unesco\n+ occ\n'),
                )
    run_list(expr_list, record)

def test_continue():
    """Test continue"""
    mf = MasterFile(join("..","sample","cds.mst"))
    record = mf[1]
    expr_list = (("(f(iocc,1,0),'=',v70';',continue),",  u'1=Magalhaes, A.C.;2=Franco, C.M.;3=;'),
                 ("(if iocc=1 then v24 else continue fi)","Techniques for the measurement of transpiration of individual plants"),
                 ("(if iocc=1 then continue else v24 fi)",""),
                 ("(if iocc=1 and p(v70) then v70,continue fi)","Magalhaes, A.C."),
                 ("(if iocc=2 and p(v70) then v70,continue fi)","Franco, C.M."),
                )
    run_list(expr_list, record)

def test_ref_l_trivial_syntax():
    """Test ref and lookup trivial syntax"""
    
    mf = MasterFile(join("fixtures","MAIL.mst"))
    for ext in ('.idx','.idx.index','.idx.lock','.idx.old','.idx.tmp'):
        fname = join("fixtures","MAIL"+ext)
        if exists(fname):
            remove(fname)
    mf.invertdb()

    record = mf[1]
    expr_list = (("ref->MAIL(mfn,v690)",  u'BIREME'),
                 ("ref->MAIL(2,v840)", u'3061-7455 / 3061-7266'),
                 ("l->MAIL('BR1323.1')", u'11'),
                 ("ref->MAIL(l->MAIL('BR1323.1'),v820)",  u'Porto Alegre'),
                 ("ref->MAIL(l->MAIL(v805),v840)",  u'5576-9835 / 5576-9846/ 5576-9800 / 5576-9839 (Scad) / 5576-9832 (Lilacs) / \n5576-9852 (Secs) / 5576-9854 (Online)'),
                )
    run_list(expr_list, record)

    

#def test_repeatable_groups2():
#    """Continue to test repetable groups - related fields """
#    mf = MasterFile(join("..","sample","cds.mst"))
#    rec = mf[1]
#    rec.v10 = ["Bedford and Associates","Van Allen Inc.","Michigan University"]
#    rec.v20 = ["Junior Programmer", "Systems programmer", "Lecturer in Computer Sciences"]
#    expr_list = (('"EMPLOYMENT HISTORY"/d10,(v10(4,4)/v20(8,8)/#)',''),
#                 )
#    run_list(expr_list, rec)


if __name__ == "__main__":
    test_include()
