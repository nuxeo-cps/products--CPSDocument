# Copyright 2005-2007 Nuxeo SAS <http://nuxeo.com>
# Author: Julien Anguenot <ja@nuxeo.com>
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

import logging

import transaction
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CPSUtil.text import OLD_CPS_ENCODING
import itertools

_marker = object()

def upgrade_334_335_allowct_sections(context):
    ttool = getToolByName(context, 'portal_types')
    section = ttool['Section']
    flextypes = context.getDocumentTypes()
    allowed_in = flextypes.keys()
    for ptype in allowed_in:
        sectionACT = list(section.allowed_content_types)
        if ptype not in  sectionACT:
            sectionACT.append(ptype)
            section.allowed_content_types = sectionACT
    return "CPSDocument updated: Sections allow content types"

def upgrade_335_336_fix_broken_flexible(context):
    """Fix broken flexible attachement fields

    The _objects attribute of docs with flexible content might be broken
    because of the use of the 'delattr' function instead of
    'manage_delObjects' when deleting flexible fields.

    This is related to ticket #889.
    """
    repository = getToolByName(context, 'portal_repository')
    fixed_fields = 0
    for doc in repository.values():
        if getattr(doc, '_objects', None) is None:
            continue
        new_objects = []
        for ob in doc._objects:
            if getattr(aq_base(doc), ob['id'], None) is None:
                fixed_fields += 1
            else:
                new_objects.append(ob)
        doc._objects = tuple(new_objects)
    return "CPSDocument updated: fixed %d broken flexible fields" % fixed_fields

def upgrade_336_337_anim_flash(context):
    """Upgrade all Flash Animations.

    The field 'preview' that contains the file is moved to 'flash_file'.
    """
    repository = getToolByName(context, 'portal_repository')
    fixed_files = 0
    for doc in repository.values():
        bdoc = aq_base(doc)
        if getattr(bdoc, 'portal_type', None) == 'Flash Animation':
            preview = getattr(bdoc, 'preview', _marker)
            flash_file = getattr(bdoc, 'flash_file', _marker)
            if preview is not _marker and flash_file is _marker:
                if preview == None:
                    delattr(bdoc, 'preview')
                    bdoc.flash_file = None
                else:
                    doc.manage_renameObject('preview', 'flash_file')
                fixed_files += 1
    return "CPSDocument updated: fixed %d flash anims" % fixed_files

def check_338_340_document_to_flex(context):
    ttool = getToolByName(context, 'portal_types')
    if 'Document' not in ttool.objectIds():
        # No Document type to upgrade
        return False
    doc_type = ttool['Document']
    from FlexibleTypeInformation import FlexibleTypeInformation
    if doc_type.meta_type != FlexibleTypeInformation.meta_type:
        # This is CPS 3.2, and Document is not even Flexible.
        # Can't upgrade
        return False
    if 'flexible_content' in doc_type.schemas:
        # Alredy upgraded:
        return False
    return True

def upgrade_338_340_document_to_flex(context):
    """Upgrade Document type instances to become flexible."""
    repository = getToolByName(context, 'portal_repository')
    ttool = getToolByName(context, 'portal_types')

    doc_type = ttool['Document']
    schemas = list(doc_type.schemas)
    if 'document' in schemas:
        schemas.remove('document')
    if 'flexible_content' not in schemas:
        schemas.append('flexible_content')
    doc_type.schemas = tuple(schemas)

    layouts = list(doc_type.layouts)
    if 'document' in layouts:
        layouts.remove('document')
    if 'flexible_content' not in layouts:
        layouts.append('flexible_content')
    doc_type.layouts = tuple(layouts)

    doc_type.flexible_layouts = ('flexible_content:flexible_content',)

    pfilter = lambda o: getattr(o, 'portal_type', '') == 'Document'
    docs = itertools.ifilter(pfilter, repository.values())
    count = 0
    for doc in docs:
        bdoc = aq_base(doc)

        schemas = getattr(bdoc, '.cps_schemas', None)
        content = getattr(bdoc, 'content', None)
        content_position = getattr(bdoc, 'content_position', None)
        content_format = getattr(bdoc, 'content_format', None)

        if (schemas is not None
            and content is None
            and content_position is None
            and content_format is None
            ):
            continue

        doc.flexibleAddWidget('flexible_content', 'textimage')
        kw = {'content_f0': content,
              'content_f1': content_position,
              'content_f2': content_format,
              }
        doc.edit(**kw)

        for attr in 'content', 'content_position', 'content_format':
            delattr(doc, attr)

        count += 1

    return 'CPSDocument updated: %d Document instances became flexible' % count

def check_338_340_newsitem_to_flex(context):
    ttool = getToolByName(context, 'portal_types')
    if 'News Item' not in ttool.objectIds():
        # No Document type to upgrade
        return False
    doc_type = ttool['News Item']
    from FlexibleTypeInformation import FlexibleTypeInformation
    if doc_type.meta_type != FlexibleTypeInformation.meta_type:
        # News item is not even a CPSDocument. That happens with 3.3.0.
        return False
    schemas = list(doc_type.schemas)
    if 'news' in schemas:
        return True

    # Even if the doc_type is upgraded, we might need to upgrade documents
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.searchResults(portal_type='News Item')
    # Let's just test the first one, so the checker doesn't get very slow.
    if len(brains) == 0:
        return False

    ob = brains[0].getObject()
    if getattr(ob, 'attachedFile', _marker) is _marker:
        return False

    return True

def upgrade_338_340_newsitem_to_flex(context):
    """Upgrade News Item type instances to become flexible."""
    repository = getToolByName(context, 'portal_repository')
    ttool = getToolByName(context, 'portal_types')

    doc_type = ttool['News Item']
    schemas = list(doc_type.schemas)
    if 'news' in schemas:
        schemas.remove('news')
        schemas.append('newsitem')
        doc_type.schemas = tuple(schemas)

    layouts = list(doc_type.layouts)
    if 'news' in layouts:
        layouts.remove('news')
        layouts.append('newsitem_start')
        layouts.append('newsitem_flexible')
        layouts.append('newsitem_end')
        doc_type.layouts = tuple(layouts)

    doc_type.flexible_layouts = ('newsitem_flexible:flexible_content',)

    pfilter = lambda o: getattr(o, 'portal_type', '') == 'News Item'
    docs = itertools.ifilter(pfilter, repository.values())
    count = 0
    for doc in docs:
        bdoc = aq_base(doc)

        schemas = getattr(bdoc, '.cps_schemas', None)
        attachedFile = getattr(bdoc, 'attachedFile', None)
        attachedFile_text = getattr(bdoc, 'attachedFile_text', None)
        attachedFile_html = getattr(bdoc, 'attachedFile_html', None)

        if (schemas is not None
            and attachedFile is None
            and attachedFile_text is None
            and attachedFile_html is None
            ):
            continue

        doc.flexibleAddWidget('newsitem_flexible', 'attachedFile')
        kw = {'attachedFile_f0': attachedFile,
              'attachedFile_f1': attachedFile_text,
              'attachedFile_f2': attachedFile_html,
              }
        doc.edit(**kw)

        for attr in 'attachedFile', 'attachedFile_text', 'attachedFile_html':
            if getattr(doc, attr, _marker) is not _marker:
                delattr(doc, attr)

        count += 1

    return 'CPSDocument updated: %d Document instances became flexible' % count

def upgrade_350_351_unicode(portal):
    """Upgrade all documents to unicode.

    Takes care of frozen revisions without version bumps
    CPS String Field content will be cast to unicode, whereas
    CPS Ascii String Field content will be cast to str
    """

    logger = logging.getLogger('Products.CPSDocument.upgrades.350_351_unicode')
    repotool = portal.portal_repository
    total = len(repotool)

    done = 0
    for doc in repotool.iterValues():
        if not _upgrade_doc_unicode(doc):
            logger.error("Could not upgrade document revision %s", doc)
            continue
        done += 1
        if done % 100 == 0:
            logger.info("Upgraded %d/%d document revisions", done, total)
            transaction.commit()

    logger.warn("Finished unicode upgrade of the %d/%d documents.", done, total)

    ptool = portal.portal_cpsportlets
    done = 0
    logger.info("Starting upgrade of portlets")
    ptls = ptool.listAllPortlets()
    total = len(ptls)
    for ptl in ptls:
        if not _upgrade_doc_unicode(ptl):
            logger.error("Could not upgrade portlet %s", doc)
            continue
        done += 1
    transaction.commit()
    logger.warn("Upgraded %d/%d portlets.", done, total)

def _upgrade_doc_unicode(doc):

        ptype = doc.portal_type

        # Going through DataModel for uniformity (DublinCore etc)
        try:
            dm = doc.getDataModel()
        except ValueError:
            # if due to lack of FTI, already logged
            return False
        sfields = []
        slfields = []
        for f_id, f in dm._fields.items():
            if f.meta_type == 'CPS String Field':
                v = dm[f_id]
                if not isinstance(v, str):
                    # can have unicode, or... None (bad schema conf)
                    continue
                dm[f_id] = v.decode(OLD_CPS_ENCODING)

            elif f.meta_type == 'CPS String List Field':
                lv = dm[f_id]
                if not lv:
                    continue
                dm[f_id] = [
                    isinstance(v, str) and v.decode(OLD_CPS_ENCODING) or v
                    for v in lv]
            elif f.meta_type == 'CPS Ascii String Field':
                v = dm[f_id]
                try:
                    dm[f_id] = str(v)
                except UnicodeError:
                    logger.error("Non ascii content for CPS Ascii String Field"
                                 " in %s", doc.getId())
            elif f.meta_type == 'CPS Ascii String List Field':
                lv = dm[f_id]
                if not lv:
                    continue
                try:
                    dm[f_id] = [str(v) for v in lv]
                except UnicodeError:
                    logger.error("Non ascii content for CPS Ascii String List "
                                 "Field in %s", doc.getId())

        dm._commitData() # _commit() could spawn a new revision
        return True

