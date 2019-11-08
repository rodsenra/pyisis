# -*- coding: utf-8 -*-
"""
This module implements views for dynamically generated pages.
"""
__created__ = "2007-05-29"
__author__  = "Rodrigo Senra <rsenra@acm.org>"

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^web/', include('pyisis.web.isis.urls')),
    (r'^$', 'pyisis.web.isis.views.root_home'),

    # Uncomment this for admin:
    #(r'^admin/', include('django.contrib.admin.urls')),
)


