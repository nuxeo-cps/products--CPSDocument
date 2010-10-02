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
import re

import transaction
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CPSUtil.text import upgrade_string_unicode
from Products.CPSSchemas.BasicFields import CPSStringField
from Products.CPSSchemas.upgrade import upgrade_datamodel_unicode

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

def upgrade_unicode(portal, resync_trees=True):
    """Upgrade all documents to unicode.

    Takes care of frozen revisions without version bumps
    CPS String Field content will be cast to unicode, whereas
    CPS Ascii String Field content will be cast to str
    """

    logger = logging.getLogger('Products.CPSDocument.upgrades.unicode')
    repotool = portal.portal_repository
    total = len(repotool)

    done = 0
    for doc in repotool.iterValues():
        if not upgrade_doc_unicode(doc):
            logger.error("Could not upgrade document revision %s", doc)
            continue
        done += 1
        if done % 100 == 0:
            logger.info("Upgraded %d/%d document revisions", done, total)
            transaction.commit()

    logger.warn("Finished unicode upgrade of the %d/%d documents.", done, total)

    if not resync_trees:
        return

    logger.info("Rebuilding Tree Caches")
    trees = portal.portal_trees.objectValues('CPS Tree Cache')
    for tree in trees:
        logger.info("Rebuilding %s", tree)
        tree.rebuild()
        transaction.commit()
    logger.warn("Finished rebuilding the Tree Caches")

def upgrade_doc_unicode(doc):
        ptype = doc.portal_type

        logger = logging.getLogger('Products.CPSDocument.upgrades.doc_unicode')
        # Going through DataModel for uniformity (DublinCore etc)
        if doc.hasObject('.cps_schemas'):
            # we may have String fields to upgrade so that they validate None
            for sch in doc['.cps_schemas'].objectValues(['CPS Schema']):
                for ffield in sch.objectValues(['CPS File Field']):
                    suffix = ffield.suffix_text
                    if not suffix:
                        continue
                    try:
                        tfield = sch[ffield._getDependantFieldsBaseId()+suffix]
                    except KeyError, AtrributeError:
                        logger.warn("Could not find the text alternative field"
                                    "for %s", ffield.absolute_url_path())
                        continue

                    if not isinstance(tfield, CPSStringField):
                        logger.warn("Should have been a CPS String Field: %s",
                                    field.absolute_url_path())
                        continue
                    tfield.validate_none = True
                    logger.info("Upgraded text alternative field at %s",
                                tfield.absolute_url_path())

        try:
            dm = doc.getDataModel()
        except ValueError:
            # if due to lack of FTI, already logged
            return False

        return upgrade_datamodel_unicode(dm)

