# $Id$

from Products.CMFCore.utils import getToolByName
from AccessControl import Unauthorized
from zLOG import LOG, DEBUG

def upgradeNewsDocuments(self):
    """Upgrade the News documents.

    This script is to be launched as an ExternalMethod, it will search for all
    News documents present in the portal and copy the old-existing newsdate
    attribute to the now-to-be-used EffectiveDate.

    Howto use the upgradeNewsDocuments ExternalMethod:
    - Log into the ZMI as manager
    - Go to your CPS root directory
    - Create an External Method with the following parameters:
    
    id            : upgradeNewsDocuments
    title         : Use this method if you upgrade an instance older than CPS 3.2.1
    Module Name   : CPSDocument.util
    Function Name : upgradeNewsDocuments
    
    - save it
    - then click on the test tab of this external method
    """

    log_key = 'upgradeNewsDocuments'
    LOG(log_key, DEBUG, "")

    brains = self.search(query={'portal_type': ('News',)})
    for brain in brains:
        proxy = brain.getObject()
        LOG(log_key, DEBUG, "checking %s..." % proxy.title_or_id)
        document = proxy.getEditableContent()
        newsdate = getattr(document, 'newsdate', None)
        if newsdate is not None:
            LOG(log_key, DEBUG, "updating -> %s <-" % proxy.title_or_id)
            document.edit(EffectiveDate = newsdate)
            delattr(document, 'newsdate')
