##parameters=dummy_user, value
# $Id$
"""Compute contributors.

Called by old Contributors write expression of the metadata schema.

BBB: will be removed in CPS 3.3.7.
"""

from Products.CPSDefault.utils import computeContributors
portal = context.portal_url.getPortalObject()

return computeContributors(portal, value)
