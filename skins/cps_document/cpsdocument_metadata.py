##parameters=REQUEST
# $Id$
"""View or edit the document metadata according to permissions.
"""

from Products.CMFCore.utils import getToolByName

pmtool = getToolByName(context, 'portal_membership')
can_edit = pmtool.checkPermission('Modify portal content', context)

if not can_edit:
    return context.cpsdocument_view(cluster='metadata')
else:
    return context.cpsdocument_metadata_template()
