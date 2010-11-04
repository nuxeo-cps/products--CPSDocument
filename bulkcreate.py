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
"""Utilities for bulk creation of documents.

Create documents according to the MIME types of the files,
typically themselves inferred from extensions
"""

from zipfile import ZipFile, BadZipfile
from cStringIO import StringIO
from copy import deepcopy
from logging import getLogger

from zope.component import getAdapter
from AccessControl import ModuleSecurityInfo
from zExceptions import BadRequest
from OFS.Image import File

from Products.CMFCore.utils import getToolByName
from Products.CPSUtil.id import generateFileName
from Products.CPSUtil.file import ofsFileHandler
from Products.CPSUtil.text import get_final_encoding
from Products.CPSCore.EventServiceTool import getEventService
from Products.CPSSchemas.FileUtils import FileObjectFactory

logger = getLogger('CPSDocument.bulkcreate')

msi = ModuleSecurityInfo('Products.CPSDocument.bulkcreate')

class FieldResolver(object):
    """Caches the field objects : must stay transient."""

    def __init__(self, types_tool):
        self.cache = {}
        self.ttool = types_tool

    def resolve(self, ptype, fid):
        fti = self.ttool[ptype]

        # field retrieval with cache
        fields_cache = self.cache
        ckey = (ptype, fid)
        field = fields_cache.get(ckey)
        if field is None:
            for s in fti._listSchemas(): # no flexible, of course
                if not s.has_key(fid):
                    continue
                field = fields_cache[ckey] = s[fid]
                break
            else:
                raise ValueError(
                    "Field %s not in %s non-flexible schemas" % (fid, ptype))
        return field


msi.declarePublic('import_zip')
def import_zip(container, zip_file, check_allowed_content_types=True):
    """create documents based on the files in a  ZIP archive.

    The archive itself must be an instance of a subclasss of OFS.Image.File
    """
    if zip_file is None:
        return
    evtool = getEventService(container)

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
        zipfile = ZipFile(ofsFileHandler(zip_file))
    except BadZipfile:
        logger.info('Bad Zip File')
        return 0

    cont_ptype = getattr(container, 'portal_type', None)
    if cont_ptype is None:
        raise ValueError("Called for improper container %s" % container)

    ttool = getToolByName(container, 'portal_types')
    cont_fti = ttool[cont_ptype]

    field_resolver = FieldResolver(ttool)
    proxy_fact = getToolByName(container, 'portal_workflow').invokeFactoryFor

    evtool.notifyEvent('modify_object', container, {})

    # browsing the ZIP file
    infolist = zipfile.infolist()
    for info in infolist:
        path = info.filename
        # Skip folders
        if path[-1] == '/':
            continue
	# Skip technical MacOS dir that's useless for us and causes collisions
	if '__MACOSX/' in path:
            continue

        # Acquiring only the filename (without the directory path)
        filename = path.rsplit('/', 1)[-1]
        path_filename = generateFileName(filename)

        ptype, fid = cont_fti.getAutoContentInfo(
            file_name=path_filename, check_allowed=check_allowed_content_types)
        if ptype is None:
            continue

        field = field_resolver.resolve(ptype, fid)

        fobj = FileObjectFactory.make(field, path_filename, filename,
                                      zipfile.read(path))

        encoding = get_final_encoding(container)
        title = filename.decode(encoding, 'ignore')
        try:
            file_id = proxy_fact(container, ptype, path_filename,
                                 Title=title, **{fid: fobj})
        except BadRequest:
            logger.exception('File %s already exists', path_filename)
            continue

        # there was a content_type correction of file obj in earlier version.
        # might be necessary again (didn't see anything in history)

    return 1
