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
    'cps_workspace_wf': 'workspace_folder_wf',
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
    'flexible_layouts': ['flexible_content:flexible_content'],
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
    'flexible_layouts': [],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

news_type = {
    'title': 'portal_type_News_title',
    'description': 'portal_type_News_description',
    'content_icon': 'news_icon.png',
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
    'schemas': ['metadata', 'common', 'news'],
    'layouts': ['common', 'news'],
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
    'flexible_layouts': [],
    'storage_methods': [],
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
    'flexible_layouts': ['flexible_content:flexible_content'],
    'storage_methods': [],
    'use_content_status_history': 1,
    }

types = {}
types['Section'] = section_type
types['Workspace'] = workspace_type
types['Flexible'] = flexible_type
types['FAQ'] = faq_type
types['FAQitem'] = faqitem_type
types['Glossary'] = glossary_type
types['GlossaryItem'] = glossaryitem_type
types['News'] = news_type
types['File'] = file_type
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