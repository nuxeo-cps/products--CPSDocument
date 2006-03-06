# Copyright 2005 Nuxeo SARL <http://nuxeo.com>
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

from zLOG import LOG, DEBUG
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName

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
    return True

def upgrade_338_340_document_to_flex(context):
    """Upgrade Document type instances to become flexible."""
    repository = getToolByName(context, 'portal_repository')
    ttool = getToolByName(context, 'portal_types')

    doc_type = ttool['Document']
    schemas = list(doc_type.schemas)
    schemas.remove('document')
    schemas.append('flexible_content')
    doc_type.schemas = tuple(schemas)

    layouts = list(doc_type.layouts)
    layouts.remove('document')
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
