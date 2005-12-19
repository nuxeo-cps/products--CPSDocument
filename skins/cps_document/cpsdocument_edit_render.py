##parameters=request=None, cluster=None, layout_mode='edit', use_session=True
# $Id$
"""
Compute the rendering for a layout.

May use previous data from the request and session to display errors.

Returns the rendered HTML.
"""

doc = context.getContent()
rendered = doc.render(layout_mode=layout_mode, cluster=cluster,
                      request=request, proxy=context,
                      use_session=True, no_form=True) # XXX remove no_form
return rendered
