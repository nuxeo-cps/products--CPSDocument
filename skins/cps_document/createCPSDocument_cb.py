##parameters=type_name, datamodel
# $Id$
"""
Callback to create an empty object with the context as a container.

Datamodel may be examined to create a suitable id.

Returns the created object. In CPS, returns the proxy (which is
the only thing the user sees).
"""
# $Id$

folder = context

id = datamodel.get('Title')
if not id:
    id = 'my ' + type_name

id = context.computeId(compute_from=id)

context.invokeFactory(type_name, id, datamodel=datamodel)
ob = getattr(context, id)

return ob
