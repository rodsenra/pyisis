# Python Character Mapping Codec gunilc
# -*- coding': utf-8 -*-
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
        name='gunilc',
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
    u'\u0041': u'\u0061',  # A -> a
    u'\u0042': u'\u0062',  # B -> b
    u'\u0043': u'\u0063',  # C -> c
    u'\u0044': u'\u0064',  # D -> d
    u'\u0045': u'\u0065',  # E -> e
    u'\u0046': u'\u0066',  # F -> f 
    u'\u0047': u'\u0067',  # G -> g
    u'\u0048': u'\u0068',  # H -> h
    u'\u0049': u'\u0069',  # I -> i
    u'\u004a': u'\u006a',  # J -> j
    u'\u004b': u'\u006b',  # K -> k
    u'\u004c': u'\u006c',  # L -> l
    u'\u004d': u'\u006d',  # M -> m
    u'\u004e': u'\u006e',  # N -> n
    u'\u004f': u'\u006f',  # O -> o
    u'\u0050': u'\u0070',  # P -> p
    u'\u0051': u'\u0071',  # Q -> q
    u'\u0052': u'\u0072',  # R -> r
    u'\u0053': u'\u0073',  # S -> s
    u'\u0054': u'\u0074',  # T -> t
    u'\u0055': u'\u0075',  # U -> u
    u'\u0056': u'\u0076',  # V -> v
    u'\u0057': u'\u0077',  # W -> w
    u'\u0058': u'\u0078',  # X -> x
    u'\u0059': u'\u0079',  # Y -> y
    u'\u005a': u'\u007a',  # Z -> z
    u'\u00c7': u'\u0063',  # C cedilha maiusculo -> c minusculo
    u'\u00fc': u'\u0075',  # u minusculo com trema -> u minusculo
    u'\u00e9': u'\u0065',  # e minusculo com acento agudo -> e minusculo
    u'\u00e2': u'\u0061',  # a minusculo com acento circunflexo -> a minusculo
    u'\u00e4': u'\u0061',  # a minusculo com trema -> a minusculo
    u'\u00e0': u'\u0061',  # a minusculo com acento grave -> a minusculo
    u'\u00e5': u'\u0061',  # a minusculo com anel -> a minusculo
    u'\u00e7': u'\u0063',  # c cedilha minusculo -> c minusculo
    u'\u00ea': u'\u0065',  # e minusculo com acento circunflexo -> e minusculo
    u'\u00eb': u'\u0065',  # e minusculo com trema -> e minusculo
    u'\u00e8': u'\u0065',  # e minusculo com acento grave -> e minusculo
    u'\u00ef': u'\u0069',  # i minusculo com trema -> i minusculo
    u'\u00ee': u'\u0069',  # i minusculo com acento circunflexo -> i minusculo
    u'\u00ec': u'\u0069',  # i minusculo com acento grave -> i minusculo
    u'\u00c4': u'\u0061',  # A maiusculo com trema -> a minusculo
    u'\u00c5': u'\u0061',  # A maiusculo com anel -> a minusculo
    u'\u00c9': u'\u0065',  # E maiusculo com acento agudo -> e minusuclo
    u'\u00e6': u'\u0065',  # ae minusculo -> e minusculo
    u'\u00c6': u'\u0065',  # AE maiusculo -> e minusculo
    u'\u00f4': u'\u006f',  # o minusculo com acento circunflexo -> o minusculo
    u'\u00f6': u'\u006f',  # o minusculo com trema -> o minusculo
    u'\u00f2': u'\u006f',  # o minusculo com acento grave -> o minusculo
    u'\u00fb': u'\u0075',  # u minusculo com acento circunflexo -> u minusculo
    u'\u00f9': u'\u0075',  # u minusculo com acento grave -> u minusculo
    u'\u00ff': u'\u0079',  # y minusculo com trema -> y minusculo
    u'\u00d6': u'\u006f',  # O maiusculo com trema -> o minusculo
    u'\u00dc': u'\u0075',  # U maiusculo com trema -> u minusculo
    u'\u00e1': u'\u0061',  # a minusculo com acento agudo -> a minusculo
    u'\u00ed': u'\u0069',  # i minusculo com acento agudo -> i minusculo
    u'\u00f3': u'\u006f',  # o minusculo com acento agudo -> o minusculo
    u'\u00fa': u'\u0075',  # u minusculo com acento agudo -> u minusculo
    u'\u00f1': u'\u006e',  # n minusculo com til -> n minusculo
    u'\u00d1': u'\u006e',  # N maiusculo com til -> n minusculo

}
