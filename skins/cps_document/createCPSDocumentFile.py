## Script (Python) "cpsdocument_import_zip"
##parameters=zip_file=None, REQUEST=None, **kw
# $Id$
"""Import documents from a ZIP file."""

from zLOG import LOG, DEBUG 
from Products.CPSDocument.createFile import createFile

if REQUEST is not None:
    kw.update(REQUEST.form)

zip_file = REQUEST['zip_file']

if createFile(context, zip_file):
    psm = 'Content imported'
else:
    psm = 'Content not imported corectly'

if REQUEST is not None:
    action_path = ''
    REQUEST.RESPONSE.redirect('%s/%s?portal_status_message=%s' %
                              (context.absolute_url(), action_path,
                               psm))
return psm
