## Script (Python) "getDocumentLayouts"
##parameters=
# $Id$
"""
Here are defined the list of layouts to be registred
Please, follow the same pattern to add new layouts
"""

#########################################################
# FAQ LAYOUT
#########################################################

faq_layout = {
    'widgets': {
        'title': {
            'type': 'String Widget',
            'data': {
                'fields': ['title'],
                'is_i18n': 0,
                'label_edit': 'FAQ short question',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': 'FAQ short question for section display',
                'css_class': 'title',
                'is_required': 0,
                'display_width': 20,
                'size_max': 0,
            },
        },
        'description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['description'],
                'is_i18n': 0,
                'label_edit': 'FAQ answer resume',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': 'FAQ answer resume for section display',
                'css_class': 'description',
                'is_required': 0,
                'width': 40,
                'height': 5,
                'render_mode': 'stx',
            },
        },
        'question': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['question'],
                'is_i18n': 0,
                'label_edit': 'FAQ question',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': 'FAQ full question',
                'css_class': 'title',
                'is_required': 0,
                'width': 40,
                'height': 5,
                'render_mode': 'stx',
            },
        },
        'answer': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['answer'],
                'is_i18n': 0,
                'label_edit': 'FAQ answer',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': 'FAQ full answer',
                'css_class': 'stx',
                'is_required': 0,
                'width': 40,
                'height': 5,
                'render_mode': 'stx',
            },
        },
    },
    'layout': {
        'ncols': 1,
        'rows': [
            [{'ncols': 1, 'widget_id': 'title'},
                ],
            [{'ncols': 1, 'widget_id': 'description'},
                ],
            [{'ncols': 1, 'widget_id': 'question'},
                ],
            [{'ncols': 1, 'widget_id': 'answer'},
                ],
            ],
        },
    }

#########################################################
# DUMMY FORM LAYOUT
#########################################################

dummy_form_layout = {
    'widgets': {
        'title': {
            'type': 'String Widget',
            'data': {
                'fields': ['title'],
                'is_i18n': 0,
                'label_edit': 'Dummy Form title field',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': 'Title for a dummy form',
                'css_class': 'title',
                'is_required': 0,
                'display_width': 20,
                'size_max': 0,
            },
        },
        'description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['description'],
                'is_i18n': 0,
                'label_edit': 'Dummy Form Description field',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': 'Description field for a dummy form',
                'css_class': 'description',
                'is_required': 0,
                'width': 40,
                'height': 5,
                'render_mode': 'stx',
            },
        },
    },
    'layout': {
        'ncols': 1,
        'rows': [
            [{'ncols': 1, 'widget_id': 'title'},
                ],
            [{'ncols': 1, 'widget_id': 'description'},
                ],
            ],
        },
    }

#########################################################
# NEWS LAYOUT
#########################################################

news_layout = {
    'widgets': {
        'preview': {
            'type': 'Image Widget',
            'data': {
                'fields': ['preview'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_preview_label_edit',
                'label': '',
                'hidden_view': 1,
                'description': 'cpsdoc_News_preview_description',
                'deletable': 1,
                'display_width': 200,
                'display_height': 150,
                'size_max': 1024*1024,
            },
        },
        'attachedFile': {
            'type': 'File Widget',
            'data': {
                'fields': ['attachedFile',
                           'attachedFile_text',
                           'attachedFile_html'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_attachedFile_label_edit',
                'label': 'cpsdoc_News_attachedFile_label',
                'hidden_empty': 1,
                'description': 'cpsdoc_News_attachedFile_description',
                'deletable': 1,
                'size_max': 3*1024*1024,
            },
        },
        'newsdate': {
            'type': 'Date Widget',
            'data': {
                'fields': ['newsdate'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_News_newsdate_label_edit',
                'label': 'cpsdoc_News_newsdate_label',
                'description': 'cpsdoc_News_newsdate_description',
                'css_class': 'dtitle5 dright',
                'view_format': 'medium',
                'time_setting': 1,
            },
        },
        'title': {
            'type': 'String Widget',
            'data': {
                'fields': ['title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_title_label_edit',
                'label': '',
                'description': 'cpsdoc_News_title_description',
                'css_class': 'dtitle',
                'display_width': 30,
                'size_max': 72,
            },
        },
        'photo': {
            'type': 'Image Widget',
            'data': {
                'fields': ['photo'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_photo_label_edit',
                'label': '',
                'description': 'cpsdoc_News_photo_description',
                'css_class': 'dleft',
                'display_width': 250,
                'display_height': 150,
                'size_max': 2*1024*1024,
            },
        },
        'description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_description_label_edit',
                'label': '',
                'description': 'cpsdoc_News_description_description',
                'css_class': 'ddescription',
                'width': 20,
                'height': 5,
                'render_mode': 'stx',
            },
        },
        'theme': {
            'type': 'Select Widget',
            'data': {
                'fields': ['theme'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_theme_label_edit',
                'label': '',
                'hidden_view': 1,
                'description': 'cpsdoc_theme_description',
                'vocabulary': 'dummy_voc',
            },
        },
        'longTitle': {
            'type': 'String Widget',
            'data': {
                'fields': ['longTitle'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_longTitle_label_edit',
                'label': '',
                'description': 'cpsdoc_News_longTitle_description',
                'css_class': 'dtitle2',
                'is_required': 1,
                'display_width': 72,
                'size_max': 72,
            },
        },
        'content': {
            'type': 'Rich Text Editor Widget',
            'data': {
                'fields': ['content'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_content_label_edit',
                'label': '',
                'description': 'cpsdoc_News_content_description',
                'css_class': 'dcontent',
                'width': 40,
                'height': 25,
                'render_mode': 'stx',
            },
        },
    },
    'layout': {
    'ncols': 2,
        'rows': [
            [{'ncols': 1, 'widget_id': 'theme'},
             ],
            [{'ncols': 1, 'widget_id': 'title'},
             {'ncols': 1, 'widget_id': 'newsdate'},
             ],
            [{'ncols': 1, 'widget_id': 'longTitle'},
             ],
            [{'ncols': 1, 'widget_id': 'description'},
             ],
            [{'ncols': 1, 'widget_id': 'photo'},
             {'ncols': 1, 'widget_id': 'preview'},
             ],
            [{'ncols': 1, 'widget_id': 'content'},
             ],
            [{'ncols': 1, 'widget_id': 'attachedFile'},
             ],
            ],
        },
    }

#########################################################
# Breve LAYOUT
#########################################################

breve_layout = {
    'widgets': {
        'title': {
            'type': 'String Widget',
            'data': {
                'fields': ['title'],
                'is_i18n': 0,
                'label_edit': 'Titre',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'is_required': 0,
                'display_width': 20,
                'size_max': 0,
            },
        },
        'description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['description'],
                'is_i18n': 0,
                'label_edit': 'Description',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'is_required': 0,
                'width': 50,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'date': {
            'type': 'Date Widget',
            'data': {
                'fields': ['date'],
                'is_i18n': 0,
                'label_edit': 'Date',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'is_required': 0,
                'view_format': '%d/%m/%Y',
                'view_format_none': '-',
            },
        },
        'image': {
            'type': 'Image Widget',
            'data': {
                'fields': ['image'],
                'is_i18n': 0,
                'label_edit': 'Image',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'deletable': 1,
                'maxsize': 2097152,
                'display_width': 0,
                'display_height': 0,
            },
        },
        'body': {
            'type': 'Rich Text Editor Widget',
            'data': {
                'fields': ['body'],
                'is_i18n': 0,
                'label_edit': 'Corps de la brève',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'width': 40,
                'height': 5,
                'render_mode': 'pre',
            },
        },
    },
    'layout': {
        'ncols': 2,
        'rows': [
            [{'ncols': 1, 'widget_id': 'title'},
                            {'ncols': 1, 'widget_id': 'date'},
                ],
            [{'ncols': 2, 'widget_id': 'description'},
                ],
            [{'ncols': 2, 'widget_id': 'image'},
                ],
            [{'ncols': 2, 'widget_id': 'body'},
                ],
            ],
        },
    }

#########################################################
# Fichier LAYOUT
#########################################################

fichier_layout = {
    'widgets': {
        'title': {
            'type': 'String Widget',
            'data': {
                'fields': ['title'],
                'is_i18n': 0,
                'label_edit': 'Titre',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'is_required': 1,
                'display_width': 20,
                'size_max': 0,
            },
        },
        'description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['description'],
                'is_i18n': 0,
                'label_edit': 'Description',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'is_required': 0,
                'width': 50,
                'height': 3,
                'render_mode': 'text',
            },
        },
        'file': {
            'type': 'File Widget',
            'data': {
                'fields': ['file'],
                'is_i18n': 0,
                'label_edit': 'Fichier',
                'label': '',
                'hidden_view': 0,
                'hidden_edit': 0,
                'hidden_empty': 0,
                'description': '',
                'css_class': '',
                'deletable': 1,
            },
        },
    },
    'layout': {
        'ncols': 1,
        'rows': [
            [{'ncols': 1, 'widget_id': 'title'},
                ],
            [{'ncols': 1, 'widget_id': 'description'},
                ],
            [{'ncols': 1, 'widget_id': 'file'},
                ],
            ],
        },
    }

###########################################################
# END OF LAYOUTS DEFINITIONS
###########################################################

layouts = {}

#
# Building the dictionnary of layouts for the installer
#

layouts['faq'] = faq_layout
layouts['dummy_form'] = dummy_form_layout
layouts['news'] = news_layout
layouts['breve'] = breve_layout
layouts['fichier'] = fichier_layout

clayouts = context.getCustomDocumentLayouts()

layouts.update(clayouts)

return layouts
