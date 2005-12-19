##parameters=comments=None
# $Id$
"""
Notify of the modification on a document.

Called by cpsdocument_edit.py
"""

# Find out if we are in a workspace, in which case we follow
# the workflow transition.
current = context
in_workspace = False
while current.portal_type != 'Portal':
    if current.portal_type == 'Workspace':
        in_workspace = True
        break
    current = current.aq_inner.aq_parent

if in_workspace:
    from Products.CMFCore.utils import getToolByName
    from Products.CMFCore.WorkflowCore import WorkflowException
    wftool = getToolByName(context, 'portal_workflow')
    # Try to fire 'modify' transition to add an entry in wf history
    try:
        wftool.doActionFor(context, 'modify', comment=comments)
        return
    except WorkflowException, e:
        if str(e) != 'No workflow provides the "modify" action.':
            raise

# Notify manually if no workflow modify transition is there
from Products.CPSCore.EventServiceTool import getPublicEventService
evtool = getPublicEventService(context)
evtool.notifyEvent('workflow_modify', context, {'comments': comments})
