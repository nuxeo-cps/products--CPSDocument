##parameters=REQUEST, cluster=None, type_name=None
# $Id$
"""
Called when a document form is posted.

Validates data, then:

 - if there's no error, updates the object and redirects to it,

 - if there's an error, puts data in session and redirects to creation form.

A form uid is propagated during the redirect to uniquely identify the
form in the session.
"""
from urllib import urlencode
from Products.CMFCore.utils import getToolByName
from Products.CPSDefault.utils import isIOrderedContainer
from Products.CPSDocument.utils import getFormUidUrlArg
from Products.CPSDocument.utils import createObjectsAtBottom

ti = getToolByName(context, 'portal_types').getTypeInfo(type_name)

is_valid, ds = ti.validateObject(None, layout_mode='create',
                                 request=REQUEST, context=context,
                                 cluster=cluster, use_session=True)

if is_valid:
    meth_id = ti.queryMethodID('create_do', 'cpsdocument_create_do')
    ob = getattr(context, meth_id)(type_name, ds.getDataModel())
    url = ob.absolute_url()
    action = ob.getTypeInfo().immediate_view
    psm = 'psm_content_created'
    args = {}
    # Move the newly created object as the first object in the folder,
    # unless an optional prop on context's fti contradicts this:
    # otherwise in folders with more that one page of documents
    # one would have to go to the last page.

    if isIOrderedContainer(context) and not createObjectsAtBottom(context):
        context.moveObjectsToTop([ob.getId()])
else:
    url = context.absolute_url()
    action = 'cpsdocument_create_form'
    psm = 'psm_content_error'
    args = {'type_name': type_name}
    args.update(getFormUidUrlArg(REQUEST))

args['portal_status_message'] = psm
url = url + '/' + action + '?' + urlencode(args)
REQUEST.RESPONSE.redirect(url)
