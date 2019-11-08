# Python Character Mapping Codec gunina
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
        name='gunina',
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
    u'\u00c7': u'\u0043',  #  C cedilha -> C  
    u'\u00fc': u'\u0075',  #  u trema -> u
    u'\u00e9': u'\u0065',  #  e agudo -> e 
    u'\u00e2': u'\u0061',  #  a circu -> a 
    u'\u00c4': u'\u0061',  #  a trema -> a 
    u'\u00e0': u'\u0061',  #  a grave -> a 
    u'\u00e5': u'\u0061',  #  a bola -> a 
    u'\u00e7': u'\u0063',  #  c cedilha -> c 
    u'\u00ea': u'\u0065',  #  e circu -> e 
    u'\u00eb': u'\u0065',  #  e trema -> e
    u'\u00e8': u'\u0065',  #  e grave -> e
    u'\u00ef': u'\u0069',  #  i trema -> i 
    u'\u00ee': u'\u0069',  #  i circu -> i 
    u'\u00ed': u'\u0069',  #  i grave -> i 
    u'\u00c4': u'\u0041',  #  A trema -> A
    u'\u00c5': u'\u0041',  #  A bola -> A 
    u'\u00c9': u'\u0045',  #  E agudo -> E 
    u'\u00f4': u'\u006f',  #  o circu -> o 
    u'\u00f6': u'\u006f',  #  o trema -> o 
    u'\u00f2': u'\u006f',  #  o grave -> o
    u'\u00fb': u'\u0075',  #  u circu -> u
    u'\u00f9': u'\u0075',  #  u grave -> u
    u'\u00ff': u'\u0079',  #  y trema -> y
    u'\u00d6': u'\u004f',  #  O trema -> O 
    u'\u00dc': u'\u0055',  #  U trema -> U 
    u'\u00e1': u'\u0061',  #  a agudo -> a 
    u'\u00ed': u'\u0069',  #  i agudo -> i 
    u'\u00f3': u'\u006f',  #  o agudo -> o
    u'\u00fa': u'\u0075',  #  u agudo -> u 
    u'\u00f1': u'\u006e',  #  n til -> n
    u'\u00d1': u'\u004e',  #  N til -> N 

}

