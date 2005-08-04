##parameters=REQUEST
# $Id$
"""View or edit the document metadata

If user is not allowed to edit the document, display the metadata page in view
mode.

If user is allowed to edit the document:
- if form has not been submitted yet, or if an error occured during edition,
  display the metadata page in edit mode.
- if edition has been successfully performed, redirect to the document view
  page.
"""

from Products.CMFCore.utils import getToolByName

pmtool = getToolByName(context, 'portal_membership')
can_edit = pmtool.checkPermission('Modify portal content', context)

if not can_edit:
    return context.cpsdocument_metadata_template(edit_metadata=0)
else:
    form_submitted = REQUEST.form.has_key('cpsdocument_edit_button')
    # editCPSDocument will check if form has been submitted too before
    # committing data managed by the metadata cluster
    rendered_main, psm = context.editCPSDocument(REQUEST=REQUEST,
                                                 cluster='metadata')
    error = psm == 'psm_content_error'

    if not form_submitted or error:
        return context.cpsdocument_metadata_template(edit_metadata=1,
                                                     rendered_main=rendered_main,
                                                     portal_status_message=psm)
    else:
        redirect_url = context.absolute_url()
        redirect_url += "?portal_status_message=" + psm
        REQUEST.RESPONSE.redirect(redirect_url)

