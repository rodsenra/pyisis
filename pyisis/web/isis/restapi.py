# -*- coding: utf-8 -*-
"""
This module implements views for dynamically generated pages.
"""
__created__ = "2007-07-29"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers

import os
import xml.etree.ElementTree as xml_parser
from StringIO import StringIO

from pyisis.django_restapi.resource import Resource
from pyisis.files import MasterFile
from pyisis.records import MasterRecord, MasterField, MasterContainerField
from pyisis.engine import Engine
from pyisis.web.isis.utils import *
import pyisis.config


XML_HEADER     = '''<?xml version="1.0" encoding="%s"?>\n'''
XML_EMPTY      = '<result></result>'
XML_ERROR      = '%s' % ( XML_HEADER  % 'utf-8') + '<result>**ERROR: %s</result>' 
XML_OK         = '%s<result>OK</result>' % ( XML_HEADER  % 'utf-8')
XML_RECDELETED = '<result mfn="%d">DELETED</result>'
XML_DBADELETED = '<result database="%s">DELETED</result>'
XML_CREATEOK   = '<result mfn="%d">OK</result>'


def get_xml_parameters(request):
    """Fill class with XML parameters from request body"""
    try:
        xml_opts = XMLOptions()
        parms = xml_parser.fromstring(request.raw_post_data)
    
        for parm in parms.getiterator():
            setattr(xml_opts,  parm.tag, parm.text)
    
        xml_opts.prepare()
    
        return xml_opts
    except:
        raise Exception(XML_PARSER_ERROR)

    
def get_form_parameters(request):
    """Fill class with FORM parameters from request GET method"""
    try:
        form_opts = XMLOptions()
        for tag, value in request.GET.items():
            setattr(form_opts,  tag, value)
    
        form_opts.prepare()
    
        return form_opts
    except:
        raise Exception(FORM_PARSE_ERROR)
    

def get_database_info(request,silent_dbnotfound=0):
    """Returns collection, database and index from url
    """    
    path_list = request.META['REQUEST_URI'].split('/')
    restapi_index = path_list.index('restapi')
    colname = path_list[restapi_index + 1]
    dbname  = path_list[restapi_index + 2]
    try:
        recno  = int(path_list[restapi_index + 3])
    except:
        recno  = None
        
    collection = get_collection(colname)
    database = get_database(collection,dbname,silent_dbnotfound)        
    
    return (colname,dbname,collection,database,recno)
    


class IsisCollectionReST(Resource):
    """Support to REST operations"""

    def create_update_record(self, request, database, mstrecord, recno):
        """Create or update record
        """        
        xmlparams = xml_parser.fromstring(request.raw_post_data)

        field_list = xmlparams.findall('field')
       
        for field in field_list:
            occurrence = []
            fieldno = int(field.attrib['tag'])
            occ_list = field.findall('occ')

            for occ in occ_list:
                content = ''
                subfield_list = occ.findall('subfield')
                
                for subfield in subfield_list:
                    tag = subfield.attrib['tag'] 
                    if tag == "": 
                        content += subfield.text
                    else:
                        content += '^%s%s'%(tag, subfield.text)
                occurrence.append( MasterField(fieldno, content) )

            if len(occurrence) > 1:
                mstrecord[fieldno] = occurrence
            else:
                mstrecord[fieldno] = occurrence[0]
            
        mstrecord.save(database)
        return HttpResponse(XML_HEADER % 'utf-8' + XML_CREATEOK % recno)     
        

    def create(self, request):
        """Method to create database or record
        """
        try:
            
            try:
                colname,dbname,collection,database,index = get_database_info(request)
            except DatabaseNotFound:
                
                colname,dbname,collection,database,index = get_database_info(request,1)                
                dbname = get_xml_parameters(request).database

                if not dbname:
                    raise Exception(DB_NAME_ERROR)
                
                try:
                    newdb = collection[dbname]
                except:
                    pass
                else:
                    raise Exception(DB_ALREADY_EXISTS)
                
                newdb = MasterFile(os.path.join(collection.path_list[0], '%s.mst'%dbname))
                collection.databases[dbname] = newdb
                return HttpResponse(XML_OK)

            else:
                recno = database.nxtmfn
                mstrecord = MasterRecord(recno)
                return self.create_update_record(request, database, mstrecord, recno)
            
        except Exception, e:
            return HttpResponse(XML_ERROR % 'CREATE (%s)' % str(e))
    

    def read(self, request):
        """Method to get records from database
        """
        try:
            
            colname,dbname,collection,database,recno = get_database_info(request)

            options = get_form_parameters(request)    
            records = database[options.start:options.end]
            
            if options.reverse:
                records.reverse()
            
            result = StringIO()
            for field in records:
                result.write(field.to_xml())

            result = result.getvalue() or XML_EMPTY
            
            result = XML_HEADER % database.config.OUTPUT_ENCODING + result
            #FIXME: apply gizmo only data    
            return HttpResponse(result.encode(options.gizmo))
        
        except Exception, e:
            return HttpResponse(XML_ERROR % str(e))
        


    def update(self, request):
        """Method to update database record
        """
        try:
            colname,dbname,collection,database,recno = get_database_info(request)

            if recno:
                return self.create_update_record(request, database, database[recno], recno)
            else:
                raise Exception(MFN_INVALID)
            
        except Exception, e:
            return HttpResponse(XML_ERROR % str(e))            


    def delete(self, request):
        """Method to delete database or record
        """
        try:
            colname,dbname,collection,database,recno = get_database_info(request)

            if recno:
                database.delete(recno)
                return HttpResponse(XML_HEADER % 'utf-8' + XML_RECDELETED % recno)
            
            else:
                dbfiles = [os.path.join(database.basepath,'%s%s'%(database.name,ext))
                           for ext in ('.mst','.xrf')]
                
                for dbfile in dbfiles:
                    if os.path.exists(dbfile):
                        os.remove(dbfile)
                try:
                    del Engine.collection[colname].databases[dbname]
                except:
                    pass
                
                return HttpResponse(XML_HEADER % 'utf-8' + XML_DBADELETED % dbname)
                        
        except Exception, e:
            return HttpResponse(XML_ERROR % str(e))


def restclient(request):
    return render_to_response('restapi.html',
                              {'title': 'ISIS NBP - REST',},
                                context_instance=RequestContext(request))

