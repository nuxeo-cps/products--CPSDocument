##parameters=
# $Id$
"""
Here are defined the list of layouts to be registred
Please, follow the same pattern to add new layouts
"""

#########################################################
# SHARED LAYOUTS
#########################################################
# metadata layout
metadata_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'label_title',
                'label': 'label_title',
                'css_class': 'dtitle',
                'display_width': 72,
                'size_max': 100,
            },
        },
        'Description': {
            'type': 'Text Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'label_description',
                'label': 'label_description',
                'css_class': 'ddescription',
                'width': 72,
                'height': 5,
                'render_format': 'text',
            },
        },
        'Subject': {
            'type': 'Lines Widget',
            'data': {
                'fields': ['Subject'],
                'is_i18n': 1,
                'label_edit': 'label_subject',
                'label': 'label_subject',
            },
        },
        'Contributors': {
            'type': 'Lines Widget',
            'data': {
                'fields': ['Contributors'],
                'is_i18n': 1,
                'label_edit': 'label_contributors',
                'label': 'label_contributors',
            },
        },
        'CreationDate': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['CreationDate'],
                'is_i18n': 1,
                'label_edit': 'time_creation_date',
                'label': 'time_creation_date',
                'view_format': 'long',
                'readonly_layout_modes': ['create', 'edit'],
                'hidden_layout_modes': ['create'],
            },
        },
        'ModificationDate': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['ModificationDate'],
                'is_i18n': 1,
                'label_edit': 'time_last_modified',
                'label': 'time_last_modified',
                'view_format': 'long',
                'readonly_layout_modes': ['create', 'edit'],
                'hidden_layout_modes': ['create'],
            },
        },
        'EffectiveDate': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['EffectiveDate'],
                'is_i18n': 1,
                'label_edit': 'time_effective_date',
                'label': 'time_effective_date',
                'view_format': 'long',
            },
        },
        'ExpirationDate': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['ExpirationDate'],
                'is_i18n': 1,
                'label_edit': 'time_expiration_date',
                'label': 'time_expiration_date',
                'view_format': 'long',
                'time_setting': 0,
            },
        },
        'Format': {
            'type': 'String Widget',
            'data': {
                'fields': ['Format'],
                'is_i18n': 1,
                'label_edit': 'label_format',
                'label': 'label_format',
                'readonly_layout_modes': ['create', 'edit'],
                'display_width': 30,
                'size_max': 40,
            },
        },
        'Language': {
            'type': 'String Widget',
            'data': {
                'fields': ['Language'],
                'is_i18n': 1,
                'label_edit': 'label_language',
                'label': 'label_language',
                'readonly_layout_modes': ['create', 'edit'],
                'display_width': 4,
                'size_max': 4,
            },
        },
        'Rights': {
            'type': 'String Widget',
            'data': {
                'fields': ['Rights'],
                'is_i18n': 1,
                'label_edit': 'label_rights',
                'label': 'label_rights',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'Creator': {
            'type': 'String Widget',
            'data': {
                'fields': ['Creator'],
                'is_i18n': 1,
                'label_edit': 'label_creator',
                'label': 'label_creator',
                'readonly_layout_modes': ['create', 'edit'],
                'display_width': 40,
                'size_max': 50,
            },
        },

    },
    'layout': {
        'style_prefix': 'layout_metadata_',
        'ncols': 2,
        'rows': [
            [{'ncols': 2, 'widget_id': 'Title'},],
            [{'ncols': 2, 'widget_id': 'Description'},],
            [{'widget_id': 'Subject'},
             {'widget_id': 'Rights'},],
            [{'widget_id': 'EffectiveDate'},
             {'widget_id': 'ExpirationDate'},],
            [{'widget_id': 'Contributors'},
             {'widget_id': 'Creator'},],
            [{'widget_id': 'Format'},
             {'widget_id': 'Language'},],
            [{'widget_id': 'CreationDate'},
             {'widget_id': 'ModificationDate'},],
            ],
        },
    }



# example of a common header layout
common_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'label': '',
                'css_class': 'dtitle',
                'display_width': 72,
                'size_max': 100,
            },
        },
        'Description': {
            'type': 'Text Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'label': '',
                'css_class': 'ddescription',
                'width': 72,
                'height': 5,
                'render_format': 'text',
            },
        },
        'date': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['date'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_date_label_edit',
                'label': 'cpsdoc_date_label',
                'css_class': 'dtitle5 dright dflush',
                'view_format': 'short',
                'time_setting': 0,
            },
        },
        'theme': {
            'type': 'Select Widget',
            'data': {
                'fields': ['theme'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_theme_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': 'cpsdoc_theme_description',
                'vocabulary': 'dummy_voc',
            },
        },
        'preview': {
            'type': 'Image Widget',
            'data': {
                'title': 'cpsdoc_preview_title',
                'fields': ['preview'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_preview_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'deletable': 1,
                'display_width': 64,
                'display_height': 64,
                'size_max': 1024*1024,
            },
        },

    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 3,
        'rows': [
            [{'ncols': 3, 'widget_id': 'Title'},
             ],
            [{'ncols': 3, 'widget_id': 'Description'},
             ],
            [{'ncols': 1, 'widget_id': 'preview'},
             {'ncols': 1, 'widget_id': 'theme'},
             {'ncols': 1, 'widget_id': 'date'},
             ],
            ],
        },
    }

# a flexible content
flexible_content_layout = {
    'widgets': {
        'content': {
            'type': 'Text Widget',
            'data': {
                'title': 'cpsdoc_flex_content_title',
                'fields': ['content', 'content_format', 'content_position'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_content_label_edit',
                'label': '',
                'css_class': 'dcontent',
                'width': 72,
                'height': 15,
                'render_format': 'html',
                'render_position': 'normal',
                'configurable': 'position and format',
                },
            },
        'attachedFile': {
            'type': 'AttachedFile Widget',
            'data': {
                'title': 'cpsdoc_flex_attachedFile_title',
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_attachedFile_label_edit',
                'label': 'cpsdoc_flex_attachedFile_label',
                'css_class': 'dflush',
                'hidden_empty': 1,
                'deletable': 1,
                'size_max': 3*1024*1024,
                },
            },
        'photo': {
            'type': 'Photo Widget',
            'data': {
                'title': 'cpsdoc_flex_photo_title',
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_photo_label_edit',
                'label': '',
                'configurable': 'position',
                'size_max': 2*1024*1024,
            },
        },
        'link': {
            'type': 'Link Widget',
            'data': {
                'title': 'cpsdoc_flex_link_title',
                'fields': ['?'],
                'is_i18n': 1,
                'is_required': 0,
                'label_edit': 'cpsdoc_flex_link_label_edit',
                'hidden_empty': 1,
                'deletable': 1,
            },
        },
    },
    'layout': {
        'flexible_widgets': ['content:4', 'link',
                            'photo:2', 'attachedFile:4'],
        'style_prefix': 'layout_default_',
        'ncols': 1,
        'rows': [
            [{'widget_id': 'content'},
             ],
            ],
        },
    }



#########################################################
# FAQ LAYOUT
#########################################################

faqitem_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_faq_question_label_edit',
                'label': '',
                'description': 'FAQ short question for section display',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 40,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_faq_long_question_label_edit',
                'label': '',
                'description': 'FAQ long question',
                'css_class': 'ddescription',
                'width': 40,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'content': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['content'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_faq_answer_label_edit',
                'label': 'cpsdoc_faq_answer_label',
                'description': 'FAQ answer',
                'css_class': 'dcontent',
                'is_required': 1,
                'width': 40,
                'height': 5,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [
            [{'widget_id': 'title'},
                ],
            [{'widget_id': 'description'},
                ],
            [{'widget_id': 'content'},
                ],
            ],
        },
    }


faq_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'label': '',
                'description': 'FAQ title',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 40,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'label': '',
                'description': 'FAQ description',
                'css_class': 'ddescription',
                'width': 40,
                'height': 5,
                'render_mode': 'text',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_faq_',
        'rows': [
            [{'widget_id': 'title'},
                ],
            [{'widget_id': 'description'},
                ],
            ],
        },
    }

#########################################################
# Glossary LAYOUT
#########################################################

glossaryitem_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_glossary_term_label_edit',
                'label': '',
                'description': 'Glossary entry key',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 40,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_glossary_expl_label_edit',
                'label': '',
                'description': 'Glossary entry explanation',
                'css_class': 'ddescription',
                'width': 40,
                'height': 5,
                'render_mode': 'text',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [
            [{'widget_id': 'title'},
                ],
            [{'widget_id': 'description'},
                ],
            ],
        },
    }


glossary_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'label': '',
                'description': 'Glossary title',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 40,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'label': '',
                'description': 'Glossary description',
                'css_class': 'ddescription',
                'width': 40,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'display_all': {
            'type': 'Int Widget',
            'data': {
                'fields': ['display_all'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_glossary_dispall_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'is_limited': 1,
                'min_value': 0,
                'max_value': 1,
                'thousands_separator': '',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_glossary_',
        'rows': [
            [{'widget_id': 'title'},
                ],
            [{'widget_id': 'description'},
                ],
            [{'widget_id': 'display_all'},
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
                'hidden_layout_modes': ['view'],
                'description': 'cpsdoc_News_preview_description',
                'deletable': 1,
                'display_width': 200,
                'display_height': 150,
                'size_max': 1024*1024,
            },
        },
        'attachedFile': {
            'type': 'AttachedFile Widget',
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
            'type': 'DateTime Widget',
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
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
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
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_description_label_edit',
                'label': '',
                'description': 'cpsdoc_News_description_description',
                'css_class': 'ddescription',
                'width': 60,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'theme': {
            'type': 'Select Widget',
            'data': {
                'fields': ['theme'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_theme_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
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
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
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
# FILE LAYOUT
#########################################################

file_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 60,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'description': '',
                'css_class': 'ddescription',
                'is_required': 0,
                'width': 60,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'file': {
            'type': 'AttachedFile Widget',
            'data': {
                'fields': ['file',
                           'file_text',
                           'file_html'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_News_attachedFile_label_edit',
                'label': 'cpsdoc_News_attachedFile_label',
                'hidden_empty': 1,
                'description': 'cpsdoc_News_attachedFile_description',
                'deletable': 1,
                'size_max': 3*1024*1024,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
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

#########################################################
# EVENT LAYOUT
#########################################################
event_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 60,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'description': '',
                'css_class': 'ddescription',
                'is_required': 0,
                'width': 60,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'start': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['start'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_Event_start_label_edit',
                'label': 'cpsdoc_Event_start_label',
                'css_class': 'dbold',
                'view_format': 'medium',
                'time_setting': 1,
            },
        },
        'end': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['end'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_Event_end_label_edit',
                'label': 'cpsdoc_Event_end_label',
                'css_class': 'dbold dright',
                'view_format': 'medium',
                'time_setting': 1,
            },
        },
        'content': {
            'type': 'Rich Text Editor Widget',
            'data': {
                'fields': ['content'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_Event_content_label_edit',
                'label': '',
                'description': 'cpsdoc_Event_content_description',
                'css_class': 'dcontent',
                'width': 40,
                'height': 25,
            },
        },
        'attachedFile': {
            'type': 'AttachedFile Widget',
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
    },
    'layout': {
        'style_prefix': 'layout_event_',
        'ncols': 2,
        'rows': [
            [{'ncols': 1, 'widget_id': 'title'},],
            [{'ncols': 1, 'widget_id': 'description'},],
            [{'ncols': 1, 'widget_id': 'start'},
             {'ncols': 1, 'widget_id': 'end'},],
            [{'ncols': 1, 'widget_id': 'content'},],
            [{'ncols': 1, 'widget_id': 'attachedFile'},],
            ],
        },
    }


#########################################################
# LINK LAYOUT
#########################################################

link_layout = {
    'widgets': {
        'link': {
            'type': 'Link Widget',
            'data': {
                'fields': ['href',
                           'title',
                           'description'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_Link_label_edit',
                'hidden_empty': 1,
                'deletable': 1,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 1,
        'rows': [
            [{'ncols': 1, 'widget_id': 'link'},
                ],
            ],
        },
    }

#########################################################
# IMAGE LAYOUT
#########################################################

image_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 60,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'description': '',
                'css_class': 'ddescription',
                'is_required': 0,
                'width': 60,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'preview': {
            'type': 'Image Widget',
            'data': {
                'fields': ['preview'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_Image_label_edit',
                'label': '',
                'display_width': 640,
                'display_height': 600,
                'size_max': 3*1024*1024,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [
            [{'widget_id': 'title'},
                ],
            [{'widget_id': 'description'},
                ],
            [{'widget_id': 'preview'},
                ],
            ],
        },
    }

imagegallery_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'label': '',
                'description': 'Image Gallery title',
                'css_class': 'dtitle',
                'is_required': 1,
                'display_width': 40,
                'size_max': 72,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'label': '',
                'description': 'Image Gallery description',
                'css_class': 'ddescription',
                'width': 40,
                'height': 5,
                'render_mode': 'text',
            },
        },
        'preview_width': {
            'type': 'Int Widget',
            'data': {
                'fields': ['preview_width'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_imgallery_width_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'is_limited': 1,
                'min_value': 0.0,
                'max_value': 65536.0,
                'thousands_separator': '',
            },
        },
        'preview_height': {
            'type': 'Int Widget',
            'data': {
                'fields': ['preview_height'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_imgallery_height_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'is_limited': 1,
                'min_value': 0.0,
                'max_value': 65536.0,
                'thousands_separator': '',
            },
        },
        'nb_items': {
            'type': 'Int Widget',
            'data': {
                'fields': ['nb_items'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_imgallery_items_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'is_limited': 1,
                'min_value': 0.0,
                'max_value': 65536.0,
                'thousands_separator': '',
            },
        },
        'nb_cols': {
            'type': 'Int Widget',
            'data': {
                'fields': ['nb_cols'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_imgallery_col_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'is_limited': 1,
                'min_value': 0.0,
                'max_value': 128.0,
                'thousands_separator': '',
            },
        }
    },
    'layout': {
        'style_prefix': 'layout_imagegallery_',
        'ncols': 2,
        'rows': [
            [{'widget_id': 'title'},
                ],
            [{'widget_id': 'description'},
                ],
            [{'widget_id': 'preview_width'},
             { 'widget_id': 'preview_height'},
                ],
            [{'widget_id': 'nb_items'},
             {'widget_id': 'nb_cols'},
                ],
            ],
        },
    }



#########################################################
# DUMMY FORM LAYOUT
#########################################################

dummy_form_layout = {
    'widgets': {
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 0,
                'label_edit': 'Dummy Form title field',
                'label': '',
                'description': 'Title for a dummy form',
                'css_class': 'title',
                'is_required': 0,
                'display_width': 20,
                'size_max': 0,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 0,
                'label_edit': 'Dummy Form Description field',
                'label': '',
                'description': 'Description field for a dummy form',
                'css_class': 'description',
                'is_required': 0,
                'width': 60,
                'height': 5,
                'render_mode': 'text',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_form_',
        'ncols': 1,
        'rows': [
            [{'ncols': 1, 'widget_id': 'title'},
                ],
            [{'ncols': 1, 'widget_id': 'description'},
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
layouts['metadata'] = metadata_layout
layouts['common'] = common_layout
layouts['flexible_content'] = flexible_content_layout

layouts['faq'] = faq_layout
layouts['faqitem'] = faqitem_layout
layouts['glossary'] = glossary_layout
layouts['glossaryitem'] = glossaryitem_layout
layouts['news'] = news_layout
layouts['file'] = file_layout
layouts['event'] = event_layout
layouts['link'] = link_layout
layouts['image'] = image_layout
layouts['imagegallery'] = imagegallery_layout
#layouts['dummy_form'] = dummy_form_layout

clayouts = context.getCustomDocumentLayouts()

layouts.update(clayouts)

return layouts
