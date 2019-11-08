# -*- coding: utf-8 -*-

"""
Handling of inverted files.
"""

__updated__ = "2008-09-25"
__created__ = "2008-09-26"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"

import os, sys
from struct import unpack, pack, calcsize

from ZODB import FileStorage, DB
from persistent.list import PersistentList
import transaction

from pyisis.files import PostIndex


N0X_DATALEN = {0:10, 1: 10, 2: 30}

class N0X:
    """N01 struct file"""
    def __init__(self, pos, ock, it):
        self.pos = pos #relative record number
        self.ock = ock #number of active keys
        self.it  = it  #type of B*tree
        self.info = {}

def read_l0x_records(fname, root, typef = 10, debug = False):
    """Reads posts"""
    progress = {0:'|',1:'/',2:'-',3:'\\'}
    filetype = {10: '.l01', 30: '.l02'}
    header_off_set = {10: 23, 30: 43}
    fd = open(fname+filetype[typef],'rb')

    fd.seek(header_off_set[typef])
    uwinlin = unpack('c',fd.read(1))
    winlin = uwinlin[0]=='\xbf'
    fd.seek(0)
    data = 1
    count = 0

    while data:
        data = fd.read(4)
        if not data:
            break
        pos = unpack('i',data)[0]
        ock = unpack('h',fd.read(2))[0]
        data = fd.read(2)
        it = unpack('h',data)[0]
        datalen = typef
        ps = unpack('i',fd.read(4))[0]

        for i in range(ock):

            data = fd.read(datalen)
            if len(data) < typef:
                break
            fkey = ''.join(unpack('c'*datalen,data))
            if winlin:
                myoffset = unpack('h',fd.read(2))
            block = unpack('i',fd.read(4))[0]
            if block == 0:
                break
            offset = unpack('i',fd.read(4))[0]
            try:
                mfn, tag, occ, cnt = read_ifp(fname, block, offset)
            except:
                print fname,block,offset
                continue
            key = fkey.strip().encode('utf-8')
            if debug:
                print 'Key:%s, MFN:%s, Tag:%s, Occ:%s, OffSet:%s'%(key,mfn,tag,occ,cnt)
            else:
                print '%s\r' % progress[count % 4],
                count += 1
            sys.stdout.flush()
            postdata = PostIndex(mfn, tag, occ, cnt, 0, tag)
            try:
                root[key].append(postdata)
            except KeyError:
                root[key] = PersistentList()
                root[key].append(postdata)

        transaction.commit()

    fd.close()

def read_l0x_key(fname,key):
    fd = open(fname+'.l01','rb')
    data = 1
    ifpblock = 0; ifpoffset = 0
    while data:
        data = fd.read(4)
        if not data:
            break
        pos = unpack('i',data)[0]
        ock = unpack('h',fd.read(2))[0]
        ock = 10 #FIXME why ock < 10 but empty offset???
        data = fd.read(2)
        it = unpack('h',data)[0]
        try:
            datalen = N0X_DATALEN[it]
        except:
            datalen = 10
        ps = unpack('i',fd.read(4))[0]

        for i in range(ock):
            data = fd.read(datalen)
            keydata = ''.join(unpack('c'*datalen,data))
            offset = unpack('h',fd.read(2))
            block = unpack('i',fd.read(4))[0]
            ifoffset = unpack('i',fd.read(4))[0]
            if key == keydata.strip():
                fd.close()
                return (block, ifoffset)

    fd.close()
    return (ifpblock,ifpoffset)


def read_ifp(fname, block, offset):
    """Reads ifp block"""
    fd = open(fname + '.ifp','rb')
    fd.seek(0)
    init_block_offset = (block - 1) * 512

    try:
        fd.seek(init_block_offset)
    except:
        print "Erro",block,init_block_offset
        os._exit(1)

    block_number = unpack('i',fd.read(4))[0]
    post_position = init_block_offset + 4 + (offset * 4)
    fd.seek(post_position)
    header = fd.read(20)
    raw = fd.read(8)
    m1,m2,tag,pocc,pcnt = unpack('>HBHBH',raw)
    mfn = (m1 << 16) | m2
    fd.close()
    return (mfn, tag, pocc, pcnt)


def search(dbname, key=''):
    key = key.upper()
    block,offset = read_l0x_key(dbname,key)
    if block and offset:
        print 'KEY: %s' % key, read_ifp(dbname, block, offset)
    else:
        print 'KEY: %s not found!' % key

def clean_old(fname):
    extlist = ['.idx','.idx.lock','.idx.index','.idx.tmp']
    for ext in extlist:
        try:
            os.remove(fname+ext)
        except:
            pass

def convert_files(fname,debug=False):
    try:
        clean_old(fname)

        storage = FileStorage.FileStorage(fname+".idx")
        db = DB(storage)
        connection = db.open()
        dbroot = connection.root()
        root = dbroot['isis']

        read_l0x_records(fname,root,10,debug)
        read_l0x_records(fname,root,30,debug)

        connection.close()
        db.pack()
        db.close()
        storage.close()

        print "\nInverted files from database %s converted to %s.idx\n" %(fname,fname)
    except Exception, e:
        print "\n** Error converting inverted file to database: %s (%s)\n" % (fname, str(e))


if __name__ == '__main__':
    #search(sys.argv[1],sys.argv[2])
    try:
        fname = sys.argv[1]
    except:
        print 'Use ifp2nbidx.py <filename>'
        os._exit(1)
    try:
        debug = sys.argv[2]
        debug = True
    except:
        debug = False


    convert_files(fname,debug=debug)