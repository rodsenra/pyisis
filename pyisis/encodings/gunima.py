# Python Character Mapping Codec gunima
# -*- coding: utf-8 -*-
import codecs

class Codec(codecs.Codec):
    
    def encode(self,input,errors='strict'):
        try:
            result = ""
            count = 0
            for i in input:
                try:
                    result += encoding_map[i]
                except:
                    result += i
                count += 1
            return (result,count)
        except:
            return (input,1)


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
        name='gunima',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )

def dump():
    for k,v in encoding_map.items():
        print k,v

encoding_map = {
    u'\u0061': u'\u0041',  #  -> A
    u'\u0062': u'\u0042',  #  -> B
    u'\u0063': u'\u0043',  #  -> C
    u'\u0064': u'\u0044',  #  -> D
    u'\u0065': u'\u0045',  #  -> E
    u'\u0066': u'\u0046',  #  -> F
    u'\u0067': u'\u0047',  #  -> G
    u'\u0068': u'\u0048',  #  -> H
    u'\u0069': u'\u0049',  #  -> I
    u'\u006a': u'\u004a',  #  -> J
    u'\u006b': u'\u004b',  #  -> K
    u'\u006c': u'\u004c',  #  -> L
    u'\u006d': u'\u004d',  #  -> M
    u'\u006e': u'\u004e',  #  -> N
    u'\u006f': u'\u004f',  #  -> O
    u'\u0070': u'\u0050',  #  -> P
    u'\u0071': u'\u0051',  #  -> Q
    u'\u0072': u'\u0052',  #  -> R
    u'\u0073': u'\u0053',  #  -> S
    u'\u0074': u'\u0054',  #  -> T
    u'\u0075': u'\u0055',  #  -> U
    u'\u0076': u'\u0056',  #  -> V
    u'\u0077': u'\u0057',  #  -> W
    u'\u0078': u'\u0058',  #  -> X
    u'\u0079': u'\u0059',  #  -> Y
    u'\u007a': u'\u005a',  #  -> Z 
    u'\u00fc': u'\u00dc',  #  -> U trema
    u'\u00e9': u'\u00c9',  #  -> E agudo
    u'\u00e2': u'\u00c2',  #  -> A circ
    u'\u00e4': u'\u00c4',  #  -> A trema
    u'\u00e0': u'\u00c0',  #  -> A grave
    u'\u00e5': u'\u00c5',  #  -> A anel
    u'\u00e7': u'\u00c7',  #  -> C cedilha
    u'\u00ea': u'\u00ca',  #  -> E circ
    u'\u00eb': u'\u00cb',  #  -> E trema
    u'\u00e8': u'\u00c8',  #  -> E grave
    u'\u00ef': u'\u00cf',  #  -> I trema
    u'\u00ee': u'\u00ce',  #  -> I circ
    u'\u00ec': u'\u00cc',  #  -> I grave
    u'\u00e6': u'\u00c6',  #  -> AE
    u'\u00f4': u'\u00d4',  #  -> O circ
    u'\u00f6': u'\u00d6',  #  -> O trema 
    u'\u00f2': u'\u00d2',  #  -> O grave
    u'\u00fb': u'\u00db',  #  -> U circ
    u'\u00f9': u'\u00d9',  #  -> U grave
    u'\u00e1': u'\u00c1',  #  -> A agudo
    u'\u00ed': u'\u00cd',  #  -> I agudo 
    u'\u00f3': u'\u00d3',  #  -> O agudo
    u'\u00fa': u'\u00da',  #  -> U agudo
    u'\u0144': u'\u0143',  #  -> N agudo 
    u'\u00fd': u'\u00dd',  #  -> Y agudo
}
