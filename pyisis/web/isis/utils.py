#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyisis.engine import Engine


XML_PARSE_ERROR       = _('XML Parse Error')
FORM_PARSE_ERROR      = _('Form Parse Error')
DB_NAME_ERROR         = _('Database name not specified!')
COLLECTION_NAME_ERROR = _('Collection name not specified!')
DB_ALREADY_EXISTS     = _('Database already exists!')
MFN_INVALID           = _('Invalid mfn!')



class DatabaseNotFound(Exception):

    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)
    


class XMLOptions:
    """This class maps XML tags from request body"""
    
    def __init__(self):
        self.parameters = None
        self.database   = None
        self.to         = None
        self.count      = None
        self.reverse    = None
        self.gizmo      = 'utf-8'
        self.end        = None
        self.start      = None

    def prepare(self):
        try:
            self.start = int(getattr(self,'from'))
        except:
            self.start = 1
        try:    
            self.end = int(self.to) + 1
        except:
            pass
        try:    
            self.end = self.start + int(self.count) 
        except:
            pass        
        
        self.reverse = self.reverse and self.reverse.upper() == 'ON'
        
        if not self.gizmo: 
            self.gizmo = 'utf-8'

    
def get_collection(collection_name):
    """Get collection object"""
    try:
        return Engine.collection.get(collection_name)
    except:
        raise Exception(_('Collection not found!'))
    

def get_database(collection, database_name,silent_dbnotfound=0):
    """Get database object
    """
    try:
        return collection[database_name]
    except:
        if silent_dbnotfound:
            return None
        else:
            raise DatabaseNotFound(_('Database not found!'))

