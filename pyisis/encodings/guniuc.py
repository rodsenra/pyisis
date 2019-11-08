    # Python Character Mapping Codec guniuc
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
        name='guniuc',
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
    u'\u0061': u'\u0041',  # a -> A
    u'\u0062': u'\u0042',  # b -> B
    u'\u0063': u'\u0043',  # c -> C
    u'\u0064': u'\u0044',  # d -> D
    u'\u0065': u'\u0045',  # e -> E
    u'\u0066': u'\u0046',  # f -> F
    u'\u0067': u'\u0047',  # g -> G
    u'\u0068': u'\u0048',  # h -> H
    u'\u0069': u'\u0049',  # i -> I
    u'\u006a': u'\u004a',  # j -> J
    u'\u006b': u'\u004b',  # k -> K
    u'\u006c': u'\u004c',  # l -> L
    u'\u006d': u'\u004d',  # m -> M
    u'\u006e': u'\u004e',  # n -> N
    u'\u006f': u'\u004f',  # o -> O
    u'\u0070': u'\u0050',  # p -> P
    u'\u0071': u'\u0051',  # q -> Q
    u'\u0072': u'\u0052',  # r -> R
    u'\u0073': u'\u0053',  # s -> S
    u'\u0074': u'\u0054',  # t -> T
    u'\u0075': u'\u0055',  # u -> U
    u'\u0076': u'\u0056',  # v -> V
    u'\u0077': u'\u0057',  # w -> W
    u'\u0078': u'\u0058',  # x -> X
    u'\u0079': u'\u0059',  # y -> Y
    u'\u007a': u'\u005a',  # z -> Z
    u'\u00c7': u'\u0043',  # C cedilha -> C maiusculo
    u'\u00fc': u'\u0055',  # u minusculo com trema -> U maiusculo
    u'\u00e9': u'\u0045',  # e minusculo com acento agudo -> E maiusculo
    u'\u00e2': u'\u0041',  # a minusculo com acento circunflexo -> A maiusculo
    u'\u00e4': u'\u0041',  # a minusculo com trema -> A maiusculo
    u'\u00e0': u'\u0041',  # a minusculo com acento grave -> A maiusculo
    u'\u00e5': u'\u0041',  # a minusculo com anel -> A maiusculo
    u'\u00e7': u'\u0043',  # c cedilha minusculo -> C maiusculo
    u'\u00ea': u'\u0045',  # e minusculo com acento circunflexo -> E maiusculo
    u'\u00eb': u'\u0045',  # e minusculo com trema -> E maiusculo
    u'\u00e8': u'\u0045',  # e minusculo com acento grave -> E maiusculo
    u'\u00ef': u'\u0049',  # i minusculo com trema -> I maiusculo
    u'\u00ee': u'\u0049',  # i minusculo com acento circunflexo -> I maiusculo
    u'\u00ec': u'\u0049',  # i minusculo com acento grave -> I maiusculo
    u'\u00c4': u'\u0041',  # A maiusculo com trema -> A maiusculo
    u'\u00c5': u'\u0041',  # A maiusculo com anel -> A maiusculo
    u'\u00c9': u'\u0045',  # E maiusculo com acento agudo -> E maiusculo
    u'\u00e6': u'\u0045',  # ae minusculo -> E maiusculo
    u'\u00c6': u'\u0045',  # AE maiusculo -> E maiusculo
    u'\u00f4': u'\u004f',  # o minusculo com acento circunflexo -> O maiusculo
    u'\u00f6': u'\u004f',  # o minusculo com trema -> O maiusculo
    u'\u00f2': u'\u004f',  # o minusculo com acento grave -> O maiusculo
    u'\u00fb': u'\u0055',  # u minusculo com acento circunflexo -> U maiusculo
    u'\u00f9': u'\u0055',  # u minusculo com acento grave -> U maiusculo
    u'\u00ff': u'\u0059',  # y minusculo com trema -> Y maiusculo
    u'\u00d6': u'\u004f',  # O maiusculo com trema -> O maiusculo
    u'\u00dc': u'\u0055',  # U maiusculo com trema -> U maiusculo
    u'\u00e1': u'\u0041',  # a minusculo com acento agudo -> A maiusculo
    u'\u00ed': u'\u0049',  # i minusculo com acento agudo -> I maiusculo
    u'\u00f3': u'\u004f',  # o minusculo com acento agudo -> O maiusculo
    u'\u00fa': u'\u0055',  # u minusculo com acento agudo -> U maiusculo
    u'\u00f1': u'\u004e',  # n minusculo com til -> N maiusculo
    u'\u00d1': u'\u004e',  # N maiusculo com til -> N maiusculo

}
