# -*- coding: utf-8 -*-

"""
list keys of inverted files (isis).
"""

__updated__ = "2008-10-10"
__created__ = "2008-10-10"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"

import os, sys
from struct import unpack, pack, calcsize
from ifp2nbpidx import read_ifp

def read_l0x_records(fname,typef=10):
    filetype = {10: '.l01', 30: '.l02'}
    fd = open(fname+filetype[typef],'rb')
    data = 1
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
            keydata = ''.join(unpack('c'*datalen,data))
            print keydata, '(%d)' % typef
            myoffset = unpack('h',fd.read(2))
            block = unpack('i',fd.read(4))[0]
            if block == 0:
                break
            offset = unpack('i',fd.read(4))[0]
            try:
                mfn, tag = read_ifp(fname, block, offset)
                print '\t',mfn, tag
            except:
                print ''

    fd.close()

def read_n0x_records(fname,typef=10):
    filetype = {10: '.n01', 30: '.n02'}
    fd = open(fname+filetype[typef],'rb')
    data = 1
    while data:
        data = fd.read(4)
        if not data:
            break
        pos = unpack('i',data)[0]
        ock = unpack('h',fd.read(2))[0]
        ock = 10 #FIXME why ock < 10 but empty offset???
        data = fd.read(2)
        it = unpack('h',data)[0]
        #try:
        #    datalen = N0X_DATALEN[it]
        #except:
        datalen = typef
        #n0xdata[pos] = N0X(pos, ock, it)
        for i in range(ock):
            data = fd.read(datalen)
            if len(data) < typef:
                break

            keydata = ''.join(unpack('c'*datalen,data))
            offset = unpack('h',fd.read(2))
            data = fd.read(4)
            punt = unpack('i',data)[0]
            print keydata
            
    fd.close()



if __name__ == '__main__':
    #search(sys.argv[1],sys.argv[2])
    try:
        fname = sys.argv[1]
    except:
        print 'Use listkeys.py <database>'
        print '\tex.: listkeys.py cds'
        os._exit(1)
    read_n0x_records(fname,10)
    read_n0x_records(fname,30)
    read_l0x_records(fname,typef=10)
    read_l0x_records(fname,typef=30)
    