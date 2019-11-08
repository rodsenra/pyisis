# -*- coding: utf-8 -*-

"""
File to test MasterFile manipulation
"""

__created__ = "2007-12-19"
__updated__ = "2008-04-30"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

from os.path import join, exists
from os import remove, stat, chmod
from stat import ST_SIZE, S_IRUSR, S_IRGRP, S_IROTH, S_IWRITE
import tempfile

from pyisis.files import Collection, MasterFile
from pyisis.records import MasterRecord, ACTIVE, LOGICALLY_DELETED

# Setup test environment
from pyisis.tests.config_tests import test_data, Lyer, initialize
config = initialize()

# Setup test directory
tmpdir = tempfile.gettempdir()
#tmpdir = "/tmp"
testmst = join(tmpdir, "test.mst")
testxrf = join(tmpdir, "test.xrf")

def clean_start():
    """remove any existing files"""
    if exists(testmst):
        chmod(testmst, S_IWRITE)
        remove(testmst)
    if exists(testxrf):
        chmod(testxrf, S_IWRITE)
        remove(testxrf)

def test_new_collection():
    """Create a collection with a single master file inside"""
    c = Collection('demo',[testmst])

def test_master():
    """Open the sample masterfile and check if it has 150 records inside"""
    mf = MasterFile(join("..","sample","cds.mst"))
    assert len(mf)==150, "Sample database shows unexpected size"

def test_type_check():
    """Check type of sample.cds database"""
    mf = MasterFile(join("..","sample","cds.mst"))
    assert type(mf)==MasterFile

def test_empty_master():
    """Create an empty MasterFile"""
    clean_start()
    mf = MasterFile(testmst)
    del mf # force flush
    assert stat(testmst)[ST_SIZE]==512
    assert stat(testxrf)[ST_SIZE]==512

def test_singlerecord_master():
    """Create a MasterFile with a single record inside"""
    clean_start()
    mf = MasterFile(testmst)
    rec = MasterRecord()
    rec.update(test_data)
    rec.save(mf)
    del mf # force flush

def test_readonly_master():
    """Attempt to open a read-only master file.
    First try read+append mode, if it fails fallback
    to readonly mode.
    """
    test_singlerecord_master()
    # transform file to readonly
    chmod(testmst, S_IRUSR or S_IRGPR or S_IROTH)
    # try to open it again
    mf = MasterFile(testmst)
    del mf


def test_delete_record():
    """Create 3 records and delete the one in the middle"""
    clean_start()
    size = 3
    mf = MasterFile(testmst)
    for i in range(size):
        rec = MasterRecord()
        rec.update(test_data)
        rec.update({131:"flag %d"%i})
        rec.save(mf)
    mf.delete(2)
    #assert mf[2].status == 1, "master record not flagged as deleted"
    #assert mf.xrf[2].status == 'logically deleted', "xrf record not flagged as delted"

def test_write_multiple_records():
    """Write multiple records in a newly created database."""
    clean_start()
    size = 381
    mf = MasterFile(testmst)
    for i in range(size):
        rec = MasterRecord()
        rec.update(test_data)
        rec.save(mf)
    mf.commit()
    assert len(mf)==size
    assert mf[90].v50.data=='Incl. bibl.'
    del mf

def test_copy():
    """Copy the sample database to a new file"""
    clean_start()
    input_mf = MasterFile(join("..","sample","cds.mst"))
    output_mf = MasterFile(testmst)
    for rec in input_mf:
        rec.save(output_mf)
    output_mf.commit()
    assert len(input_mf)==len(output_mf)

def test_delete():
    """Create a record and delete it"""
    clean_start()
    mf = MasterFile(testmst)
    r = MasterRecord()
    r.update(test_data)
    r.save(mf)
    mf.commit()
    assert r.status == ACTIVE
    assert mf.xrf[1].status == 'active'
    assert len(mf)==1
    r = mf[1]
    mf.delete(1)
    mf.commit()
    r = mf[1]
    assert r.status == LOGICALLY_DELETED
    assert mf.xrf[1].status == 'logically deleted'
    assert len(mf)==0

def test_undelete():
    """Create a record and undelete it"""
    clean_start()
    mf = MasterFile(testmst)
    r = MasterRecord()
    r.update(test_data)
    r.save(mf)
    mf.delete(1)
    mf.commit()
    r = mf[1]
    assert r.status == LOGICALLY_DELETED
    assert mf.xrf[1].status == 'logically deleted'
    assert len(mf)==0
    mf.undelete(1)
    r = mf[1]
    assert r.status == ACTIVE
    assert mf.xrf[1].status == 'active'
    assert len(mf)==1

def test_update():
    """Create a record, modify it and save it and check previous"""
    clean_start()
    mf = MasterFile(testmst)
    r = MasterRecord()
    r.update(test_data)
    r.save(mf)
    r[90]="This is a new field"
    r.save(mf)
    prev = mf.previous(r)
    assert prev is not None
    assert len(prev)+1==len(r)

def test_restore_previous():
    """Create a record, modify it, save it and restore previous version"""
    clean_start()
    mf = MasterFile(testmst)
    r = MasterRecord()
    r.update(test_data)
    r.save(mf)
    r[90]="This is a new field"
    r.save(mf)
    prev = mf.previous(r)
    prev.save(mf)
    old_r = mf[1]
    try:
        old_r[90]
        assert False,"Field with tag 90 should not exist anymore."
    except KeyError:
        pass
    assert r.status==ACTIVE
    assert len(old_r)==len(prev)

def test_fdt():
    """Access fields using FDT file"""
    mf = MasterFile(join("..","sample","cds.mst"))
    assert len(mf.fdt)!=0
    assert len(mf.fdt)==39
    assert mf.fdt_field_names == ['Conference main entry', 'Title', 'Edition', 'Imprint', 'Collation', 'Series', 'Notes', 'Keywords', 'Personal', 'Corporate', 'Meetings', 'Added Title', 'Other language titles']
    assert mf.fdt_field_tags ==  [12, 24, 25, 26, 30, 44, 50, 69, 70, 71, 72, 74, 76]
    assert mf[1]['Title']==mf[1][24]

def test_update_flags():
    """Test update flags (xrf and master files)"""

    xref_fd = join('fixtures','testflag.xrf')
    db_fd = join('fixtures','testflag.mst')

    if exists(xref_fd):
        remove(xref_fd)
    if exists(db_fd):
        remove(db_fd)

    dbtest = MasterFile(db_fd)
    rec = MasterRecord()
    rec.update(test_data)
    rec.save(dbtest)

    xrf_rec = dbtest.xrf[1]
    assert xrf_rec.status   == 'active'
    assert xrf_rec.status   == 'active'
    assert xrf_rec.new_flag == True
    assert xrf_rec.modified_flag == False

    rec = dbtest[1]
    rec[27] = 'Test new field'
    rec.save(dbtest)

    assert xrf_rec.new_flag == False
    assert xrf_rec.modified_flag == True

    dbtest.invertdb(expr='70 0 MHU,(V70/)')

    assert xrf_rec.new_flag == False
    assert xrf_rec.modified_flag == False


if __name__=="__main__":
    test_write_multiple_records()



#import unittest
#class TestMasterFile(unittest.TestCase):
#    def setUp(self):
#        self.mf = MasterFile(join("..","sample","cds.mst"))
#
#    def tearDown(self):
#        self.mf = None
#
#    def test_size(self):
#        assert len(self.mf)==150, "Sample database shows unexpected size"
