## Script (Python) "getDocumentTypes"
##parameters=
#$Id$
"""
Here are defined list of portal type created with CPSDocument
"""
faq_type = {
    'title': 'portal_type_FAQ_title',
    'description': 'portal_type_FAQ_description',
    'content_icon': 'faq_icon.gif',
    'content_meta_type': 'CPS Document',
    'permission': 'Add portal content',
    'immediate_view': 'cpsdocument_edit_form',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['faq'],
    'default_layout': 'faq',
    'layout_style_prefix': 'layout_dummy_',
    'flexible_layouts': [],
    'storage_methods': [],
    }

news_type = {
    'title': 'portal_type_News_title',
    'description': 'portal_type_News_description',
    'content_icon': 'news_icon.gif',
    'content_meta_type': 'CPS Document',
    'permission': 'Add portal content',
    'immediate_view': 'cpsdocument_edit_form',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['news'],
    'default_layout': 'news',
    'layout_style_prefix': 'layout_default_',
    'flexible_layouts': [],
    'storage_methods': [],
    }

dummy_form_type = {
    'title': 'portal_type_Dummy_Form',
    'description': 'portal_type_Dummy_description',
    'content_icon': 'document_icon.gif',
    'content_meta_type': 'CPS Document',
    'permission': 'Add portal content',
    'immediate_view': 'cpsdocument_edit_form',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': (),
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['dummy_form'],
    'default_layout': 'dummy_form',
    'layout_style_prefix': 'layout_form_',
    'flexible_layouts': [],
    'storage_methods': [],
    }
    
breve_type = {
    'title': 'Brève',
    'description': '',
    'content_icon': 'news_item.gif',
    'content_meta_type': 'CPS Document',
    'permission': 'Add portal content',
    'immediate_view': 'cpsdocument_edit_form',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': [],
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'schemas': ['breve'],
    'default_layout': 'breve',
    'layout_style_prefix': 'layout_default_',
    'flexible_layouts': [],
    'storage_methods': [],
    }

fichier_type = {
    'title': 'Fichier',
    'description': '',
    'content_icon': '',
    'content_meta_type': 'CPS Document',
    'permission': 'Add portal content',
    'immediate_view': 'cpsdocument_edit_form',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': [],
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'folderishdocument',
    'schemas': ['fichier'],
    'default_layout': 'fichier',
    'layout_style_prefix': 'layout_default_',
    'flexible_layouts': [],
    'storage_methods': [],
    }

types = {}

types['FAQ'] = faq_type
types['News'] = news_type
types['Dummy Form'] = dummy_form_type
types['Breve'] = breve_type
types['Fichier'] = fichier_type

ctypes = context.getCustomDocumentTypes()

types.update(ctypes)

return types
