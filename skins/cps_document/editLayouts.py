##parameters=REQUEST=None, **kw
# $Id$
"""
Called when something is changed in the flexible part of a document.

Returns True if layout changed
"""

if REQUEST is not None:
    kw.update(REQUEST.form)

layout_id = kw.get('layout_id')
if layout_id is None:
    return False

changed = False

up_row = None
down_row = None
delete_rows = []
for k in kw:
    if k.startswith('uprow_'):
        up_row = int(k[len('uprow_'):])
    if k.startswith('downrow_'):
        down_row = int(k[len('downrow_'):])
    if k.startswith('deleterow_'):
        delete_rows.append(int(k[len('deleterow_'):]))

if up_row is not None or down_row is not None:
    doc = context.getEditableContent()
    doc.flexibleChangeLayout(layout_id, up_row=up_row, down_row=down_row)
    changed = True

if delete_rows:
    doc = context.getEditableContent()
    doc.flexibleDelWidgetRows(layout_id, delete_rows)
    changed = True

if 'addwidget_button' in kw:
    doc = context.getEditableContent()
    doc.flexibleAddWidget(layout_id, kw['widget_type'],
                          label_edit=kw.get('widget_label_edit'))
    changed = True

return changed
