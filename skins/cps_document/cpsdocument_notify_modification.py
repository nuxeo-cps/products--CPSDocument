##parameters=comments=None
# $Id$
"""
Notify of the modification on a document.

Called by cpsdocument_edit.py
"""

# Only CPS Proxy Documents and friends have a workflow (this is not the case
# for other CPSDocument instances such as portlets)
if context.meta_type.startswith('CPS Proxy'):
    from Products.CMFCore.utils import getToolByName
    from Products.CMFCore.WorkflowCore import WorkflowException
    wftool = getToolByName(context, 'portal_workflow')
    # Try to fire 'modify' transition to add an entry in wf history
    try:
        wftool.doActionFor(context, 'modify', comment=comments)
        return
    except WorkflowException, e:
        # if the current document's wf does not have a modify transition, simply
        # ignore it
        if str(e) != 'No workflow provides the "modify" action.':
            raise

# Notify manually if no workflow modify transition is there
from Products.CPSCore.EventServiceTool import getPublicEventService
evtool = getPublicEventService(context)
evtool.notifyEvent('workflow_modify', context, {'comments': comments})
