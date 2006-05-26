##parameters=REQUEST, cluster=None
# $Id$
"""
Called when a document form is posted for AJAX validation.

Returns the validation result and the rendered page in an XML-RPC response.
"""
from Products.CPSDocument.utils import cleanAjaxParams

# cleaning incoming params
cleanAjaxParams(REQUEST)

doc = context.getContent()
res = doc.renderEditDetailed(request=REQUEST, proxy=context, cluster=cluster)
layout, is_valid = str(res[0]), res[1]

# AJAX tries to change the doc and just needs to know if there were errors
# for feedback without a new form rendering.
# XXX TODO: avoid here an extra HTML rendering
# by calling renderEditDetailed() with the right parameters

# At this time we do XML-RPC answers.
# We'll see later how to automate it to avoid a manual serialization here.
if is_valid and 'cpsdocument_edit_and_view_button' in REQUEST:
    action = 'view'
else:
    action = ''

REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml')
REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')
response = '<?xml version="1.0" encoding="utf-8" ?>'
response += '<ajax-response>'
response += '<result>%s</result>' % str(bool(is_valid))
response += '<layout><![CDATA[%s]]></layout>' % layout
response += '<action>%s</action>' % action
response += '</ajax-response>'

return response
