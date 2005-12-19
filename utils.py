# (C) Copyright 2005 Nuxeo SAS <http://nuxeo.com>
# Author: Florent Guillaume <fg@nuxeo.com>
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
"""Various cps document form utilities.

The form uid is used to ensure that the session applies to the same form
currently edited. It is included in forms and propagated during redirects.
"""

import random
from AccessControl import ModuleSecurityInfo


_FORM_UID_REQUEST_KEY = 'cpsformuid'

def getFormUid(request):
    return request.get(_FORM_UID_REQUEST_KEY)

def generateFormUid():
    return (str(random.randrange(1000000, 10000000)) +
            str(random.randrange(1000000, 10000000)))

ModuleSecurityInfo('Products.CPSDocument.utils'
                   ).declarePublic('getFormUidHtml')
def getFormUidHtml(request):
    """Generate HTML for the form uid.

    Generates a new uid if needed.
    """
    uid = getFormUid(request)
    if uid is None:
        # Generate a new one
        uid = generateFormUid()
        request[_FORM_UID_REQUEST_KEY] = uid
    return ('<input type="hidden" name="%s" value="%s" />'
            % (_FORM_UID_REQUEST_KEY, uid))

ModuleSecurityInfo('Products.CPSDocument.utils'
                   ).declarePublic('getFormUidUrlArg')
def getFormUidUrlArg(request):
    """Get an URL argument for the form uid.

    Returns a dict suitable for urlencode.
    """
    uid = getFormUid(request)
    if uid is not None:
        return {_FORM_UID_REQUEST_KEY: uid}
    else:
        return {}

