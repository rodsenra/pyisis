# -*- coding: utf-8 -*-
"""
This module implements XML-RPC.
"""
__created__ = "2008-08-26"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"


import os
from StringIO import StringIO
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse

from pyisis.files import MasterFile
from pyisis.records import MasterRecord, MasterField, MasterContainerField
from pyisis.engine import Engine
import pyisis.config
from pyisis.web.isis.utils import *

# Create a Dispatcher; this handles the calls and translates info to function maps
dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)
dispatcher.register_introspection_functions()


def rpc_handler(request):
    """
    If post data is defined, it assumes it's XML-RPC and tries to process as such
    Empty post assumes you're viewing from a browser and tells you about the service.
    """
    response = HttpResponse()
    if len(request.POST):
        result = dispatcher._marshaled_dispatch(request.raw_post_data)
        response.write(result)        

    else:
        response.write("<b>This is an XML-RPC Service.</b><br>")
        response.write("You need to invoke it using an XML-RPC Client!<br>")
        response.write("The following methods are available:<ul>")
        methods = dispatcher.system_listMethods()

        for method in methods:
            if method.startswith('system'): continue
            #sig = dispatcher.system_methodSignature(method)
            # this just reads your docblock, so fill it in!
            help =  dispatcher.system_methodHelp(method).split('\n')[0]
            response.write("<li><b>%s</b>: %s" % (method, help))

        response.write("</ul>")
        response.write('<b>ISIS-NBP Server</b>')

    response['Content-length'] = str(len(response.content))
    return response


def get_database_info(params,silent_dbnotfound=0):
    """Get collection/database from parameters
    """
    try:
        dbname = params['database']
    except:
        raise Exception(DB_NAME_ERROR)

    try:    
        colname = params['collection']
    except:
        raise Exception(COLLECTION_NAME_ERROR)
    
    collection = get_collection(colname)
    database = get_database(collection,dbname,silent_dbnotfound)        
    
    return (colname, dbname, collection, database)


def get_xml_options(params):
    """Fill class with XML parameters from request body"""
    try:
        xml_opts = XMLOptions()
    
        for option in params.keys():
            if option in ('collection','database'): 
                continue
            setattr(xml_opts, option, params[option])
    
        xml_opts.prepare()
    
        return xml_opts
    except:
        raise Exception(_('XML Parse Error'))    


def createDB(params):
    """Create new database
<?xml version='1.0'?>
 <methodCall>
  <methodName>createDB</methodName>
   <params>
    <param>
     <value>
      <struct>
       <member>
        <name>collection</name>
        <value><string>sample</string></value>
       </member>
       <member>
        <name>database</name>
        <value><string>dbtest</string></value>
       </member>
      </struct>
    </value>
   </param>
  </params>
</methodCall>
"""
    try:
        try:
            colname, dbname, collection, database = get_database_info(params)
            raise Exception(DB_ALREADY_EXISTS)
        except  DatabaseNotFound:
            colname, dbname, collection, database = get_database_info(params,1)
        
            newdb = MasterFile(os.path.join(collection.path_list[0], '%s.mst'%dbname))
            collection.databases[dbname] = newdb
        
            return _('Database %s created' % dbname)
    
    except Exception, e:
        return _('** Create Database (%s)' % str(e) )


def deleteDB(params):
    """Delete database
<?xml version='1.0'?>
 <methodCall>
  <methodName>deleteDB</methodName>
   <params>
    <param>
     <value>
      <struct>
       <member>
        <name>collection</name>
        <value><string>sample</string></value>
       </member>
       <member>
        <name>database</name>
        <value><string>dbtest</string></value>
       </member>
      </struct>
     </value>
    </param>
  </params>
 </methodCall>
"""
    try:        
        colname, dbname, collection, database = get_database_info(params)

        dbfiles = [os.path.join(database.basepath,'%s%s'%(dbname,ext))
                   for ext in ('.mst','.xrf')]
        
        for dbfile in dbfiles:
            if os.path.exists(dbfile):
                os.remove(dbfile)
        try:
            del Engine.collection[colname].databases[dbname]
        except:
            pass
        
        return _("Database %s removed") % dbname
    
    except Exception, e:
        return _("** Delete Database (%s)") % str(e) 


def createRecord(params):
    """Create new record
<?xml version='1.0'?>
 <methodCall>
  <methodName>createRecord</methodName>
   <params>
    <param>
     <value>
      <struct>
       <member>
        <name>collection</name>
        <value><string>sample</string></value>
       </member>
       <member>
        <name>database</name>
        <value><string>dbtest</string></value>
       </member>
       <member>
        <name>26</name>
        <value><string>^aParis^bUnesco^c-1965</string></value>
       </member>
       <member>
        <name>30</name>
        <value><string>^ap. 211-224^billus.</string></value>
       </member>
       <member>
        <name>50</name>
        <value><string>Incl. bibl.</string></value>
       </member>
      </struct>
    </value>
   </param>
  </params>
 </methodCall>  
"""    
    try:        
        colname, dbname, collection, database = get_database_info(params)
        
        recno = database.nxtmfn
        mstrecord = MasterRecord(recno)
        for tag in params.keys():
            if tag in ('database','collection'): continue
            value = params[tag]
            if type(value) is list:
                mstfield = [MasterField(tag,valtag) for valtag in value]
            else:
                mstfield = MasterField(tag,value)
                
            mstrecord[tag] = mstfield
        
        mstrecord.save(database)

        return _("Record mfn=%s created") % recno
    
    except Exception, e:
        return _("** Create Record (%s)") % str(e) 


def updateRecord(params):
    """Update record
<?xml version='1.0'?>
 <methodCall>
  <methodName>updateRecord</methodName>
   <params>
    <param>
     <value>
      <struct>
       <member>
        <name>collection</name>
        <value><string>sample</string></value>
       </member>
       <member>
        <name>database</name>
        <value><string>dbtest</string></value>
       </member>
       <member>
        <name>mfn</name>
        <value><int>1</int></value>
       </member>
       <member>
        <name>26</name>
        <value><string>^aParis^bUnesco^c-1965</string></value>
       </member>
       <member>
        <name>30</name>
        <value><string>^ap. 211-224^billus.</string></value>
       </member>
       <member>
        <name>50</name>
        <value><string>Incl. bibl.</string></value>
       </member>
      </struct>
    </value>
   </param>
  </params>
 </methodCall>  
"""
    try:        
        colname, dbname, collection, database = get_database_info(params)
        mfn = int(params['mfn'])

        mstrecord = database[mfn]
        for tag in params.keys():
            if tag in ('database','collection','mfn'): continue
            value = params[tag]
            if type(value) is list:
                mstfield = [MasterField(tag,valtag) for valtag in value]
            else:
                mstfield = MasterField(tag,value)
            mstrecord[tag] = mstfield
        
        mstrecord.save(database)

        return _("Record mfn=%d updated") % mfn     
    except Exception, e:
        return _("** Update Record (%s)") % str(e) 


def deleteRecord(params):
    """Delete record
<?xml version='1.0'?>
 <methodCall>
  <methodName>deleteRecord</methodName>
   <params>
    <param>
     <value>
      <struct>
       <member>
        <name>collection</name>
        <value><string>sample</string></value>
       </member>
       <member>
        <name>database</name>
        <value><string>dbtest</string></value>
       </member>
       <member>
        <name>mfn</name>
        <value><int>2</int></value>
       </member>
      </struct>
     </value>
    </param>
   </params>
 </methodCall>
"""
    try:        
        colname, dbname, collection, database = get_database_info(params)
        database.delete(params['mfn']) 
                
        return _("Record mfn=%s deleted") % params['mfn']
    except Exception, e:
        return _("** Delete Record (%s)") % str(e) 



def readRecord(params):
    """Read record
<?xml version='1.0'?>
 <methodCall>
  <methodName>readRecord</methodName>
   <params>
    <param>
     <value>
      <struct>
       <member>
        <name>collection</name>
        <value><string>sample</string></value>
       </member>
       <member>
        <name>database</name>
        <value><string>dbtest</string></value>
       </member>
       <member>
        <name>from</name>
        <value><string>1</string></value>
       </member>
       <member>
        <name>to</name>
        <value><string>2</string></value>
       </member>
       <member>
        <name>count</name>
        <value><string>2</string></value>
       </member>
       <member>
        <name>gizmo</name>
        <value><string>gunima</string></value>
       </member>
       <member>
        <name>reverse</name>
        <value><string>on</string></value>
       </member>
      </struct>
     </value>
    </param>
   </params>
  </methodCall>
"""
    try:
        colname, dbname, collection, database = get_database_info(params)
        options = get_xml_options(params) 
        records = database[options.start:options.end]
        
        if options.reverse:
            records.reverse()
        
        result = StringIO()
        for field in records:
            result.write(field.to_xml())

        return result.getvalue().encode(options.gizmo)             
    
    except Exception, e:
        return _("** Read Record (%s)") % str(e) 



# you have to manually register all functions that are xml-rpc-able with the dispatcher
# the dispatcher then maps the args down.
# The first argument is the actual method, the second is what to call it from the XML-RPC side...
dispatcher.register_function(createDB, 'createDB')
dispatcher.register_function(deleteDB, 'deleteDB')
dispatcher.register_function(createRecord, 'createRecord')
dispatcher.register_function(updateRecord, 'updateRecord')
dispatcher.register_function(deleteRecord, 'deleteRecord')
dispatcher.register_function(readRecord, 'readRecord')
