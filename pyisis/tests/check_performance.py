# -*- coding: utf-8 -*-

"""
File to test Isis performance
"""

__created__ = "2007-05-15"
__updated__ = "2008-05-15"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

# Setup test environment
from timeit import Timer
from pyisis.tests.config_tests import test_data, Lyer, initialize
config = initialize()

setup="""
from pyisis.files import MasterFile
from pyisis.views import list_all
from os.path import join
mf = MasterFile(join("..","sample","cds.mst"))
"""

def list_all():
    stmt = """
list_all(mf)
"""
    import sys
    stdout = sys.stdout
    sys.stdout = open("/dev/null","w")

    t = Timer(stmt=stmt, setup=setup)
    elapsed = t.timeit(number=4)/4

    sys.stdout.flush()
    sys.stdout = stdout
    print "list_all %.4f sec/pass" % (elapsed)

if __name__=="__main__":
    list_all()