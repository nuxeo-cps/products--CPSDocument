##parameters=REQUEST=None, **kw
# $Id$
"""
Called when something is changed in the flexible part of a document.

Returns True if layout changed
"""

if REQUEST is not None:
    kw.update(REQUEST.form)

changed = False

# parsing the form data
up_rows = []
down_rows = []
delete_rows = {}
add_widgets = []

for k in kw:

    if k.startswith('uprow_'):
        cmd, layout_id = k.split('__', 1)
        up_rows.append((int(cmd[len('uprow_'):]), layout_id))

    elif k.startswith('downrow_'):
        cmd, layout_id = k.split('__', 1)
        down_rows.append((int(cmd[len('downrow_'):]), layout_id))

    elif k.startswith('deleterow_'):
        cmd, layout_id = k.split('__', 1)
        rows = delete_rows.setdefault(layout_id, [])
        rows.append(int(cmd[len('deleterow_'):]))

    elif k.startswith('addwidget_button'):
        cmd, layout_id = k.split('__')
        try:
            position = int(cmd[len('addwidget_button_'):])
        except ValueError: # layout method not up to date for #2159
            position = None
        add_widgets.append((position, layout_id))

if not (up_rows or down_rows or delete_rows or add_widgets):
    # optim: do not getEditableContent unless necessary
    return changed

# now performing the requested layout tasks:
doc = context.getEditableContent()

for up_row, layout_id in up_rows:
    doc.flexibleChangeLayout(layout_id, up_row=up_row)
    changed = True

for down_row, layout_id in down_rows:
    doc.flexibleChangeLayout(layout_id, down_row=down_row)
    changed = True

for layout_id, rows in delete_rows.items():
    doc.flexibleDelWidgetRows(layout_id, rows)
    changed = True

for position, layout_id in add_widgets:
    doc.flexibleAddWidget(layout_id,
                          kw['widget_type_%d__%s' % (position, layout_id)],
                          label_edit=kw.get('widget_label_edit'),
                          position=position)
    changed = True

return changed
