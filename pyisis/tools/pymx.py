# -*- coding: utf-8 -*-

"""
This is an interactive CDS/ISIS based tool to
manipulate ISIS database files.
"""

__updated__ = "2007-11-22"
__created__ = "2007-02-14"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

from optparse import OptionParser
import sys
import logging
from logging import FileHandler
from os.path import exists,join
import gettext

import codecs, glob, os

import pyisis.config
from pyisis import __version__, banner
from pyisis.files import IsisCollection, MasterFile
from pyisis.records import ACTIVE
from pyisis.views import browse, list_all, dump_xml
from pyisis.engine import interactive, Engine
from pyisis import gateway


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

    #config = pyisis.config.config
    #encodingdir = join(config.basepath,'encodings')
    #import pdb; pdb.set_trace()
    #modlist = glob.glob(os.path.join(encodingdir,'g*.py'))
    #for modname in modlist:
    #modname = os.path.split(modname)[1].split('.')[0]
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

    parser.add_option("-f", "--config",
                      action="store", type="string", dest="configfile",
                      help=_("Specify the path to the configuration file"))

    parser.add_option("-m", "--inputdb",
                      action="store", type="string", dest="inputdb",
                      help=_("Specify the path to the master file"))

    parser.add_option("-o", "--outputdb",
                      action="store", type="string", dest="outputdb",
                      help=_("Specify the path to the output master file"))

    parser.add_option("-s", "--server",
                      action="store_true",   dest="server",
                      help=_("Start in server mode."))

    parser.add_option("-b", "--browse",
                      action="store_true",  dest="browse",
                      help=_("Browse the the master file interactively"))

    parser.add_option("-l", "--list",
                      action="store_true",  dest="list",
                      help=_("List the contents of the master file"))

    parser.add_option("-p", "--profile",
                      action="store_true",  dest="profile",
                      help=_("Profile the execution of --list option"))

    parser.add_option("-x", "--xml-dump",
                      action="store_true",  dest="xml",
                      help=_("Convert master file contents to XML"))

    parser.add_option("-i", "--interactive",
                      action="store_true",  dest="interactive",
                      help=_("Interactive mode of operation"))

    parser.add_option("-V",
                    action="store_true",  dest="version",
                    help=_("Prints current version"))

    parser.add_option("-c", "--control",
                      action="store_true", dest="control",
                      help=_("Dumps the control record"))

    parser.add_option("--copy",
                      action="store_true", dest="copy",
                      help=_("Copy inputdb into outputdb"))

    (options, args) = parser.parse_args()

    config = pyisis.config.config
    if options.configfile:
        config.load(options.configfile)
    set_lang(config)

    # Initialize engine
    Engine.setup(config)

    # Setup logging
    logger = logging.getLogger('pyisis')
    logger.propagate = False
    logger.setLevel(config.LOG_LEVEL)
    handler = FileHandler(filename=config.LOG_PATH)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger.addHandler(handler)
    logger.info("Isis-NBP Cell version " + __version__)


    if options.version:
        print "Isis-NBP Cell version ",__version__
        print "Python", sys.version
        sys.exit(0)

    if options.server:
        gateway.run(Engine)

    # Setup master file objects
    mf = None
    if options.inputdb:
        input_filepath = normalize_path(options.inputdb)
        if not exists(input_filepath):
            print _("File %s does not exist or is inaccessible.") % input_filepath
            sys.exit(0)
        mf = MasterFile(input_filepath, config=config)

    if options.outputdb:
        output_filepath = normalize_path(options.outputdb)
        dest_mf = MasterFile(output_filepath, config=config)


    # dump control record
    if options.control:
        
        if not mf:
            print _('Use -m or --inputdb to set input database.')
            sys.exit(0)
            
        template_header = "%10s %10s %10s %2s %10s %10s %10s %10s"
        template_values = "%10d %10d %10d %2d %10d %10d %10d %10d"
        print template_header%('nxtmfn', 'nxtmfb', 'nxtmfp', 't',
                               'reccnt', 'mfcxx1', 'mfcxx2', 'mfcxx3')
        print template_values%(mf.nxtmfn, mf.nxtmfb, mf.nxtmfp, mf.mftype,
                               mf.reccnt, mf.mfcxx1, mf.mfcxx1, mf.mfcxx1)
        print

    if options.browse:
        if not mf:
            print _('Use -m or --inputdb to set input database.')
            sys.exit(0)
        browse(mf)

    if options.list:
        if not mf:
            print _('Use -m or --inputdb to set input database.')
            sys.exit(0)
        list_all(mf)

    if options.xml:
        if not mf:
            print _('Use -m or --inputdb to set input database.')
            sys.exit(0)
        
        dump_xml(mf)

    if options.copy:
        # Check dependencies
        if not options.inputdb:
            print _("Use -m or --inputdb to set input database.")
            sys.exit(0)
        if not options.outputdb:
            print _("Use -o or --outputdb to set output database.")
            sys.exit(0)
        # do copy
        for rec in mf:
            if rec.status==ACTIVE:
                rec.save(dest_mf)


    if options.interactive:
        if options.inputdb and input_filepath:
            Engine.collection[options.inputdb] = IsisCollection(options.inputdb,
                                                                input_filepath)
        interactive(Engine.collection)

    if options.profile:
        if not options.inputdb:
            print _("Use -m or --inputdb to set input database.")
            sys.exit(0)
        
        def inspected():
            list_all(mf)
            return [1,2]

        import hotshot, hotshot.stats
        prof = hotshot.Profile("listall")
        benchtime, stones = prof.runcall(inspected)
        print benchtime, stones
        prof.close()
        s = hotshot.stats.load("listall")
        s.sort_stats("cumulative").print_stats()

if __name__ == '__main__':
    main()
