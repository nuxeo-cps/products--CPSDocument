# (C) Copyright 2005-2007 Nuxeo SAS <http://nuxeo.com>
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
from OFS.Image import File, Image
from AccessControl import ModuleSecurityInfo
from zipfile import ZipFile, BadZipfile
from StringIO import StringIO
from zExceptions import BadRequest
from Products.CPSCore.EventServiceTool import getEventService
from Products.CPSUtil.id import generateFileName

logger = getLogger('CPSDocument.createFile')

ModuleSecurityInfo('Products.CPSDocument.createFile').declarePublic('createFile')

def createFile(context, zip_file, check_allowed_content_types=True):
    """create documents based on the files in the uploaded ZIP"""
    if zip_file is None:
        return
    evtool = getEventService(context)
    evtool.notifyEvent('modify_object', context, {})
    registry = getToolByName(context, 'mimetypes_registry')
    ttool = getToolByName(context, 'portal_types')
    allowed_content_types = ttool[context.portal_type].allowed_content_types

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
    if not check_allowed_content_types:
        image_type_allowed = True
    else:
        image_type_allowed = 'Image' in  allowed_content_types
    # browsing the ZIP file
    for info in infolist:
        path = info.filename
        # Skip folders
        if path[-1] == '/':
            continue
        # Acquiring only the filename (without the directory path)
        path_filename = generateFileName(path.split('/')[-1])

        mimetype = registry.lookupExtension(path_filename.lower())
        if mimetype is not None:
            mimetype = mimetype.normalized()
        else:
            mimetype = 'application/octet-stream'

        if mimetype.startswith('image/') and image_type_allowed:
            # use the Image portal type or fallback to File if Image is not
            # allowed
            ptype = 'Image'
            field_name = 'preview'
        else:
            ptype = 'File'
            field_name = 'file'
        if check_allowed_content_types and ptype not in allowed_content_types:
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
        if ptype in ['Image']:
            file_to_attach = Image(path_filename, path_filename, data)
        else:
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
