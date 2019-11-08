#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib,sys

DEBUG = 0
IPADDR= '127.0.0.1'
PORT  = 8000

BODY_READ ='''<?xml version="1.0" encoding="utf-8"?>
<parameters>
   <gizmo></gizmo>
   <from></from>
   <to></to>
   <count></count>
   <reverse>on</reverse>
</parameters>
'''

BODY_CREATE_DB ='''<?xml version="1.0" encoding="utf-8"?>
<parameters> 
   <database>newdatabase</database> 
</parameters> 
'''

BODY_CREATE_REG ='''<?xml version="1.0" encoding="utf-8"?>
<record>
  <field tag="1"> 
   <occ>
     <subfield tag="">field1 campo1</subfield>
   </occ> 
   <occ>
     <subfield tag="">field1 campo2</subfield>
   </occ> 
  </field> 
  <field tag="2"> 
   <occ>
     <subfield tag="">field 2</subfield>
   </occ> 
  </field> 
  <field tag="3"> 
   <occ>
     <subfield tag="a">subcampo a</subfield>
     <subfield tag="b">subcampo b</subfield>
     <subfield tag="c">subcampo c</subfield>
     <subfield tag="d">subcampo d</subfield>
   </occ> 
  </field> 
</record>
'''

BODY_UPDATE_REG ='''<?xml version="1.0" encoding="utf-8"?>
<record>
  <field tag="1"> 
   <occ>
     <subfield tag="">field1 campo1 trocado</subfield>
   </occ> 
   <occ>
     <subfield tag="">field1 campo2 trocado</subfield>
   </occ> 
  </field> 
  <field tag="2"> 
   <occ>
     <subfield tag="">field 2 trocado</subfield>
   </occ> 
  </field> 
</record>
'''

BODY_READ_CDS ='''<?xml version="1.0" encoding="utf-8"?>
<parameters>
   <gizmo></gizmo>
   <from>1</from>
   <to>2</to>
   <count></count>
   <reverse>on</reverse>
</parameters>
'''

def rest_Create(conn):
    conn.request('POST','/web/restapi/sample/',BODY_CREATE_DB)
    result = con.getresponse()
    print result.read()
    
    
def rest_Create_REG(conn):
    conn.request('POST','/web/restapi/sample/newdatabase/',BODY_CREATE_REG)
    result = con.getresponse()
    print result.read()


def rest_Delete(conn):
    conn.request('DELETE','/web/restapi/sample/newdatabase/1/')
    result = con.getresponse()
    print result.read()


def rest_Delete_DB(conn):
    conn.request('DELETE','/web/restapi/sample/newdatabase/')
    result = con.getresponse()
    print result.read()


def rest_Update(conn):
    conn.request('PUT','/web/restapi/sample/newdatabase/1/',BODY_UPDATE_REG)
    result = con.getresponse()
    print result.read()


def rest_Read(conn):
    conn.request('GET','/web/restapi/sample/newdatabase/',BODY_READ)
    result = con.getresponse()
    text = result.read()
    print text
    try:
        open('/tmp/teste.xml','w').write(text)
    except:
        pass

def rest_Read_CDS(conn):
    conn.request('GET','/web/restapi/sample/cds/',BODY_READ_CDS)
    result = con.getresponse()
    text = result.read()
    print text
    try:
        open('/tmp/teste.xml','w').write(text)
    except:
        pass


if __name__ == '__main__':
    con = httplib.HTTPConnection(IPADDR,PORT)
    con.set_debuglevel(DEBUG)
    
    print '\n'+'-'*10,' DELETE DB ','-'*10; rest_Delete_DB(con)    
    
    print '\n'+'-'*10,'CREATE DB','-'*10; rest_Create(con)
    
    print '\n'+'-'*10,'CREATE REG','-'*10; rest_Create_REG(con)
    
    print '\n'+'-'*10,' READ ','-'*10; rest_Read(con)
    
    print '\n'+'-'*10,' UPDATE ','-'*10; rest_Update(con)
    
    print '\n'+'-'*10,' DELETE RECORD ','-'*10; rest_Delete(con)
    
    print '\n'+'-'*10,' READ ','-'*10; rest_Read(con)
    
    print '\n'+'-'*10,' DELETE DB ','-'*10; rest_Delete_DB(con)    
    
    #print '\n'+'-'*10,' READ ','-'*10; rest_Read_CDS(con)

    con.close()

