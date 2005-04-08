##parameters=loadcustom=1
#$Id$
"""
The list of the document roots.

Returns the following structure:
{
root_id:{
          'title': 'The title',
          'wf_attrname': 'attribute in doctype definitions',
          'content_default_wf': 'default wf under this root'
        },
...
}
*title -> a title for this root of documents
*wf_attrname -> the name of the attribute to use in doctype
definitions in order to specify the workflow associated with
that type under the root in question. 
This is only needed for backward compatibility, as the workflows
associated with the type in different roots can now be specified
into a dictionnary corresponding to the key "workflows" in
doctype definition; the keys 'cps_workspace_wf' and 'cps_section_wf'
was used before.
*content_default_wf: the workflow to be applied to the objects 
situated under this root if no explicit association is found
"""


workspaces = {
    'title': 'Workspaces',
    'wf_attrname': 'cps_workspace_wf',
    'content_default_wf': 'workspace_content_wf',
    }

sections = {
    'title': 'Sections',
    'wf_attrname': 'cps_section_wf',
    'content_default_wf': 'section_content_wf',
}

doc_roots = {}
doc_roots['workspaces'] = workspaces
doc_roots['sections'] = sections

if loadcustom:
    custom_document_roots = context.getCustomDocumentRoots()
    doc_roots.update(custom_document_roots)

return doc_roots
