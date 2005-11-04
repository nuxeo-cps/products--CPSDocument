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

from Products.CMFCore.utils import getToolByName

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

    The _objects attribute of docs with flexible content might be broken because
    of the use of the 'delattr' function instead of 'manage_delObjects' when
    deleting flexible fields.

    This is related to ticket:889
    """
    repository = getToolByName(context, 'portal_repository')
    fixed_fields = 0
    for doc in repository.values():
        new_objects = []
        for ob in doc._objects:
            if not hasattr(doc, ob['id']):
                fixed_fields += 1
            else:
                new_objects.append(ob)
        doc._objects = tuple(new_objects)
    return "CPSDocument updated: fixed %d broken flexible fields" % fixed_fields

def upgrade_336_337_anim_flash(context):
    """ Upgrade all Flash anims

    the field that contains the file, named 'preview'
    is beeing moved to 'flash_file'
    """
    repository = getToolByName(context, 'portal_repository')

    fixed_files = 0

    for doc in repository.values():
        if (hasattr(doc, 'portal_type') and
            doc.portal_type == 'Flash Animation'):
            if not hasattr(doc, 'flash_file') and hasattr(doc, 'preview'):
                doc.manage_renameObject('preview', 'flash_file')
                fixed_files += 1

    return "CPSDocument updated: fixed %d flash anims" % fixed_files
