# -*- coding: utf-8 -*-
"""
This module implements tests to XML-RPC.
"""
__created__ = "2008-08-28"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"

import sys
import xmlrpclib

IPADDR= 'localhost'
PORT  = 8000

dbname = sys.argv[1]

rpc_srv = xmlrpclib.ServerProxy("http://%s:%d/web/xmlrpc/"%(IPADDR,PORT),verbose=False)

params = {'collection':'sample','database':dbname}
print '\n'+'-'*10,' DELETE DB ','-'*10;print rpc_srv.deleteDB(params)
print '\n'+'-'*10,' CREATE DB ','-'*10;print rpc_srv.createDB(params)

params['24'] = 'Techniques for the measurement of transpiration of individual plants'
params['26'] = '^aParis^bUnesco^c-1965'
params['30'] = '^ap. 211-224^billus.'
params['44'] = 'Methodology of plant eco-physiology: proceedings of the Montpellier Symposium'
params['50'] = 'Incl. bibl.'
params['69'] = 'Paper on: <plant physiology><plant transpiration><measurement and instruments>'
params['70'] = ('Magalhaes, A.C.','Franco, C.M.')
print '\n'+'-'*10,' CREATE RECORD 1 ','-'*10;print rpc_srv.createRecord(params)
print '\n'+'-'*10,' CREATE RECORD 2 ','-'*10;print rpc_srv.createRecord(params)

params['24'] = 'xxxTechniques for the measurement of transpiration of individual plants'
params['26'] = 'xxx^aParis^bUnesco^c-1965'
params['30'] = 'xxx^ap. 211-224^billus.'
params['44'] = 'xxxMethodology of plant eco-physiology: proceedings of the Montpellier Symposium'
params['50'] = 'xxxIncl. bibl.'
params['69'] = 'xxxPaper on: <plant physiology><plant transpiration><measurement and instruments>'
params['70'] = 'xxxMagalhaes, A.C.'
params['mfn'] = 1
print '\n'+'-'*10,' UPDATE RECORD 1 ','-'*10;print rpc_srv.updateRecord(params)

params = {'collection': 'sample','database': dbname,'mfn': 2}
print '\n'+'-'*10,' DELETE RECORD 2 ','-'*10;print rpc_srv.deleteRecord(params)

params = {'collection': 'sample'}
for k,v in [('database',dbname),('from','1'),('to','1'),('count','2'),
            ('gizmo','gunima'),('reverse','on')]:
    params[k] = v
    print '\n'+'-'*10,' READ RECORD %s,%s'%(k,v),'-'*10;
    print rpc_srv.readRecord(params)
    print

print '\nIntrospection'
print "-"*40
methods = rpc_srv.system.listMethods()
#print methods
for method in methods:
    if method.startswith('system'): continue
    print rpc_srv.system.methodHelp(method)+'\n'
