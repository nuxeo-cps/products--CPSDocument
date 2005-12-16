##parameters=REQUEST, layout_id=None, cluster=None, **kw
# $Id$
"""
edit layout and content if form submited

return html renderer + psm
"""
from zLOG import LOG, DEBUG, INFO

ajax_edit = 'ajax_edit' in REQUEST.form or 'ajax_edit' in REQUEST

from Products.CMFCore.WorkflowCore import WorkflowException

doc = context.getContent()

do_notify = False

layout_changed = context.editLayouts(REQUEST=REQUEST);

if (layout_changed
    or REQUEST.has_key('cpsdocument_edit_button')
    or REQUEST.has_key('cpsdocument_edit_and_view_button')
    or ajax_edit):
    request = REQUEST
    psm = 'psm_content_changed'
    do_notify = True
else:
    request = None
    psm = ''

if ajax_edit:
    # this is hardcoded here because CPS is not utf8 yet
    # (it's ISO-8859-15)
    # so the form fields are sent in strings that are
    # unicode in fact
    for field_name, field_value in request.form.items():
        if isinstance(field_value, str):
            field_value = field_value.decode('utf8', 'replace')
            request.form[field_name] = field_value.encode('ISO-8859-15')

res = doc.renderEditDetailed(request=request, proxy=context,
                             layout_id=layout_id, cluster=cluster)

if ajax_edit:
    # ajax tries to change the doc
    # and just needs to know if there were errors
    # for feedback without a new form rendering
    # XXX todo: avoid here an extra HTML rendering
    # by calling renderEditDetailed() with the right parameters

    # at this time we do xmlrpc answers
    #
    # we'll see after how to automate it to avoid a manual
    # serialization here
    action = ''
    result = res[1]
    layout = str(res[0])

    # sending utf8 content
    layout = layout.decode('iso-8859-15').encode('utf8')
    if result and REQUEST.has_key('cpsdocument_edit_and_view_button'):
        action = 'redirect'

    REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml')
    REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')
    response = '<?xml version="1.0" encoding="utf-8" ?>'
    response += '<ajax-response>'
    response += '<result>%s</result>' % str(res[1])
    response += '<layout><![CDATA[%s]]></layout>' % layout
    response += '<action>%s</action>' % action
    response += '</ajax-response>'
    return response

if not res[1]:
    psm = 'psm_content_error'
    do_notify = False

if do_notify:
    comments = request.get('comments')
    # XXX:
    # Notification has to be done manually here until the workflow takes care of
    # the "workflow_modify" transition.
    from Products.CPSCore.EventServiceTool import getPublicEventService
    getPublicEventService(context).notifyEvent('workflow_modify', context,
                                            {'comments': comments,
                                             })

    # only done if we are in workspaces
    # in sections, modification leads to a full new version
    current = context
    curr_portal_type = ''
    in_workspace = False

    while curr_portal_type <> 'Portal' and current and not in_workspace:
        curr_portal_type = current.portal_type
        if curr_portal_type == 'Workspace':
            in_workspace = True
        else:
            next = current.getParentNode()
            if next == current:
                current = None
            else:
                current = next

    if in_workspace:
        pw = context.portal_workflow
        # try to fire 'modify' transition to add an entry in wf history
        # if wf do not provide it, do nothing
        try:
            pw.doActionFor(context, 'modify', comment=comments)
        except WorkflowException:
            pass

if REQUEST.has_key('cpsdocument_edit_and_view_button') and res[1]:
    # If everything went well and view is requested, redirect to it
    view_url = context.absolute_url()
    REQUEST.RESPONSE.redirect("%s?portal_status_message=%s" % (view_url, psm))

return res[0], psm
