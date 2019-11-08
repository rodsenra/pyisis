# Python Character Mapping Codec gunimi
# -*- coding'utf-8 -*-
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
        name='gunimi',
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
    u'\u0041': u'\u0061',  #  -> a
    u'\u0042': u'\u0062',  #  -> b
    u'\u0043': u'\u0063',  #  -> c
    u'\u0044': u'\u0064',  #  -> d
    u'\u0045': u'\u0065',  #  -> e
    u'\u0046': u'\u0066',  #  -> f
    u'\u0047': u'\u0067',  #  -> g
    u'\u0048': u'\u0068',  #  -> h
    u'\u0049': u'\u0069',  #  -> i
    u'\u004a': u'\u006a',  #  -> j
    u'\u004b': u'\u006b',  #  -> k
    u'\u004c': u'\u006c',  #  -> l
    u'\u004d': u'\u006d',  #  -> m
    u'\u004e': u'\u006e',  #  -> n
    u'\u004f': u'\u006f',  #  -> o
    u'\u0050': u'\u0070',  #  -> p
    u'\u0051': u'\u0071',  #  -> q
    u'\u0052': u'\u0072',  #  -> r
    u'\u0053': u'\u0073',  #  -> s
    u'\u0054': u'\u0074',  #  -> t
    u'\u0055': u'\u0075',  #  -> u
    u'\u0056': u'\u0076',  #  -> v
    u'\u0057': u'\u0077',  #  -> x
    u'\u0058': u'\u0078',  #  -> y
    u'\u0059': u'\u0079',  #  -> w
    u'\u005a': u'\u007a',  #  -> z
    u'\u00c7': u'\u00e7',  #  -> c cedilha
    u'\u00c4': u'\u00e4',  #  -> a trema
    u'\u00c5': u'\u00e5',  #  -> a anel
    u'\u00c9': u'\u00e9',  #  -> e agudo
    u'\u00c6': u'\u00e6',  #  -> ae
    u'\u00d6': u'\u00f6',  #  -> o trema
    u'\u00dc': u'\u00fc',  #  -> u trema
    u'\u00d1': u'\u00f1',  #  -> n tils

}
