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
    'immediate_view': 'cpsdocument_edit_form',
    'schemas': ['faq'],
    'default_layout': 'faq',
    'layout_style_prefix': 'layout_dummy_',
    'cps_proxy_type': 'document',
     }

news_type = {
    'title': 'portal_type_News_title',
    'description': 'portal_type_News_description',
    'content_icon': 'news_icon.gif',
    'immediate_view': 'cpsdocument_edit_form',
    'schemas': ['news'],
    'default_layout': 'news',
    'layout_style_prefix': 'layout_default_',
    'cps_proxy_type': 'document',
    }

dummy_form_type = {
    'title': 'portal_type_Dummy_Form',
    'description': 'portal_type_Dummy_description',
    'content_icon': 'document_icon.gif',
    'immediate_view': 'cpsdocument_edit_form',
    'schemas': ['dummy_form'],
    'default_layout': 'dummy_form',
    'layout_style_prefix': 'layout_form_',
    'cps_proxy_type': 'document',
    }

types = {}

types['faq'] = faq_type
types['news'] = news_type
types['dummy_form'] = dummy_form_type

ctypes = context.getCustomDocumentTypes()

types.update(ctypes)

return types
