##parameters=REQUEST, layout_id=None, cluster=None
# $Id$
"""
edit layout and content if form submited

return html renderer + psm
"""
from Products.CMFCore.WorkflowCore import WorkflowException

doc = context.getContent()

do_notify = False

layout_changed = context.editLayouts(REQUEST=REQUEST);

if (layout_changed
    or REQUEST.has_key('cpsdocument_edit_button')
    or REQUEST.has_key('cpsdocument_edit_and_view_button')):
    request = REQUEST
    psm = 'psm_content_changed'
    do_notify = True
else:
    request = None
    psm = ''

res = doc.renderEditDetailed(request=request, proxy=context,
                             layout_id=layout_id, cluster=cluster)

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
