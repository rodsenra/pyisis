# -*- coding: utf-8 -*-

"""
Convert gizmo id file to python codec module
"""
__created__ = "2007-07-23"
__updated__ = "2008-07-23"
__author__  = "Joao Chaves <joaochaves@gpr.com.br>"


ENCODE_LINE_TEMPLATE = "    %s: %s,  # %s -> %s\n"
DECODE_LINE_TEMPLATE = "    %s,  # %s\n"
TEST_LINE_TEMPLATE   = "    ('%s','%s',%s,'%s -> %s'),\n"
DECODING_TABLE       = "decoding_table = (\n"
END_TEMPLATE         = {True: '\n})\n', False: '\n}\n', None: '\n)\n'}
ENCODE_CMD_TEMPLATE  = {
    True: '''
        try:
            amp = -1
            count = 0
            charmaps = []
            for i in input:
                if i == '&':
                    amp = count
                if i == ';':
                    if amp > -1:
                        tag = input[amp:count+1]
                        try:
                            char = encoding_map[tag]
                            charmaps.append((char,amp,count))
                            amp = -1
                        except:
                            pass
                count += 1

            result = ''
            last_position = 0
            for char,index,sz in charmaps:
                result += input[last_position:index]
                result += char
                last_position = sz + 1
            result += input[last_position:]

            return (result,len(result))
        except:
            return (input,1)
    ''',

    False:'''
        try:
            result = ""
            count = 0
            for i in input:
                try:
                    carac, sz = codecs.charmap_encode(i,errors,encoding_map)
                    result += carac
                    count += sz
                except:
                    result += i
                    count += 1
            return (result,count)
        except:
            return (input,1)
'''
                        }

MOD_TEMPLATE = """# Python Character Mapping Codec %s
# -*- coding: utf-8 -*-
import codecs

class Codec(codecs.Codec):
    def encode(self,input,errors='strict'):
        %s

    def decode(self,input,errors='strict'):
        pass

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        pass

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        pass

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

def getregentry():
    return codecs.CodecInfo(
        name='%s',
        encode=Codec().encode,
        decode=Codec().encode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )

encoding_map = {
"""

MOD_TEMPLATE_UTF = """# Python Character Mapping Codec %s
# -*- coding: utf-8 -*-
import codecs

class Codec(codecs.Codec):
    def encode(self,input,errors='strict'):
        %s

    def decode(self,input,errors='strict'):
        try:
            utf8,flag = codecs.charmap_decode(input,errors,decoding_table)
            utf8 = utf8.encode('utf-8')
            return (utf8,flag)
        except:
            return (input,1)

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        pass

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        pass

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

def getregentry():
    return codecs.CodecInfo(
        name='%s',
        encode=Codec().decode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )

decoding_map = codecs.make_identity_dict(range(256))
decoding_map.update({
"""


TEST_START_TEMPLATE = """#!/usr/bin/python
# -*- coding: utf-8 -*-

encode_str = '%s'

source = [
"""

TEST_END_TEMPLATE = """
]

def load_codec_module(encoding):

    try:
        mod = __import__('%s', globals(), locals(), '[*]')
    except ImportError:
        print "Erro importando codec"
        os._exist(0)

    getregentry = mod.getregentry
    entry = getregentry()
    return entry


if __name__ == '__main__':

    import os, codecs

    codecs.register(load_codec_module)

    for (origem,dest,resultado,comentario) in source:
        try:
            print origem, dest, resultado.encode(encode_str), "#", comentario
        except Exception,e :
            print "*** %%s %%s %%s (%%s)" %%( origem, dest, comentario, e)
            os._exit(0)
"""

BODY_TMPL = {True: MOD_TEMPLATE_UTF, False: MOD_TEMPLATE }


import os
import sys


class Gizmo:
    """Mapeia os campos do arquivo gizmo ID para classe"""
    def __init__(self):
        self.v001 = ''
        self.v002 = ''
        self.v011 = ''
        self.v021 = ''
        self.v041 = ''
        self.v050 = ''
        self.v051 = ''
        self.v052 = ''
        self.v059 = ''

    def is_v1_html(self):
        """Verifica se v001 e tag html"""
        return len(self.v001) > 2 and self.v001[0] == '&' and self.v001[-1] == ';'

    def getv1(self):
        return self.get_valor(self.v001,self.v011)

    def getv2(self):
        return self.get_valor(self.v002,self.v021)

    def get_valor(self,valor,tipo):
        """Formata valor conforme tipo"""
        if tipo == 'hex':
            return '0x%s' % valor
        elif tipo == 'asc':
            return '0x%x' % (int(valor))
        else:
            return "'%s'" % valor

    def getv1_as_string(self):
        return self.get_valor_as_string(self.v001,self.v011)

    def getv2_as_string(self):
        return self.get_valor_as_string(self.v002,self.v021)

    def get_valor_as_string(self,valor,tipo):
        """Formata valor conforme tipo para script de teste"""

        if tipo == 'hex':
            return "u'\u%s'" % valor
        elif tipo == 'asc':
            return "'%s'" % hex(int(valor)).replace('0x','\\x')
        else:
            return "'%s'" % valor

    def getv1_unicode(self):
        return self.get_unicode(self.v001)

    def getv2_unicode(self):
        return self.get_unicode(self.v002)

    def get_unicode(self,valor):
        if len(valor) == '2':
            return "'\\x%s'" % valor
        else:
            return "u'\\u%s'" % valor


def load(lines):
    """Monta e devolve lista com gizmos"""

    lista_gizmo = []
    giz = None
    for line in lines:
        line = line.strip()
        if not line: continue

        if line.startswith('!ID'):
            if giz:
                lista_gizmo.append(giz)
            giz = Gizmo()
            continue

        try:
            v,tag,valor = line.split('!')
        except:
            print "Erro processando linha:%s" % line
            os._exit(0)

        try:
            setattr(giz,tag,valor)
        except Exception, e:
            print "Erro adicionando atributo (tag:%s,valor:%s) (%s)" % (tag,valor,e)
            os._exit(0)
    if giz:
        lista_gizmo.append(giz)
    return lista_gizmo


def geraGizmoPy(fname):
    try:
        lines = open(fname).readlines()
    except:
        print "Erro lendo arquivo: %s" % fname
        os._exit(0)

    giz_name = os.path.split(fname)[1].split('.')[0]
    gizmos = load(lines)

    if gizmos:
        gtest = gizmos[0]
        TO_UTF = (gtest.v021 == 'hex')
        FROM_HTML = gtest.is_v1_html()

        fdout = open('%s.py' % giz_name,'w')

        if TO_UTF:
            UTF_LIST = {}
            for i in range(256):
                UTF_LIST[i] = None

        try:
            body = BODY_TMPL[TO_UTF]%(giz_name,ENCODE_CMD_TEMPLATE[FROM_HTML],giz_name)
        except:
            body = BODY_TMPL[TO_UTF]%(giz_name,'pass',giz_name)
        fdout.write(body)

        fdtest = open('%s_test.py' % giz_name,'w')
        fdtest.write(TEST_START_TEMPLATE % giz_name)

        print "Gerando:", giz_name, "tamanho:", len(gizmos)

        for g in gizmos:
            texto1 = unicode(g.v051,'cp1252').encode('cp1252')
            texto2 = unicode(g.v052,'cp1252').encode('cp1252')

            if g.is_v1_html():
                fdout.write(ENCODE_LINE_TEMPLATE % (g.getv1(),g.getv2_as_string(),texto1,texto2))
            else:
                fdout.write(ENCODE_LINE_TEMPLATE % (g.getv1(),g.getv2(),texto1,texto2))

            fdtest.write(TEST_LINE_TEMPLATE % (g.v001,g.v002,g.getv1_as_string(),texto1,texto2))

            if TO_UTF:
                UTF_LIST[int(g.v001)] = (g.getv2_unicode(),texto2)

        fdout.write(END_TEMPLATE[TO_UTF])

        if TO_UTF:
            fdout.write(DECODING_TABLE)
            for i in range(256):
                try:
                    valor, texto = UTF_LIST[i]
                except:
                    valor = None; texto = "None"
                fdout.write(DECODE_LINE_TEMPLATE % (valor, texto))
            fdout.write(END_TEMPLATE[None])

        fdout.close()

        fdtest.write(TEST_END_TEMPLATE % (giz_name))
        fdtest.close()


def printHelp():
    print "\nAbre arquivos de definicao gizmo (.id) e cria"
    print "arquivo equivalente no formato python (.py)"
    print "\nUtilize: convert_gizmo.py <dir>"
    print "Onde <dir> e' o caminho dos arquivos .id\n"
    os._exit(0)

if __name__ == '__main__':

    import glob

    try:
        dirname = sys.argv[1]
    except:
        printHelp()

    if not os.path.exists(dirname):
        print "Diretório não existe"
        printHelp()

    arquivos = glob.glob(os.path.join(dirname,'*.id'))

    for arquivo in arquivos:
        geraGizmoPy(arquivo)
