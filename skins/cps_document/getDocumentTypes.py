##parameters=
#$Id$
"""
Here are defined list of portal type created with CPSDocument
"""

flexible_type = {
    'title': 'portal_type_Flexible_title',
    'description': 'portal_type_Flexible_description',
    'content_icon': 'flexible_icon.gif',
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
    'schemas': ['common', 'flexible_content'],
    'layouts': ['common', 'flexible_content'],
    'flexible_layouts': ['flexible_content:flexible_content'],
    'storage_methods': [],
    }

faq_type = {
    'title': 'portal_type_FAQ_title',
    'description': 'portal_type_FAQ_description',
    'content_icon': 'faqs_icon.gif',
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
    'schemas': ['faq'],
    'layouts': ['faq'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    }

faqitem_type = {
    'title': 'portal_type_FAQitem_title',
    'description': 'portal_type_FAQitem_description',
    'content_icon': 'faq_icon.gif',
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
    'schemas': ['faqitem'],
    'layouts': ['faqitem'],
    'flexible_layouts': [],
    'storage_methods': [],
    }

glossary_type = {
    'title': 'portal_type_Glossary_title',
    'description': 'portal_type_Glossary_description',
    'content_icon': 'glossary_icon.gif',
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
    'schemas': ['glossary'],
    'layouts': ['glossary'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    }

glossaryitem_type = {
    'title': 'portal_type_GlossaryItem_title',
    'description': 'portal_type_GlossaryItem_description',
    'content_icon': 'glossary_icon.gif',
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
    'schemas': ['glossaryitem'],
    'layouts': ['glossaryitem'],
    'flexible_layouts': [],
    'storage_methods': [],
    }

news_type = {
    'title': 'portal_type_News_title',
    'description': 'portal_type_News_description',
    'content_icon': 'news_icon.gif',
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
    'schemas': ['news'],
    'layouts': ['news'],
    'flexible_layouts': [],
    'storage_methods': [],
    }

event_type = {
    'title': 'portal_type_Event_title',
    'description': 'portal_type_Event_description',
    'content_icon': 'event_icon.gif',
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
    'schemas': ['event'],
    'layouts': ['event'],
    'flexible_layouts': [],
    'storage_methods': [],
    'display_in_cmf_calendar': 1,
    }

file_type = {
    'title': 'portal_type_File_title',
    'description': 'portal_type_File_description',
    'content_icon': 'attachedfile_icon.gif',
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
    'schemas': ['file'],
    'layouts': ['file'],
    'flexible_layouts': [],
    'storage_methods': [],
    }

link_type = {
    'title': 'portal_type_Link_title',
    'description': 'portal_type_Link_description',
    'content_icon': 'link_icon.gif',
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
    'schemas': ['link'],
    'layouts': ['link'],
    'flexible_layouts': [],
    'storage_methods': [],
    'display_in_cmf_calendar': 1,
    }

imagegallery_type = {
    'title': 'portal_type_ImageGallery_title',
    'description': 'portal_type_ImageGallery_description',
    'content_icon': 'imgallery_icon.gif',
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
    'schemas': ['imagegallery'],
    'layouts': ['imagegallery'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folderish_content_wf',
    }

image_type = {
    'title': 'portal_type_Image_title',
    'description': 'portal_type_Image_description',
    'content_icon': 'image_icon.gif',
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
    'schemas': ['image'],
    'layouts': ['image'],
    'flexible_layouts': [],
    'storage_methods': [],
    }

dummy_form_type = {
    'title': 'portal_type_Dummy_Form',
    'description': 'portal_type_Dummy_description',
    'content_icon': 'document_icon.gif',
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
    'schemas': ['dummy_form'],
    'layouts': ['dummy_form'],
    'flexible_layouts': [],
    'storage_methods': [],
    }

types = {}

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
#types['Dummy Form'] = dummy_form_type

ctypes = context.getCustomDocumentTypes()

types.update(ctypes)

return types
