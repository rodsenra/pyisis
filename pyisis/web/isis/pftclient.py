# -*- coding: utf-8 -*-
"""
This module implements views for dynamically generated pages.
"""
__created__ = "2008-09-09"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers

import os
from StringIO import StringIO

from pyisis.files import MasterFile
from pyisis.records import MasterRecord, MasterField, MasterContainerField
from pyisis.engine import Engine
from pyisis.session import format
from pyisis.web.isis.utils import *
import pyisis.config


def pftclient(request):
    """Returns pft client page"""
    try:
        collections = Engine.collection.keys()
        return render_to_response('pftclient.html',
                                 {'collections': collections },
                                 context_instance=RequestContext(request))
        
    except:
        raise Exception(_("Error pftclient access"))


def pftget_databases(request):
    """Returns database list for collection"""
    response = HttpResponse()        
    try:
        collection = Engine.collection.get(request.POST['collection'])
        databases = collection.databases.keys()
        databases = [db.split('.')[0] for db in databases]
        response.status_code = 200
        result = ""
        for db in databases:
            result += '<option value="%s">%s</option>\n'%(db,db)
        response.write(result)
    except:
        response.status_code = 500
        response.write(_('Error getting databases'))    
    return response


def pftfunction(request):
    """Returns record formated by form expression"""
    response = HttpResponse()        
    try:
        #import pdb; pdb.set_trace()
        collection = Engine.collection.get(request.POST['collection'])
        database = collection[request.POST['database']]
        record = database[int(request.POST['record'])]
        result = format(request.POST['pft'],record)
        response.status_code = 200
        response.write('<pre>'+result+'</pre>')
    except Exception, e:
        response.status_code = 500
        response.write('Error: %s' % str(e))    
    return response
    

