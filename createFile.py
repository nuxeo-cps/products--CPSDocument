"""Compatibility alias."""

import warnings
from AccessControl import ModuleSecurityInfo
from bulkcreate import import_zip

ModuleSecurityInfo('Products.CPSDocument.createFile').declarePublic(
    'createFile')

def createFile(*args, **kwargs):
    warnings.warn('createFile.createFile is a compatibility alias for '
                  'bulkcreate.import_zip and will be removed in CPS 3.6',
                  DeprecationWarning, 2)
    return import_zip(*args, **kwargs)

