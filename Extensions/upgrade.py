# (C) Copyright 2003-2005 Nuxeo SARL <http://nuxeo.com>
# Author:
# M.-A. Darche <madarche@nuxeo.com>
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
from AccessControl import Unauthorized
from zLOG import LOG, DEBUG


def upgradeDocuments(self):
    """Upgrade various documents to new portal_types and/or new schemas.

    Howto use the upgradeDocuments ExternalMethod:
    - Log into the ZMI as manager
    - Go to your CPS root directory
    - Create an External Method with the following parameters:

    id            : upgradeDocuments
    title         : Use this method if you upgrade an instance older than CPS 3.2.1
    Module Name   : CPSDocument.upgrade
    Function Name : upgradeDocuments

    - save it
    - then click on the test tab of this external method
    """

    log_key = 'upgradeDocuments'
    LOG(log_key, DEBUG, "")

    portal = self.portal_url.getPortalObject()

    modifyPortalType('News', 'News Item', portal)
    modifyPortalType('PressRelease', 'Press Release', portal)

    deletePortalTypes(('News', 'PressRelease'), portal)


def modifyPortalType(new_portal_type, old_portal_type, portal):
    log_key = 'modifyPortalType'
    brains = portal.search(query={'portal_type': (old_portal_type,)})
    for brain in brains:
        proxy = brain.getObject()
        LOG(log_key, DEBUG, "checking %s..." % proxy.title_or_id)
        document = proxy.getEditableContent()

        if document.portal_type == 'News':
            # Changing the newsdate field into the use of EffectiveDate instead
            newsdate = getattr(document, 'newsdate', None)
            if newsdate is not None:
                LOG(log_key, DEBUG, "updating -> %s <-" % proxy.title_or_id)
                document.edit(EffectiveDate = newsdate)
                delattr(document, 'newsdate')

        proxy.portal_type = new_portal_type
        document.portal_type = new_portal_type



def deletePortalTypes(portal_types, portal):
    for portal_type in portal_types:
        if portal_type in portal.portal_types.objectIds():
            portal.portal_types.manage_delObjects(portal_type)
