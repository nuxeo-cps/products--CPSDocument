##parameters=REQUEST, cpsdocument_edit_and_view_button=None
# $Id$
"""Edit the document metadata
"""

return context.cpsdocument_edit(
    REQUEST, cluster='metadata', action='/cpsdocument_metadata',
    cpsdocument_edit_and_view_button=cpsdocument_edit_and_view_button)
