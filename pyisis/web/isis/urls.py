# -*- coding: utf-8 -*-
__created__ = "2007-05-29"
__author__  = "Rodrigo Senra <rsenra@acm.org>"


from django.conf.urls.defaults import *
from pyisis.web.isis.restapi import IsisCollectionReST
import pyisis.config

urlpatterns = patterns('',
    # static media files: images, js, css
    (r'media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': pyisis.config.config.MEDIA_ROOT}),
)

urlpatterns += patterns('pyisis.web.isis.restapi',
    (r'^restapi/*', IsisCollectionReST(permitted_methods=('DELETE','GET','PUT','POST'))),
    (r'^restclient/*', 'restclient'),   
)

urlpatterns += patterns('',
    (r'^xmlrpc/', 'pyisis.web.isis.xmlrpc.rpc_handler'),
)

urlpatterns += patterns('pyisis.web.isis.pftclient',
    (r'^pftclient/*', 'pftclient'),
    (r'^pftget_databases/*', 'pftget_databases'),
    (r'^pftfunction/*', 'pftfunction'),       
)

urlpatterns += patterns('pyisis.web.isis.views',
    (r'^$', 'home'),
    (r'^actionlet/*', 'view_html'),
    (r'^api/*', 'api'),
)
