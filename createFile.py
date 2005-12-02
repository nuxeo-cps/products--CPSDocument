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

from Products.CMFCore.utils import getToolByName
from OFS.Image import File
from zLOG import LOG, DEBUG, INFO
from AccessControl import ModuleSecurityInfo
from zipfile import ZipFile, BadZipfile
from StringIO import StringIO
from zExceptions import BadRequest
from Products.CPSCore.EventServiceTool import getEventService


ModuleSecurityInfo('Products.CPSDocument.createFile').declarePublic('createFile')

def createFile(context, zip_file):
    """create documents based on the files in the uploaded ZIP"""

    evtool = getEventService(context)
    evtool.notifyEvent('modify_object', context, {})

    if hasattr(zip_file, 'filename'):
        filename = zip_file.filename
    else:
        filename = zip_file.name

    try:
        temp_file = File(filename, '', file=zip_file)
    except ValueError:
        LOG('createFile', INFO,
                'Inexistent uploaded ZIP file')
        return 0
    try:
        zipfile = ZipFile(StringIO(str(temp_file)))
    except BadZipfile:
        LOG('createFile', INFO,
                'Bad Zip File')
        return 0
    infolist = zipfile.infolist()
    # browsing the ZIP file
    for info in infolist:
        path = info.filename
        # Skip folders
        if path[-1] == '/':
            continue
        data = zipfile.read(path)
        # Acquiring only the filename (without the directory path)
        path_filename = path.split('/')[-1]
        try:
            file_id = context.portal_workflow.invokeFactoryFor(
                     context, 'File', path_filename)
        except BadRequest:
            LOG('createFile', INFO,
                'File %s already exists' % (path_filename))
            return 0

        file_obj = getattr(context, file_id)
        file_obj = file_obj.getEditableContent()

        # create file to attach to document
        file_to_attach = File(path_filename, path_filename, data)
        registry = getToolByName(context, 'mimetypes_registry')
        mimetype = registry.lookupExtension(path_filename.lower())
        if mimetype and file_to_attach.content_type != mimetype.normalized():
            LOG('createFile', DEBUG,
                'Fixing mimetype from %s to %s' % (
                file_to_attach.content_type, mimetype.normalized()))
            file_to_attach.manage_changeProperties(
                content_type=mimetype.normalized())

        kw = {'Title': path_filename,
          'Description': 'Imported File (original archive: %s)' % filename,
          'file': file_to_attach}

        file_obj.edit(**kw)

    return 1
