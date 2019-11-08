# -*- coding: utf-8 -*-
"""
This module implements the Cell´ s Gateway
Handling of URL Gateway service interface.
"""
__updated__ = "2008-05-08"
__created__ = "2007-11-22"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

from twisted.internet import reactor, defer
from twisted.application import app, service, strports
from twisted.python.runtime import platformType
from twisted.scripts import twistd


from glob import glob
from os.path import join, basename
import os
import re
import sys
from copy import deepcopy

from pyisis import banner, __version__
from pyisis.engine import Engine

# TODO
#caching headers in actionlets
#context.setHeader('Cache-Control', 'no-cache')
#context.setHeader('Pragma', 'no-cache')
#context.setHeader('Expires', '0')


def run(engine):
    "Gateway´s Runloop"
    config = engine.config

    #os.environ['DJANGO_SETTINGS_MODULE'] = 'pyisis.web.settings'
    # needed to use django templates
    if config.HTTP_PORT:
        from twisted.web2 import server, vhost, channel
        from twisted.web2 import wsgi, log
        from django.core.handlers.wsgi import  WSGIHandler
        from django.core.servers.basehttp import AdminMediaHandler
        from django.conf import settings

        settings.configure(DEBUG=True,
                           TEMPLATE_DEBUG=config.HTML_DEBUG,
                           DEFAULT_CHARSET=config.OUTPUT_ENCODING,
                           DEFAULT_CONTENT_TYPE='text/html',
                           ROOT_URLCONF = 'pyisis.web.urls',
                           INSTALLED_APPS = (
                                #'django.contrib.auth',
                                'django.contrib.contenttypes',
                                'django.contrib.sessions',
                                'django.contrib.sites',
                                #'django.contrib.admin',
                                'pyisis.web.isis'
                            ),
                            MIDDLEWARE_CLASSES = (
                                'django.middleware.common.CommonMiddleware',
                                'django.contrib.sessions.middleware.SessionMiddleware',
                                'django.contrib.auth.middleware.AuthenticationMiddleware',
                                'django.middleware.doc.XViewMiddleware',
                            ),
                            TEMPLATE_LOADERS = (
                            'django.template.loaders.filesystem.load_template_source',
                            'django.template.loaders.app_directories.load_template_source',
                            ),
                           SECRET_KEY = 'b(+ukc38349u0reu_8j)@iwpm017e(c#=0nmdn%s2u=$+*t@vo',
                           MEDIA_URL = '',
                           MEDIA_ROOT = config.MEDIA_ROOT,
                           USE_I18N = False,
                           LANGUAGE_CODE = 'en-us',
                           SITE_ID = 1,
                           TIME_ZONE = 'America/Sao_Paulo',
                           TEMPLATE_CONTEXT_PROCESSORS = (
                                "django.core.context_processors.debug",
                                #"django.core.context_processors.i18n",
                                "django.core.context_processors.media",
                            ),
                           TEMPLATE_DIRS=config.HTML_TEMPLATE_DIRS)

        # Glue code to plug Django into Twisted
        wsgires = wsgi.WSGIResource(AdminMediaHandler(WSGIHandler()))
        res = log.LogWrapperResource(wsgires)
        log.FileAccessLoggingObserver(config.WEB_LOG).start()
        site = server.Site(res)

        reactor.listenTCP(config.HTTP_PORT, channel.HTTPFactory(site))

    if config.SSH_PORT:
        from twisted.cred import portal, checkers
        from twisted.conch import manhole, manhole_ssh
        def getManholeFactory(namespace):
            realm = manhole_ssh.TerminalRealm()
            def getManhole(_): return manhole.Manhole(namespace)
            realm.chainedProtocolFactory.protocolFactory = getManhole
            p = portal.Portal(realm)
            checker = checkers.InMemoryUsernamePasswordDatabaseDontUse() 
            checker.addUser(config.USERNAME,config.PASSWORD)
            p.registerChecker(checker)
            f = manhole_ssh.ConchFactory(p)
            return f

        reactor.listenTCP(config.SSH_PORT, getManholeFactory(engine.collection))


    def showBanner(config):
        print "PyISIS Cell", __version__
        print "Python", sys.version
        if config.HTTP_PORT:
            print  _("Gateway ready to handle HTTP requests at port %s") % config.HTTP_PORT
        if config.SSH_PORT:
            print  _("Gateway ready to handle SSH requests at port %s") % config.SSH_PORT

    reactor.callWhenRunning(showBanner, config)
    reactor.run()


