# -*- coding: utf-8 -*-

"""
List the contents of an Isis Master File
"""
__created__ = "2007-05-15"
__updated__ = "2008-05-15"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

import sys
import gc
from datetime import  datetime
from pyisis.files import MasterFile
from pyisis.config import Config

def dump_rec(rec, dump, encoding):
    if dump:
        print "mfn=%6s"%rec.mfn
    for f in rec.get_fields():
        data = unicode(f.data).encode(encoding)
        if dump:
            print '%4d  "%s"'%(f.tag, data)

def read_loop(master, dump=True):
    # Loop through the records
    encoding = master.config.OUTPUT_ENCODING
    for rec in master:
        dump_rec(rec, dump, encoding)

def main():

    # override config
    config = Config()

    # Parse command-line parameters
    master = sys.argv[1]

    try:
        dump = eval(sys.argv[2])
    except IndexError:
        dump = True

    try:
        config.INPUT_ENCODING = sys.argv[3]
    except IndexError:
        config.INPUT_ENCODING = 'cp850'

    try:
        config.OUTPUT_ENCODING = sys.argv[4]
    except IndexError:
        config.OUTPUT_ENCODING = 'utf-8'


    # Open database
    mf = MasterFile(master, config=config)

    begin = datetime.now()
    gc.disable()
    read_loop(mf, dump)
    print _("Elapsed time:"), datetime.now()-begin
    gc.enable()


def profile():
    def inspected():
        main()
        return [1,2]
    import hotshot, hotshot.stats
    prof = hotshot.Profile("main")
    benchtime, stones = prof.runcall(inspected)
    print benchtime, stones
    prof.close()
    s = hotshot.stats.load("main")
    s.sort_stats("cumulative").print_stats()

if __name__=="__main__":
    #profile()
    main()