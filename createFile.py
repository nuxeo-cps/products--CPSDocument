# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
# Author: Dragos Ivan <di@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$
"""import documents from uploaded ZIP file

Create a document (attached file) for each file in the uploaded ZIP, 
with types according to their extensions
"""

from logging import getLogger

from Products.CMFCore.utils import getToolByName
from OFS.Image import File
from AccessControl import ModuleSecurityInfo
from zipfile import ZipFile, BadZipfile
from StringIO import StringIO
from zExceptions import BadRequest
from Products.CPSCore.EventServiceTool import getEventService
from Products.CPSUtil.id import generateFileName

logger = getLogger('CPSDocument.createFile')

ModuleSecurityInfo('Products.CPSDocument.createFile').declarePublic('createFile')

def createFile(context, zip_file):
    """create documents based on the files in the uploaded ZIP"""
    if zip_file is None:
        return
    evtool = getEventService(context)
    evtool.notifyEvent('modify_object', context, {})
    registry = getToolByName(context, 'mimetypes_registry')
    ttool = getToolByName(context, 'portal_types')

    if hasattr(zip_file, 'filename'):
        filename = zip_file.filename
    elif hasattr(zip_file, 'name'):
        filename = zip_file.name
    else:
        filename = "temp_file"

    if not isinstance(zip_file, File):
        try:
            zip_file = File(filename, '', file=zip_file)
        except ValueError:
            logger.info('Inexistent uploaded ZIP file')
            return
    try:
        zipfile = ZipFile(StringIO(str(zip_file)))
    except BadZipfile:
        logger.info('Bad Zip File')
        return 0
    infolist = zipfile.infolist()
    # browsing the ZIP file
    for info in infolist:
        path = info.filename
        # Skip folders
        if path[-1] == '/':
            continue
        # Acquiring only the filename (without the directory path)
        path_filename = generateFileName(path.split('/')[-1])
        mimetype = registry.lookupExtension(path_filename.lower()).normalized()
        if mimetype.startswith('image/'):
            ptype = 'Image'
            field_name = 'preview'
        else:
            ptype = 'File'
            field_name = 'file'
        fti = ttool[context.portal_type]
        if ptype not in fti.allowed_content_types:
            continue
        try:
            file_id = context.portal_workflow.invokeFactoryFor(
                context, ptype, path_filename)
        except BadRequest:
            logger.info('File %s already exists', path_filename)
            return 0

        file_proxy = getattr(context, file_id)
        file_doc = file_proxy.getEditableContent()

        # create file to attach to document
        data = zipfile.read(path)
        file_to_attach = File(path_filename, path_filename, data)
        if mimetype and file_to_attach.content_type != mimetype:
            logger.debug('Fixing mimetype from %s to %s',
                         file_to_attach.content_type, mimetype)
            file_to_attach.manage_changeProperties(content_type=mimetype)

        doc_def = {
            'Title': path_filename,
            'Description': 'Imported File (original archive: %s)' % filename,
            field_name: file_to_attach,
        }

        file_doc.edit(doc_def, proxy=file_proxy)

    return 1
