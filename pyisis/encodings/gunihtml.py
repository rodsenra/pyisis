# Python Character Mapping Codec gunihtml
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
                            char = decoding_map[tag]
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
            print 'erro'
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
        name='gunihtml',
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
    u'\u0022': '&quot;',  # &#34; -> 
    u'\u0026': '&amp;',  # &#38; -> 
    u'\u0027': '&apos;',  # &#39; -> 
    u'\u003c': '&lt;',  # &#60; -> 
    u'\u003e': '&gt;',  # &#62; -> 
    u'\u00c7': '&Ccedil;',  # &#199; -> 
    u'\u00fc': '&uuml;',  # &#252; -> 
    u'\u00e9': '&eacute;',  # &#233; -> 
    u'\u00e2': '&acirc;',  # &#226; -> 
    u'\u00e4': '&auml;',  # &#228; -> 
    u'\u00e0': '&agrave;',  # &#224; -> 
    u'\u00e5': '&aring;',  # &#229; -> 
    u'\u00e7': '&ccedil;',  # &#231; -> 
    u'\u00ea': '&ecirc;',  # &#234; -> 
    u'\u00eb': '&euml;',  # &#235; -> 
    u'\u00e8': '&egrave;',  # &#232; -> 
    u'\u00ef': '&iuml;',  # &#239; -> 
    u'\u00ee': '&icirc;',  # &#238; -> 
    u'\u00ec': '&igrave;',  # &#236; -> 
    u'\u00c4': '&Auml;',  # &#196; -> 
    u'\u00c5': '&Aring;',  # &#197; -> 
    u'\u00c9': '&Eacute;',  # &#201; -> 
    u'\u00e6': '&aelig;',  # &#230; -> 
    u'\u00c6': '&AElig;',  # &#198; -> 
    u'\u00f4': '&ocirc;',  # &#244; -> 
    u'\u00f6': '&ouml;',  # &#246; -> 
    u'\u00f2': '&ograve;',  # &#242; -> 
    u'\u00fb': '&ucirc;',  # &#251; -> 
    u'\u00f9': '&ugrave;',  # &#249; -> 
    u'\u00ff': '&yuml;',  # &#255; -> 
    u'\u00d6': '&Ouml;',  # &#214; -> 
    u'\u00dc': '&Uuml;',  # &#220; -> 
    u'\u00f8': '&oslash;',  # &#248; -> 
    u'\u00a3': '&pound;',  # &#163; -> 
    u'\u00d8': '&Oslash;',  # &#216; -> 
    u'\u00d7': '&times;',  # &#215; -> 
    u'\u00e1': '&aacute;',  # &#225; -> 
    u'\u00ed': '&iacute;',  # &#237; -> 
    u'\u00f3': '&oacute;',  # &#243; -> 
    u'\u00fa': '&uacute;',  # &#250; -> 
    u'\u00f1': '&ntilde;',  # &#241; -> 
    u'\u00d1': '&Ntilde;',  # &#209; -> 
    u'\u00aa': '&ordf;',  # &#170; -> 
    u'\u00b0': '&ordm;',  # &#186; -> 
    u'\u00bf': '&iquest;',  # &#191; -> 
    u'\u00ae': '&reg;',  # &#174; -> 
    u'\u00ac': '&not;',  # &#172; -> 
    u'\u00bd': '&frac12;',  # &#189; -> 
    u'\u00bc': '&frac14;',  # &#188; -> 
    u'\u00a1': '&iexcl;',  # &#161; -> 
    u'\u00ab': '&laquo;',  # &#171; -> 
    u'\u00bb': '&raquo;',  # &#187; -> 
    u'\u00df': '&szlig;',  # &#223; -> 
    u'\u00b5': '&micro;',  # &#181; -> 
    u'\u00b1': '&plusmn;',  # &#177; -> 
    u'\u00f7': '&divide;',  # &#247; -> 
    u'\u00ba': '&deg;',  # &#176; -> 
    u'\u00b7': '&middot;',  # &#183; -> 
    u'\u00b2': '&sup2;',  # &#178; -> 
}

decoding_map = {}

for code, tag in encoding_map.items():
    decoding_map[tag] = code


