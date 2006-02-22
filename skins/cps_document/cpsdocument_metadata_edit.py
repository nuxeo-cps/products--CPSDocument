##parameters=REQUEST, cpsdocument_edit_and_view_button=None
# $Id$
"""Edit the document metadata
"""
# Until ajax posts directly to its own script...
if 'ajax_edit' in REQUEST.form:
    if cpsdocument_edit_and_view_button is not None:
        REQUEST.form['cpsdocument_edit_and_view_button'] = \
          cpsdocument_edit_and_view_button
    return context.cpsdocument_edit_ajax(REQUEST, cluster='metadata')

return context.cpsdocument_edit(
    REQUEST, cluster='metadata', action='/cpsdocument_metadata',
    cpsdocument_edit_and_view_button=cpsdocument_edit_and_view_button)
