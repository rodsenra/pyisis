# -*- coding: utf-8 -*-

"""
File to test MasterRecord and XrfRecord  manipulation
"""

__created__ = "2008-04-30"
__updated__ = "2008-04-30"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

from os.path import join
from pyisis.records import MasterRecord, XrfRecord
from pyisis.fields import MasterContainerField
from pyisis.tests.config_tests import Lyer

# Setup test environment
from pyisis.tests.config_tests import test_data, Lyer, initialize
config = initialize()

def test_record():
    """Create a MasterRecord, insert data and check it."""
    rec = MasterRecord()
    rec.update(test_data)
    for i in test_data:
        if type(test_data[i]) != list:
            assert rec[i].data==test_data[i]
        else:
            # repeatable fields
            assert rec[i].data==''.join([j for j in test_data[i]])

def test_record_status():
    """Build a MasterRecord with specific status"""
    for status in MasterRecord.str2status.keys():
        rec = MasterRecord(status=status)
        assert rec.status == MasterRecord.str2status[status]

def test_encoding():
    cfg = Lyer()
    cfg.INPUT_ENCODING = 'utf-8'
    cfg.OUTPUT_ENCODING = 'utf-8'
    r = MasterRecord(mfn=1, config=cfg, fields={42: u"Slavík"})
    assert repr(r.v42) == "MasterField(42, 'Slav\xc3\xadk')"
    assert str(r.v42) == 'Slav\xc3\xadk'
    assert r.v42.data == u'Slav\xedk'
    r.v1 = "água"
    r.v2 = "água".decode("utf-8")
    r.v3 = unicode("água","utf-8")
    assert r.v1.data == r.v2.data == r.v3.data, "Failed to add encoded data to record"


def test_sorting_fields():
    """Check if fields from a record are sorted according to their tags."""
    r = MasterRecord()
    r.update(test_data)
    s1 = list(sorted(r.get_tags()))
    s2 = [f.tag for f in sorted(r)]
    # use set to avoid repeated tags for repeatable fields in s2
    assert set(s1)==set(s2)

def test_conversion_xrf_new():
    """Test the conversion routines of XrfRecords for new record"""
    EXTRA_LARGE = 0
    NEW_RECORD = True
    MODIFIED_RECORD = False
    xrf = XrfRecord(1, 3480, EXTRA_LARGE)
    assert xrf.block == 1
    assert xrf.offset == 408
    assert xrf.status == 'active'
    assert xrf.encode() == 3480
    assert xrf.decode(3480, EXTRA_LARGE) == (1, 408, NEW_RECORD, MODIFIED_RECORD)

def test_conversion_xrf_deleted():
    """Test the conversion routines of XrfRecords for deleted record"""
    EXTRA_LARGE = 0
    NEW_RECORD = True
    MODIFIED_RECORD = False
    xrf = XrfRecord(1, -616, EXTRA_LARGE)
    assert xrf.block == 0
    assert xrf.offset == 104
    assert xrf.status == 'invalid'
    assert xrf.decode(-616, EXTRA_LARGE) == (0, 104, NEW_RECORD, MODIFIED_RECORD)
    assert xrf.encode() == 1128


def test_field_lengths():
    """Verify consistency of field lengths"""
    rec = MasterRecord()
    rec.v90 = ["Hello","Good-bye"]
    rec[80] = "Belex"
    assert len(rec[80])==1
    assert len(rec[80].data)==5
    assert len(rec[90])==2
    # ISIS indexing begins from 1 (not 0)
    # zero index must return MasterField with empty String
    assert rec[90][0].data==''
    assert len(rec[90][1].data)==5
    assert rec[90][2].data==u'Good-bye'

def test_repeatable_subfields():
    """Verify access to repeatable subfields"""
    rec = MasterRecord()
    rec.v90 = "^a123^a456^bBelex^cGreat"
    assert type(rec.v90.a)==list
    assert len(rec.v90.a)==2
    assert rec.v90.a[0]=="123"
    assert rec.v90.a[1]=="456"
    assert type(rec.v90.b) == unicode
    assert rec.v90.b=="Belex"

def test_subfield_delimiter():
    cfg = Lyer()
    cfg.SUBFIELD_DELIMITER = "$"
    cfg.INPUT_ENCODING = "utf-8"
    cfg.OUTPUT_ENCODING = "utf-8"
    rec = MasterRecord(config=cfg)
    rec.v90 = "$a123$a456$bBelex$cGreat"
    assert type(rec.v90.a)==list
    assert len(rec.v90.a)==2
    assert rec.v90.a[0]=="123"
    assert rec.v90.a[1]=="456"
    assert type(rec.v90.b) == unicode
    assert rec.v90.b=="Belex"

def test_record_update():
    """Populate record from dict"""
    rec = MasterRecord()
    rec.update({"10":"a", "20":"b", "30":["c","d"]})
    assert rec.v10.data == "a"
    assert rec[20].data == "b"
    assert type(rec.v30) == MasterContainerField
    assert rec.v30[0].data == ""
    assert rec.v30[1].data == "c"
    assert rec.v30[2].data == "d"


if __name__=="__main__":
    #import pdb; pdb.set_trace()
    pass
