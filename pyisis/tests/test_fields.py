# -*- coding: utf-8 -*-

"""
File to test MasterField manipulation
"""

from __future__ import with_statement

__created__ = "2007-04-15"
__updated__ = "2008-04-30"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

# Setup test environment

from os.path import join
from pyisis.files import MasterFile
from pyisis.records import MasterRecord
from pyisis.fields import MasterField, MasterContainerField

# global setup
from pyisis.tests.config_tests import test_data, Lyer, initialize
config = initialize()

def test_empty_field():
    """Create an empty field just with a tag."""
    f = MasterField(1)
    assert f.tag==1, "Field tag is not set correctly."

def test_data_field():
    """Create a field with data and test its size."""
    f = MasterField(44, "Paper on: <plant physiology><plant transpiration>"+\
                        "<measurement and instruments>")
    assert len(f.data)==78, "Field data does not match expected size."

def test_xml():
    """Create a field and render as xml."""
    f = MasterField(44, "^aXML Text")
    assert f.to_xml() == '<field tag="44"><occ><subfield tag="a">XML Text</subfield></occ></field>' , "Error XML."

def test_access_subfield():
    """Create a field with subfields and try to access them."""
    f = MasterField(26, "^aParis^bUnesco^c-1965")
    assert f.a=="Paris", "Failed to access subfield a"
    assert f.b=="Unesco", "Failed to access subfield b"
    assert f.c=="-1965", "Failed to access subfield c"

def test_first_subfield():
    """Create a field with subfields and try to access first subfield ^* ."""
    f = MasterField(26, "^aParis^bUnesco^c-1965")
    f2 = MasterField(24, "Techniques for the measurement of transpiration of individual plants")
    assert f.a=="Paris", "Failed to access subfield a (f.a)"
    assert f["a"]=="Paris", "Failed to access subfield a (f['a'])"
    assert f["*"]=="Paris", "Failed to access first subfield (f['*'])"
    assert f2["*"]==f2.data, "Failed to compute v24^* == v24.data"

def test_valid_string_tag():
  """Create a field with a integer conversible string tag"""
  f = MasterField("50","Incl. bibl.")
  assert f.tag==50, "Failed to convert string tag into integer"

def test_invalid_string_tag():
  """Create a field with a string tag, should signal it as invalid"""
  try:
    f = MasterField("bla","valid data though")
  except ValueError:
    pass
  else:
    assert False, "Failed to raise exception with invalid tag type"

def test_mixed_field_subfield():
    """Test field values that have anonymous and explicit subfields"""
    mf = MasterFile(join("..","sample","cds.mst"))
    field = mf[27][76]
    assert field[""]==field.data.split("^")[0]
    assert field["z"] == field.z == "fre"
    

def test_key_error():
    """Invalid fields should raise KeyError"""
    class raises_keyerror:
        def __enter__(self):
            pass
        def __exit__(self, type, value, tb):
            print "type",type
            if type != KeyError:
                assert False, "Failed to raise expected KeyError exception"
            return True

    mf = MasterFile(join("..","sample","cds.mst"))
    r = mf[1]
    with raises_keyerror():
        r[1]
    with raises_keyerror():
        r["1"]
    with raises_keyerror():
        r.v1

def test_add_repeatable():
    """Test adding repeatable fields"""
    rec = MasterRecord()
    rec.v90 = ["Hello","Good-bye","^a123^bBelex"]
    assert rec.v90 == rec[90] == rec["90"]
    # Indexing begins from 1
    assert rec.v90[1].data == "Hello"
    assert rec.v90.tag == 90
    assert rec.v90[2].tag == 90
    assert type(rec.v90) == MasterContainerField
    assert rec.v90[3].a == '123'
    assert rec.v90[3].b == 'Belex'
    


if __name__=="__main__":
    #import pdb; pdb.set_trace()
    test_key_error()

