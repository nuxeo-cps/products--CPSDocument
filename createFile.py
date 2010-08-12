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

from zipfile import ZipFile, BadZipfile
from cStringIO import StringIO
from copy import deepcopy
from logging import getLogger

from zope.component import getAdapter
from AccessControl import ModuleSecurityInfo
from zExceptions import BadRequest
from OFS.Image import Image, File

from Products.CMFCore.utils import getToolByName
from Products.CPSUtil.id import generateFileName
from Products.CPSCore.EventServiceTool import getEventService
from Products.CPSSchemas.BasicFields import CPSFileField, CPSImageField

logger = getLogger('CPSDocument.createFile')

ModuleSecurityInfo('Products.CPSDocument.createFile').declarePublic('createFile')

class FileObjectFactory(object):
    """A class that generate File objects, caching some info.

    Must be transient.
    """

    # GR: this could be handled by a ZCA adapter,
    # but I don't want to open this pandora box now; just opening CPSSchema's
    # ZCML files is mind-blocking: two many things around
    # (StorageAdapter, TramlineFile itself?) that could be done this way
    # and clarified.
    # Besides, OFS.Image.File has no interface anyway (!)
    methods = { # field class -> (callable, options dict)
        CPSFileField.meta_type: (File, {}),
        CPSImageField.meta_type: (Image, {})
        # example with a factory method needing the context and having
        # another option
        # : (TramlineFile.direct_create, dict(context=True, thr=10240))
    }

    def __init__(self, types_tool):
        self.cache = {}
        self.ttool = types_tool

    def make(self, ptype, fid, oid, title, data):
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

        # instantiation
        meth, options = self.methods[field.meta_type]
        kw = deepcopy(options)
        if kw.get('context', False):
            kw['context'] = self.ttool
        return meth(oid, title, data, **kw)

def createFile(container, zip_file, check_allowed_content_types=True):
    """create documents based on the files in the uploaded ZIP"""
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
        # TODO use OFSFileIO
        zipfile = ZipFile(StringIO(str(zip_file)))
    except BadZipfile:
        logger.info('Bad Zip File')
        return 0

    cont_ptype = getattr(container, 'portal_type', None)
    if cont_ptype is None:
        raise ValueError("Called for improper container %s" % container)

    ttool = getToolByName(container, 'portal_types')
    cont_fti = ttool[cont_ptype]

    fobj_fact = FileObjectFactory(ttool)
    proxy_fact = getToolByName(container, 'portal_workflow').invokeFactoryFor

    evtool.notifyEvent('modify_object', container, {})

    # browsing the ZIP file
    infolist = zipfile.infolist()
    for info in infolist:
        path = info.filename
        # Skip folders
        if path[-1] == '/':
            continue

        # Acquiring only the filename (without the directory path)
        filename = path.rsplit('/', 1)[-1]
        path_filename = generateFileName(filename)

        ptype, fid = cont_fti.getAutoContentInfo(
            file_name=path_filename, check_allowed=check_allowed_content_types)
        if ptype is None:
            continue

        fobj = fobj_fact.make(ptype, fid, path_filename, filename,
                              zipfile.read(path))
        try:
            file_id = proxy_fact(container, ptype, path_filename,
                                 Title=filename, **{fid: fobj})
        except BadRequest:
            logger.info('File %s already exists', path_filename)
            return 0

        # there was a content_type correction of file obj in earlier version.
        # might be necessary again (didn't see anything in history)

    return 1
