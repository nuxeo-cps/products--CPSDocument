##parameters=REQUEST=None, **kw
# $Id$
"""
Action called when something is changed in the flexible part of a document.
return 1 if layout changed
"""

if REQUEST is not None:
    kw.update(REQUEST.form)

layout_id = kw.get('layout_id')
ret = 0

up_row = None
down_row = None
delete_rows = []
for k in kw.keys():
    if k.startswith('uprow_'):
        up_row = int(k[len('uprow_'):])
    if k.startswith('downrow_'):
        down_row = int(k[len('downrow_'):])
    if k.startswith('deleterow_'):
        delete_rows.append(int(k[len('deleterow_'):]))

if up_row is not None or down_row is not None:
    context.getContent().flexibleChangeLayout(layout_id, up_row=up_row,
                                              down_row=down_row)
    ret = 1

if delete_rows:
    context.getContent().flexibleDelWidgetRows(layout_id, delete_rows)
    ret = 1

if kw.has_key('addwidget_button'):
    kwargs = {'label_edit': kw.get('widget_label_edit')}
    context.getContent().flexibleAddWidget(layout_id, kw['widget_type'],
                                           **kwargs)
    ret = 1

return ret
