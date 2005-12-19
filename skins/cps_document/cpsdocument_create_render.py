##parameters=request=None, cluster=None, type_name=None, layout_mode='create', use_session=True
# $Id$
"""
Compute the rendering for a creation layout.

May use previous data from the request and session to display errors.

Returns the rendered HTML.
"""
from Products.CMFCore.utils import getToolByName

ti = getToolByName(context, 'portal_types').getTypeInfo(type_name)

rendered = ti.renderObject(None, layout_mode=layout_mode, cluster=cluster,
                           request=request, context=context,
                           use_session=True, no_form=True) # XXX remove no_form
return rendered
