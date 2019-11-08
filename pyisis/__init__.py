# make this a package
__all__ = ['tools', 'files', 'fields', 'views', 'records', 'config', 'tests']

__versioninfo__ = (0, 9, 2)
__version__ = u".".join([str(i) for i in  __versioninfo__])
__author__ = u"Rodrigo D. A. Senra"

# aliases
from pyisis.files import MasterFile
from pyisis.records import MasterRecord
from pyisis.fields import MasterField
from pyisis.fields import MasterContainerField  

banner = u"""
PyISIS Cell v%s
Copyright (c)BIREME/PAHO 2007. All rights reserved.
"""%__version__
