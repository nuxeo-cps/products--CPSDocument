##parameters=loadcustom=1
#$Id$
"""
Here are defined list of portal type created with CPSDocument
"""

section_type = {
    'title': 'portal_type_Section_title',
    'description': 'portal_type_Section_description',
    'content_icon': 'section_icon.png',
    'content_meta_type': 'Folder',
    'product': 'CPSDefault',
    'factory': 'addFolder',
    'immediate_view': 'folder_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ('Section',),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folder',
    'schemas': ['metadata', 'common', 'folder'],
    'layouts': ['common', 'folder'],
    'layout_clusters': ['metadata:metadata'],
    'cps_section_wf': 'section_folder_wf',
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'folder_view',
                 'permissions': ('View',)},
                {'id': 'new_content',
                 'name': 'action_new_content',
                 'action': 'folder_factories',
                 'permissions': ('Modify portal content',)},
                {'id': 'contents',
                 'name': 'action_folder_contents',
                 'action': 'folder_contents',
                 'permissions': ('Modify portal content',)},
                {'id': 'edit',
                 'name': 'action_edit',
                 'action': 'cpsdocument_edit_form',
                 'permissions': ('Modify portal content',)},
                {'id': 'metadata',
                 'name': 'action_metadata',
                 'action': 'cpsdocument_metadata',
                 'condition': 'not:portal/portal_membership/isAnonymousUser',
                 'permissions': ('View',)},
                {'id': 'localroles',
                 'name': 'action_local_roles',
                 'action': 'folder_localrole_form',
                 'permissions': ('Change permissions',)},
                {'id': 'boxes',
                 'name': 'action_boxes',
                 'action': 'box_manage_form',
                 'permissions': ('Manage Boxes',)},
                ),
    }

workspace_type = {
    'title': 'portal_type_Workspace_title',
    'description': 'portal_type_Workspace_description',
    'content_icon': 'workspace_icon.png',
    'content_meta_type': 'Folder',
    'product': 'CPSDefault',
    'factory': 'addFolder',
    'immediate_view': 'folder_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ('Workspace',),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folder',
    'schemas': ['metadata', 'common', 'folder'],
    'layouts': ['common', 'folder'],
    'layout_clusters': ['metadata:metadata'],
    'cps_workspace_wf': 'workspace_folder_wf',
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'folder_view',
                 'permissions': ('View',)},
                {'id': 'new_content',
                 'name': 'action_new_content',
                 'action': 'folder_factories',
                 'permissions': ('Modify portal content',)},
                {'id': 'import_documents',
                 'name': 'action_import_documents',
                 'action': 'cpsdocument_import_zip_form',
                 'visible': 0,
                 'permissions': ('Modify portal content',)},
                {'id': 'contents',
                 'name': 'action_folder_contents',
                 'action': 'folder_contents',
                 'permissions': ('Modify portal content',)},
                {'id': 'edit',
                 'name': 'action_edit',
                 'action': 'cpsdocument_edit_form',
                 'permissions': ('Modify portal content',)},
                {'id': 'metadata',
                 'name': 'action_metadata',
                 'action': 'cpsdocument_metadata',
                 'condition': 'not:portal/portal_membership/isAnonymousUser',
                 'permissions': ('View',)},
                {'id': 'localroles',
                 'name': 'action_local_roles',
                 'action': 'folder_localrole_form',
                 'permissions': ('Change permissions',)},
                {'id': 'boxes',
                 'name': 'action_boxes',
                 'action': 'box_manage_form',
                 'permissions': ('Manage Boxes',)},
                ),
    }

document_type = {
    'title': 'portal_type_Document_title',
    'description': 'portal_type_Document_description',
    'content_icon': 'document_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'document'],
    'layouts': ['common', 'document'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

flexible_type = {
    'title': 'portal_type_Flexible_title',
    'description': 'portal_type_Flexible_description',
    'content_icon': 'flexible_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_edit_form',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'flexible_content'],
    'layouts': ['common', 'flexible_content'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': ['flexible_content:flexible_content'],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

newsitem_type = {
    'title': 'portal_type_NewsItem_title',
    'description': 'portal_type_NewsItem_description',
    'content_icon': 'newsitem_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'newsitem', 'flexible_content'],
    'layouts': ['common', 'newsitem_start', 'newsitem_flexible', 'newsitem_end'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': ['newsitem_flexible:flexible_content'],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

pressrelease_type = {
    'title': 'portal_type_PressRelease_title',
    'description': 'portal_type_PressRelease_description',
    'content_icon': 'pressrelease_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'newsitem', 'flexible_content'],
    'layouts': ['common', 'newsitem_start', 'newsitem_flexible', 'newsitem_end'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': ['newsitem_flexible:flexible_content'],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

faq_type = {
    'title': 'portal_type_FAQ_title',
    'description': 'portal_type_FAQ_description',
    'content_icon': 'faqs_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ('FAQitem',),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folderishdocument',
    'schemas': ['metadata', 'common'],
    'layouts': ['common', 'faq'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    'cps_display_as_document_in_listing': 1,
    'use_content_status_history': 1,
    }

faqitem_type = {
    'title': 'portal_type_FAQitem_title',
    'description': 'portal_type_FAQitem_description',
    'content_icon': 'faq_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'faqitem'],
    'layouts': ['faqitem'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

glossary_type = {
    'title': 'portal_type_Glossary_title',
    'description': 'portal_type_Glossary_description',
    'content_icon': 'glossaries_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ('GlossaryItem',),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folderishdocument',
    'schemas': ['metadata', 'common', 'glossary'],
    'layouts': ['common', 'glossary'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    'cps_display_as_document_in_listing': 1,
    'use_content_status_history': 1,
    }

glossaryitem_type = {
    'title': 'portal_type_GlossaryItem_title',
    'description': 'portal_type_GlossaryItem_description',
    'content_icon': 'glossary_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common'],
    'layouts': ['common', 'glossaryitem'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

event_type = {
    'title': 'portal_type_Event_title',
    'description': 'portal_type_Event_description',
    'content_icon': 'event_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'event'],
    'layouts': ['common', 'event'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'display_in_cmf_calendar': 1,
    'use_content_status_history': 1,
    }

file_type = {
    'title': 'portal_type_File_title',
    'description': 'portal_type_File_description',
    'content_icon': 'attachedfile_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': [],
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'file'],
    'layouts': ['common', 'file'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'use_content_status_history': 1,
    'actions_add': ({'id': 'edit_online',
                     'name': 'action_edit_online',
                     'action': 'python:portal.getExternalEditorPath(object, "file", "file")',
                     'condition': ('python:object is not None '
                                   'and object.getContent().file is not None '
                                   'and modules["Products.CPSUtil.integration"].isProductPresent("Products.ExternalEditor")'),
                     'permissions': ('Modify portal content',)},
                ),
    }

zippedhtml_type = {
    'title': 'portal_type_ZippedHtml_title',
    'description': 'portal_type_ZippedHtml_description',
    'content_icon': 'zippedhtml_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'zippedhtml'],
    'layouts': ['common', 'zippedhtml'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'display_in_cmf_calendar': 1,
    'use_content_status_history': 1,
    }

link_type = {
    'title': 'portal_type_Link_title',
    'description': 'portal_type_Link_description',
    'content_icon': 'link_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common'],
    'layouts': ['link'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'display_in_cmf_calendar': 1,
    'use_content_status_history': 1,
    }

imagegallery_type = {
    'title': 'portal_type_ImageGallery_title',
    'description': 'portal_type_ImageGallery_description',
    'content_icon': 'imgallery_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ('Image',),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folderishdocument',
    'schemas': ['metadata', 'common', 'imagegallery'],
    'layouts': ['common', 'imagegallery'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    'cps_display_as_document_in_listing': 1,
    'use_content_status_history': 1,
    }

image_type = {
    'title': 'portal_type_Image_title',
    'description': 'portal_type_Image_description',
    'content_icon': 'image_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': [],
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common'],
    'layouts': ['common', 'image'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

book_type = {
    'title': 'portal_type_Book_title',
    'description': 'portal_type_Book_description',
    'content_icon': 'book_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ('Page','Chapter'),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folderishdocument',
    'schemas': ['metadata', 'common', 'book'],
    'layouts': ['common', 'book'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    'cps_display_as_document_in_listing': 0,
    'use_content_status_history': 1,
    }

chapter_type = {
    'title': 'portal_type_Chapter_title',
    'description': 'portal_type_Chapter_description',
    'content_icon': 'book_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ('Page',),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folderishdocument',
    'cps_display_as_document_in_listing': 0,
    'schemas': ['metadata', 'common', 'book'],
    'layouts': ['common', 'chapter'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': (),
    'storage_methods': (),
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    'cps_display_as_document_in_listing': 1,
    'use_content_status_history': 1,
}

page_type = {
    'title': 'portal_type_Page_title',
    'description': 'portal_type_Page_description',
    'content_icon': 'page_icon.png',
    'content_meta_type': 'CPS Document',
    'product': 'CPSDocument',
    'factory': 'addCPSDocument',
    'immediate_view': 'cpsdocument_edit_form',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'flexible_content'],
    'layouts': ['page', 'common', 'flexible_content'],
    'layout_clusters': ['metadata:metadata'],
    'flexible_layouts': ['flexible_content:flexible_content'],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

types = {}
types['Section'] = section_type
types['Workspace'] = workspace_type
types['Document'] = document_type
types['Flexible'] = flexible_type
types['News Item'] = newsitem_type
types['Press Release'] = pressrelease_type
types['FAQ'] = faq_type
types['FAQitem'] = faqitem_type
types['Glossary'] = glossary_type
types['GlossaryItem'] = glossaryitem_type
types['File'] = file_type
types['ZippedHtml'] = zippedhtml_type
types['EventDoc'] = event_type
types['Link'] = link_type
types['Image'] = image_type
types['ImageGallery'] = imagegallery_type
types['Book'] = book_type
types['Chapter'] = chapter_type
types['Page'] = page_type

# other products
try:
    types.update(context.getCPSCollectorTypes())
except AttributeError:
    pass
try:
    types.update(context.getCPSMailBoxerDocumentTypes())
except AttributeError, e:
    pass



if loadcustom:
    ctypes = context.getCustomDocumentTypes()
    types.update(ctypes)

return types
