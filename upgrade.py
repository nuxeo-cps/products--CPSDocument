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
    return "CPSDocument updated : Sections allow conten types"
