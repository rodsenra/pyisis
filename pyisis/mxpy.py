#!/usr/bin/python

from optparse import OptionParser
from os.path import exists, join, split
import sys, os, re
import gettext
import codecs
from pyisis import __version__, banner
import pyisis.config
import pyisis.files

include_pat = re.compile(r"@[\w\d\.\/]+")

class Session(object):
    def __init__(self, config):
        self.lexer = pyisis.lexer.PftLexer()
        self.parser = pyisis.parser.PftParser(lexer=self.lexer,
                                              debug=False,
                                              outputdir=config.PARSER_AUXFILES_DIR)
        self.compiler = pyisis.ast.PftCompiler()
        self.config = config


def normalize_path(filepath):
    """Assume .mst extension if missing"""
    filepath = filepath.strip()
    if '.' not in filepath:
       return filepath + ".mst"
    else:
       return filepath

def set_lang(config):
    localedir = join(config.basepath,'locale')
    gettext.install('pyisis',localedir=localedir)
    lang1 = gettext.translation('pyisis', languages=[config.LANGUAGE],localedir=localedir)
    lang1.install(unicode=1)


def load_codec_modules(encoding):

    try:
        mod = __import__('pyisis.encodings.' + encoding, globals(), locals(), '[*]')
    except ImportError:
        print "Erro importando codec"
        mod = None
    try:
        getregentry = mod.getregentry
        entry = getregentry()
    except:
        entry = None
    return entry


def main():
    codecs.register(load_codec_modules)
    set_lang(pyisis.config.config)
    parser = OptionParser(
             usage=banner,
             version="%prog "+__version__,
             description="Python-based ISIS-NBP Cell.")

    parser.add_option("-C", "--config",
                      action="store", type="string", dest="configfile",
                      help=_("Specify the path to the configuration file"))

    parser.add_option("-m", "--inputdb",
                      action="store", type="string", dest="inputdb",
                      help=_("Specify the path to the master file"))

    parser.add_option("-c", "--collection",
                      action="store", type="string", dest="collection",
                      help=_("Specify the collection"))

    parser.add_option("-d", "--database",
                      action="store", type="string", dest="database",
                      help=_("Specify database."))

    parser.add_option("-f", "--from",
                      action="store", type="string", dest="frecord",
                      help=_("Specify initial record."))

    parser.add_option("-t", "--to",
                      action="store", type="string", dest="trecord",
                      help=_("Specify last record."))

    parser.add_option("-e", "--expr",
                      action="store", dest="expr",
                      help=_("Formatting language expression"))
    
    parser.add_option("-v", "--ver",
                      action="store_true", dest="version",
                      help=_("Version"))
                    
    parser.add_option("-D", "--debug",
                      action="store_true", dest="debug",
                      help=_("Debug"))


    (options, args) = parser.parse_args()

    if options.version:
        print "Isis-NBP Cell version ",__version__
        print "Python", sys.version
        sys.exit(0)

    #import pdb; pdb.set_trace()
    config = pyisis.config.config
    if options.configfile:
        config.load(options.configfile)
    set_lang(config)

    debug           = False
    collection_name = 'current'
    database_name   = 'cds'
    frecord         = 1
    trecord         = 2

    if options.collection:
        collection_name = options.collection
        
    if options.database:
        database_name = options.database
        
    if options.frecord:
        frecord = int(options.frecord)

    if options.trecord:
        trecord = int(options.trecord) + 1

    if options.debug:
        debug = True

    if not options.expr:
        print 'Expression?'
        print 'Try "-h" for more information.'
        sys.exit(0)
    else:
        expr = options.expr

    session = Session(config)

    #try:
    #    import psyco
    #    psyco.full()
    #    #psyco.log(logfile='/tmp/profile.log')
    #    #psyco.profile()
    #except Exception, e:
    #    print "Psyco not found!", str(e)

    current_path = os.getcwd()
    collection = pyisis.files.IsisCollection(collection_name,[current_path],config=config)
    database = collection[database_name]
    format(session, expr, database, frecord, trecord, config)


def format(session, expr, database, inicio=1, fim=1, config=None, debug=False, stdout=1):
    """ Apply the formatting function resulting from the compilation
    of expression over the pair (mst,record).
    Every formatting function is saved in a cache to avoid recompilation
    in the future.
    """
    result = ''
    expr = expr.strip()
    current_path = os.getcwd()
    while 1:
        # loop needed to handle include inside include
        includes = include_pat.findall(expr)
        if not includes:
            # no include was found
            break
        for include in includes:
            filenamepath = include[1:]
            if exists(filenamepath):
                includefile = filenamepath
            else:
                includefile = join(split(current_path)[0], filenamepath)
            if exists(includefile):
                try:
                    expanded_include = open(includefile).read().strip()
                    expr = include_pat.sub(expanded_include, expr)
                except:
                    raise Exception (_('Include file error'))
            else:
                raise Exception (_('File %s not found' % includefile))

    ast = session.parser.parse(expr.decode(config.INPUT_ENCODING), debug=debug)
    chain = pyisis.ast.flatten(ast)
    formatter = session.compiler.compile_code(chain)
    mst = database
    for idx in range(inicio,fim): 
        outputdata = formatter(rec=database[idx], mst=mst, debug=0)
        outputdata = outputdata.encode(config.OUTPUT_ENCODING)
        if stdout:
            sys.stdout.write(outputdata)
        else:
            result += outputdata
    sys.stdout.flush()
    return result

if __name__ == '__main__':
    main()
