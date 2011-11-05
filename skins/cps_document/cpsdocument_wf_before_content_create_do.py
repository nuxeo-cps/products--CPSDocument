##parameters=type_name, datamodel
# $Id$
"""
Create an empty object in the context according to the datamodel.

Datamodel may be examined to create a suitable id.

Returns the created object (usually a proxy).
"""
from Products.CMFCore.utils import getToolByName
id = datamodel.get('Title')
if not id:
    id = 'my ' + type_name
id = context.computeId(compute_from=id) # XXX shouldn't use a skin

language = datamodel.get('Language')
if not language:
    ts = getToolByName(context, 'translation_service')
    language = ts.getSelectedLanguage()

ttool = getToolByName(context, 'portal_types')
ti = ttool[type_name]
allow_discussion = ti.allowDiscussion()

# Datamodel is passed so that flexti can initialize the object.
new_id = context.invokeFactory(type_name, id, datamodel=datamodel,
                               language=language,
                               wf_before_content=True,
                               allow_discussion=allow_discussion)
if new_id is not None:
    id = new_id

ob = getattr(context, id)

context.notifyCPSDocumentCreation(ob=ob) # BBB obsolete in CPS 3.5.0

return ob
