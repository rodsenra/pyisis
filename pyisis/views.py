# -*- coding: utf-8 -*-

"""
Auxiliary routines for displaying and formatting data.
"""
__updated__ = "2007-02-15"
__created__ = "2007-01-25"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

def list_all(master_file):
    """Dump all records at once to the standard output stream.
    """
    output_encoding = master_file.config.OUTPUT_ENCODING
    for rec in master_file:
        print "mfn=%6s"%rec.mfn
        for f in rec.get_fields():
            data = unicode(f.data).encode(output_encoding)
            print '%4d  "%s"'%(f.tag, data)

def dump_xml(master_file):
    """Dump all records as a XML file
    """
    for rec in master_file:
        print '<rec mfn="%d">'%rec.mfn
        try:
            for f in rec.get_fields():
                data = unicode(f.data).encode(master_file.config.OUTPUT_ENCODING)
                print "<t%s>%s</t%s>"%(f.tag, data, f.tag)
        except KeyError:
            pass
        print "</rec>"


def browse(master_file, pause=True):
    """Show all records. If pause == True (default)
    wait for <enter> between showing the next record.
    """
    for rec in master_file:
        print "mfn=%6s"%rec.mfn
        for f in rec.get_fields():
            data = unicode(f.data).encode(master_file.config.OUTPUT_ENCODING)
            print '%4d  "%s"'%(f.tag, data)
        if pause:
            raw_input("..")


def buffer2hex(buffer):
    """ Convert buffer into list of
    pairs (relative position, 'byte in hex')"""
    sz = len(buffer)
    byte_list = unpack('<%dB'%sz, buffer)
    result = [" %02X "%i for i in byte_list]
    return list(enumerate(result))
