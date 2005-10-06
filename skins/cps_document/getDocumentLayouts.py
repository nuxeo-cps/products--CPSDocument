##parameters=loadcustom=1
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
                'display_width': 72,
                'size_max': 200,
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
        'PortalType': {
            'type': 'Method Widget',
            'data': {
                'is_i18n': 1,
                'label_edit': 'label_portal_type',
                'label': 'label_portal_type',
                'readonly_layout_modes': ['create', 'edit'],
                'render_method': 'widget_portal_type',
            },
        },
        'Subject': {
            'type': 'Subject Widget',
            'data': {
                'fields': ['Subject'],
                'is_i18n': 1,
                'label_edit': 'label_subject',
                'label': 'label_subject',
                'vocabulary': 'subject_voc',
                'help': 'help_dc_subject',
                'translated': 1,
                'size': 5,
            },
        },
        'Contributors': {
            'type': 'Lines Widget',
            'data': {
                'fields': ['Contributors'],
                'is_i18n': 1,
                'label_edit': 'label_contributors',
                'label': 'label_contributors',
                'readonly_layout_modes': ['create', 'edit'],
                'help': 'help_dc_contirbutors',
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
        'Source': {
            'type': 'String Widget',
            'data': {
                'fields': ['Source'],
                'is_i18n': 1,
                'label_edit': 'label_source',
                'label': 'label_source',
                'display_width': 30,
                'size_max': 80,
                'help': 'help_dc_source',
            },
        },
        'Coverage': {
            'type': 'String Widget',
            'data': {
                'fields': ['Coverage'],
                'is_i18n': 1,
                'label_edit': 'label_coverage',
                'label': 'label_coverage',
                'display_width': 30,
                'size_max': 80,
                'help': 'help_dc_coverage',
            },
        },
        'Relation': {
            'type': 'URL Widget',
            'data': {
                'fields': ['Relation'],
                'is_i18n': 1,
                'label_edit': 'label_relation',
                'label': 'label_relation',
                'display_width': 72,
                'help': 'help_dc_relation',
                # empty string to overload CPSUrlWidget default
                'css_class': '',
            },
        },
        'preview': {
            'type': 'Image Widget',
            'data': {
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
        'allow_discussion': {
            'type': 'Boolean Widget',
            'data': {
                'fields': ['allow_discussion'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_allow_discussion_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_metadata_',
        'validate_values_expr' : 'python:portal.verifyMetaData(datastructure, layout)',
        'ncols': 2,
        'rows': [
            [{'ncols': 2, 'widget_id': 'Title'},],
            [{'ncols': 2, 'widget_id': 'Description'},],
            [{'ncols': 2, 'widget_id': 'PortalType'},],
            [{'widget_id': 'Subject'},
             {'widget_id': 'Rights'},],
            [{'widget_id': 'Source'},
             {'widget_id': 'Coverage'},],
            [{'ncols': 2, 'widget_id': 'Relation'},],
            [{'widget_id': 'EffectiveDate'},
             {'widget_id': 'ExpirationDate'},],
            [{'widget_id': 'Contributors'},
             {'widget_id': 'Creator'},],
            [{'widget_id': 'Format'},
             {'widget_id': 'Language'},],
            [{'widget_id': 'CreationDate'},
             {'widget_id': 'ModificationDate'},],
            [{'widget_id': 'preview'},
             {'widget_id': 'allow_discussion'},],
            ],
        },
    }


# common header layout
common_layout = {
    'widgets': {
        'LanguageSelector': {
            'type': 'Document Language Select Widget',
            'data': {
                'fields': ['Language'],
            },
        },
        'Title': {
            'type': 'Heading Widget',
            'data': {
                'fields': ['Title'],
                'level': 1,
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'display_width': 72,
                'size_max': 200,
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
        'LanguageSelectorCreation': {
            'type': 'Select Widget',
            'data': {
                'title': 'Language',
                'fields': ('Language',),
                'is_required': 0,
                'label': 'label_language',
                'label_edit': 'label_language',
                'description': '',
                'help': '',
                'is_i18n': 1,
                'readonly_layout_modes': (),
                'hidden_layout_modes': ('edit', 'view'),
                'hidden_readonly_layout_modes': (),
                'hidden_empty': 0,
                'hidden_if_expr': '',
                'css_class': '',
                'vocabulary': 'language_voc',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [
            [{'widget_id': 'LanguageSelector'}],
            [{'widget_id': 'Title'},],
            [{'widget_id': 'Description'},],
            [{'widget_id': 'LanguageSelectorCreation'}],
            ],
        },
    }

# flexible content
flexible_content_layout = {
    'widgets': {
        'attachedFile': {
            'type': 'AttachedFile Widget',
            'data': {
                'title': 'cpsdoc_flex_attachedFile_title',
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_attachedFile_label_edit',
                'label': 'cpsdoc_flex_attachedFile_label',
                'css_class': 'ddefault',
                'hidden_empty': 1,
                'deletable': 1,
                'size_max': 4*1024*1024,
                },
            },
        'link': {
            'type': 'Link Widget',
            'data': {
                'title': 'cpsdoc_flex_link_title',
                'fields': ['?'],
                'is_i18n': 1,
                'css_class': 'ddefault',
                'label_edit': 'cpsdoc_Link_label_edit',
                'widget_ids': ['link_href',
                               'link_title',
                               'link_description'],
            },
        },
        'link_href': {
            'type': 'URL Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_href',
                'display_width': 60,
            },
        },
        'link_title': {
            'type': 'String Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_content',
                'display_width': 60,
                'size_max': 100,
            },
        },
        'link_description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_title',
                'width': 60,
                'height': 3,
            },
        },
        'textimage': {
            'type': 'Text Image Widget',
            'data': {
                'title': 'cpsdoc_flex_textimage_title',
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_textimage_label_edit',
                'widget_ids': ['photo',
                               'content',
                               'content_right',
                               ],
            },
        },
        'photo': {
            'type': 'Photo Widget',
            'data': {
                'title': 'cpsdoc_flex_photo_title',
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_photo_label_edit',
                'configurable': 'position',
                'display_width': 320,
                'display_height': 200,
                'size_max': 2*1024*1024,
                'allow_resize': 1,
            },
        },
        'content': {
            'type': 'Text Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_content_label_edit',
                'label': '',
                'css_class': 'dcontent',
                'width': 72,
                'height': 10,
                'file_uploader': 1,
                'render_format': 'html',
                'render_position': 'normal',
                'configurable': 'format',
                },
            },
        'content_right': {
            'type': 'Text Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_content_right_label_edit',
                'label': '',
                'css_class': 'dcontent',
                'width': 72,
                'height': 10,
                'file_uploader': 1,
                'render_format': 'html',
                'render_position': 'normal',
                'configurable': 'format',
                },
            },
    },
    'layout': {
        'flexible_widgets': ['textimage:4', 'link', 'attachedFile:5'],
        'style_prefix': 'layout_default_',
        'ncols': 1,
        'rows': [
            [],
            ],
        },
    }

#########################################################
# Folder layout used by section and workspace
#########################################################
folder_layout = {
    'widgets': {
        'hidden_folder': {
            'type': 'Boolean Widget',
            'data': {
                'fields': ['hidden_folder'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_hidden_folder',
                'help': 'cpsdoc_hidden_folder_help',
                'hidden_layout_modes': ['view'],
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [[{'widget_id': 'hidden_folder'}, ], ],
        }
}

#########################################################
# Document
#########################################################
document_layout = {
    'widgets': {
        'content': {
            'type': 'Text Widget',
            'data': {
                'fields': ['content', 'content_position', 'content_format'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_content_label_edit',
                'label': '',
                'css_class': 'dcontent',
                'width': 72,
                'height': 20,
                'file_uploader': 1,
                'render_format': 'html',
                'render_position': 'normal',
                'configurable': 'format',
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [
            [{'widget_id': 'content'}],
            ],
        },
    }

#########################################################
# FAQ LAYOUT
#########################################################
faq_layout = {
    'widgets': {},
    'layout': {
        'layout_view_method': 'layout_faq_view',
        'rows': [[],],
        }
    }

faqitem_layout = {
    'widgets': {
        'Title': {
            'type': 'Heading Widget',
            'data': {
                'fields': ['Title'],
                'level': 2,
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_faq_question_label_edit',
                'display_width': 72,
                'size_max': 200,
            },
        },
        'Description': {
            'type': 'Text Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_faq_long_question_label_edit',
                'label': '',
                'css_class': 'ddescription',
                'width': 72,
                'height': 5,
                'render_format': 'text',
            },
        },
        'content': {
            'type': 'Text Widget',
            'data': {
                'fields': ['content', 'content_position', 'content_format'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_faq_answer_label_edit',
                'label': 'cpsdoc_faq_answer_label',
                'description': 'FAQ answer',
                'css_class': 'dcontent',
                'is_required': 1,
                'width': 72,
                'height': 5,
                'render_format': 'text',
            },
        },
    },
    'layout': {
        'rows': [
            [{'widget_id': 'Title'},],
            [{'widget_id': 'Description'},],
            [{'widget_id': 'content'},],
            ],
        },
    }


#########################################################
# Glossary LAYOUT
#########################################################
glossaryitem_layout = {
    'widgets': {
        },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [[],],
        },
    }

glossary_layout = {
    'widgets': {
        'display_all': {
            'type': 'Boolean Widget',
            'data': {
                'fields': ['display_all'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_glossary_dispall_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_glossary_',
        'rows': [
            [{'widget_id': 'display_all'},
                ],
            ],
        },
    }

#########################################################
# NEWS LAYOUT
#########################################################
newsitem_start_layout = {
    'widgets': {
        'textimage': {
            'type': 'Text Image Widget',
            'data': {
                'title': 'cpsdoc_flex_textimage_title',
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_textimage_label_edit',
                'widget_ids': ['photo',
                               'content',
                               ],
            },
        },
        'photo': {
            'type': 'Photo Widget',
            'data': {
                'title': 'cpsdoc_flex_photo_title',
                'fields': ['photo', 'photo_subtitle', 'photo_position', 'photo_original'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_photo_label_edit',
                'configurable': 'position',
                'display_width': 320,
                'display_height': 200,
                'size_max': 2*1024*1024,
                'allow_resize': 1,
                },
            },
        'content': {
            'type': 'Text Widget',
            'data': {
                'fields': ['content', 'content_position', 'content_format'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_content_label_edit',
                'label': '',
                'css_class': 'dcontent',
                'width': 72,
                'height': 20,
                'file_uploader': 1,
                'render_format': 'html',
                'render_position': 'normal',
                'configurable': 'format',
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_default_',
        'rows': [
            [{'widget_id': 'textimage'}],
            ],
        },
    }

# flexible part of a newsitem
newsitem_flexible_layout = {
    'widgets': {
        'link': {
            'type': 'Link Widget',
            'data': {
                'title': 'cpsdoc_flex_link_title',
                'fields': ['?'],
                'is_i18n': 1,
                'css_class': 'ddefault',
                'label_edit': 'cpsdoc_Link_label_edit',
                'widget_ids': ['link_href',
                               'link_title',
                               'link_description'],
            },
        },
        'link_href': {
            'type': 'URL Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_href',
                'display_width': 60,
            },
        },
        'link_title': {
            'type': 'String Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_content',
                'display_width': 60,
                'size_max': 100,
            },
        },
        'link_description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_title',
                'width': 60,
                'height': 3,
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
                'css_class': 'ddefault',
                'hidden_empty': 1,
                'deletable': 1,
                'size_max': 4*1024*1024,
                },
            },
    },
    'layout': {
        'flexible_widgets': ['link', 'attachedFile'],
        'ncols': 1,
        'rows': [
            [],
            ],
        },
    }

newsitem_end_layout = {
    'widgets': {
        'Subject': {
            'type': 'Subject Widget',
            'data': {
                'fields': ['Subject'],
                'is_i18n': 1,
                'label': 'cpsdoc_NewsItem_label_related_subjects',
                'label_edit': 'cpsdoc_NewsItem_label_related_subjects',
                'vocabulary': 'subject_voc',
                'size': 5,
                'hidden_empty': 1,
            },
        },
        'publication_date': {
            'type': 'DateTime Widget',
            'data': {
                'fields': ['EffectiveDate'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_NewsItem_label_publication_date',
                'label': '',
                'css_class': 'publicationDate',
                'view_format': 'medium',
                'time_setting': 1,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 2,
        'rows': [
            [{'widget_id': 'Subject'}],
            [{'widget_id': 'publication_date'}],
            ],
        },
    }

#########################################################
# FILE LAYOUT
#########################################################
file_layout = {
    'widgets': {
        'Source': {
            'type': 'String Widget',
            'data': {
                'fields': ['Source'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_source',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'Rights': {
            'type': 'String Widget',
            'data': {
                'fields': ['Rights'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_rights',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'file': {
            'type': 'AttachedFile Widget',
            'data': {
                'fields': ['file',
                           'file_text',
                           'file_html'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_attachedFile_label',
                'label': 'cpsdoc_attachedFile_label',
                'hidden_empty': 1,
                'description': 'cpsdoc_attachedFile_description',
                'deletable': 1,
                'size_max': 4*1024*1024,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 2,
        'rows': [
            [{'ncols': 1, 'widget_id': 'Source'},
             {'ncols': 1, 'widget_id': 'Rights'},],
            [{'ncols': 1, 'widget_id': 'file'},
                ],
            ],
        },
    }


#########################################################
# ZIPPEDHTML LAYOUT
#########################################################
zippedhtml_layout = {
    'widgets': {
        'Source': {
            'type': 'String Widget',
            'data': {
                'fields': ['Source'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_source',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'Rights': {
            'type': 'String Widget',
            'data': {
                'fields': ['Rights'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_rights',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'file': {
            'type': 'ZippedHtml Widget',
            'data': {
                'fields': ['file',
                           'file_text',
                           'file_html'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_zippedhtml_label',
                'label': 'cpsdoc_zippedhtml_label',
                'hidden_empty': 1,
                'description': 'cpsdoc_zippedhtml_description',
                'deletable': 1,
                # for performence reason size of zipped should be small!
                'size_max': 1*1024*1024,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 2,
        'rows': [
            [{'ncols': 1, 'widget_id': 'Source'},
             {'ncols': 1, 'widget_id': 'Rights'},],
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
        'Coverage': {
            'type': 'String Widget',
            'data': {
                'fields': ['Coverage'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_coverage',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'content': {
            'type': 'Text Widget',
            'data': {
                'fields': ['content'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_Event_content_label_edit',
                'label': '',
                'description': 'cpsdoc_Event_content_description',
                'css_class': 'dcontent',
                'width': 72,
                'height': 15,
                'render_format': 'text',
                'configurable': 'format',
            },
        },
        'attachedFile': {
            'type': 'AttachedFile Widget',
            'data': {
                'fields': ['attachedFile',
                           'attachedFile_text',
                           'attachedFile_html'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_attachedFile_label',
                'label': 'cpsdoc_attachedFile_label',
                'hidden_empty': 1,
                'description': 'cpsdoc_attachedFile_description',
                'deletable': 1,
                'size_max': 3*1024*1024,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_event_',
        'ncols': 2,
        'rows': [
            [{'ncols': 1, 'widget_id': 'start'},
             {'ncols': 1, 'widget_id': 'end'},],
            [{'ncols': 1, 'widget_id': 'Coverage'},],
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
                'label_edit': 'cpsdoc_Link_label_edit',
                'is_i18n': 1,
                'fields': [],
                'widget_ids': ['Relation', 'Title', 'Description'],
            },
        },
        'Title': {
            'type': 'String Widget',
            'data': {
                'fields': ['Title'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_content',
                'display_width': 60,
                'size_max': 250,
            },
        },
        'Description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_title',
                'width': 60,
                'height': 3,
            },
        },
        'Relation': {
            'type': 'URL Widget',
            'data': {
                'fields': ['Relation'],
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsschemas_label_link_href',
                'display_width': 60,
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
        'Source': {
            'type': 'String Widget',
            'data': {
                'fields': ['Source'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_source',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'Rights': {
            'type': 'String Widget',
            'data': {
                'fields': ['Rights'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_rights',
                'label': '',
                'display_width': 30,
                'size_max': 80,
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
                'allow_resize': True,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 2,
        'rows': [
            [{'widget_id': 'Source'},
             {'widget_id': 'Rights'},],
            [{'ncols': 2, 'widget_id': 'preview'},],
            ],
        },
    }

#########################################################
# IMAGE LAYOUT
#########################################################
flash_animation_layout = {
    'widgets': {
        'Source': {
            'type': 'String Widget',
            'data': {
                'fields': ['Source'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_source',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'Rights': {
            'type': 'String Widget',
            'data': {
                'fields': ['Rights'],
                'hidden_layout_modes': ['view'],
                'is_i18n': 1,
                'label_edit': 'label_rights',
                'label': '',
                'display_width': 30,
                'size_max': 80,
            },
        },
        'preview': {
            'type': 'Flash Widget',
            'data': {
                'fields': ['preview'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_Flash_Animation_label_edit',
                'label': '',
                'display_width': 640,
                'display_height': 600,
                'size_max': 0,
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 2,
        'rows': [
            [{'widget_id': 'Source'},
             {'widget_id': 'Rights'},],
            [{'ncols': 2, 'widget_id': 'preview'},],
            ],
        },
    }

#########################################################
# IMAGE GALLERY LAYOUT
#########################################################
imagegallery_layout = {
    'widgets': {
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
        },
        'popup_mode': {
            'type': 'Boolean Widget',
            'data': {
                'fields': ['popup_mode'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_popup_mode_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
            },
        },
        'popup_width': {
            'type': 'Int Widget',
            'data': {
                'fields': ['popup_width'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_popup_width_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'is_limited': 1,
                'min_value': 100.0,
                'max_value': 1024.0,
                'thousands_separator': '',
            },
        },
        'popup_height': {
            'type': 'Int Widget',
            'data': {
                'fields': ['popup_height'],
                'is_required': 0,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_popup_height_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'is_limited': 1,
                'min_value': 100.0,
                'max_value': 1024.0,
                'thousands_separator': '',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_imagegallery_',
        'ncols': 2,
        'rows': [
            [{'widget_id': 'preview_width'},
             { 'widget_id': 'preview_height'},
                ],
            [{'widget_id': 'nb_items'},
             {'widget_id': 'nb_cols'},
                ],
            [{'widget_id': 'popup_mode'},
            {'widget_id': 'popup_width'},
            {'widget_id': 'popup_height'},
                ],
            ],
        },
    }

#########################################################
# BOOK LAYOUT
#########################################################
book_layout = {
    'widgets': {
        'nb_items_per_summary_page': {
            'type': 'Int Widget',
            'data': {
                'fields': ['nb_items_per_summary_page'],
                'is_required': 1,
                'is_i18n': 1,
                'label_edit': 'cpsdoc_book_nb_summary_page_label_edit',
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
        'has_search_box': {
            'type': 'CheckBox Widget',
            'data': {
                'fields': ['has_search_box'],
                'is_required': 0,
                'is_i18n': True,
                'label_edit': 'cpsdoc_book_has_search_box_label_edit',
                'label': '',
                'hidden_layout_modes': ['view'],
                'description': '',
                'css_class': '',
                'display_true': 'Yes',
                'display_false': 'No',
            },
        },
        'display_mode': {
            'type': 'Boolean Widget',
            'data': {
                'fields': ['display_mode'],
                'is_i18n': 1,
                'label': 'book_display',
                'label_edit': 'cpsdoc_book_display',
                'label_false': 'cpsdoc_book_display_pages',
                'label_true': 'cpsdoc_book_display_flat',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_book_',
        'ncols': 1,
        'rows': [[{'widget_id': 'nb_items_per_summary_page'},
                  ],
                 [{'widget_id': 'has_search_box'},
                  ],
                 [{'widget_id': 'display_mode'},
                  ],
                 ],
        }
    }

#########################################################
# CHAPTER LAYOUT
#########################################################
chapter_layout = {
    'widgets': {
        'nb_items_per_summary_page': {
            'type': 'Int Widget',
            'data': {
                'title': '',
                'fields': ('nb_items_per_summary_page',),
                'is_required': 1,
                'label': '',
                'label_edit': 'cpsdoc_book_nb_summary_page_label_edit',
                'description': '',
                'help': '',
                'is_i18n': 1,
                'readonly_layout_modes': [],
                'hidden_layout_modes': ('view',),
                'hidden_readonly_layout_modes': [],
                'hidden_empty': 0,
                'hidden_if_expr': '',
                'css_class': '',
                'widget_mode_expr': '',
                'is_limited': 1,
                'min_value': 0.0,
                'max_value': 65536.0,
                'thousands_separator': '',
            },
        },
    },
    'layout': {
        'style_prefix': 'layout_chapter_',
        'flexible_widgets': (),
        'ncols': 1,
        'rows': [
            [{'widget_id': 'nb_items_per_summary_page', 'ncols': 1},
            ],
        ],
    },
}

#########################################################
# PAGE LAYOUT
#########################################################
page_layout = {
    'widgets': {

    },
    'layout': {
        'style_prefix': 'layout_page_',
        'ncols': 1,
        'rows': [],
        }
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
layouts['folder'] = folder_layout
layouts['document'] = document_layout
layouts['faq'] = faq_layout
layouts['faqitem'] = faqitem_layout
layouts['glossary'] = glossary_layout
layouts['glossaryitem'] = glossaryitem_layout
layouts['newsitem_start'] = newsitem_start_layout
layouts['newsitem_flexible'] = newsitem_flexible_layout
layouts['newsitem_end'] = newsitem_end_layout
layouts['file'] = file_layout
layouts['zippedhtml'] = zippedhtml_layout
layouts['event'] = event_layout
layouts['link'] = link_layout
layouts['image'] = image_layout
layouts['imagegallery'] = imagegallery_layout
layouts['book'] = book_layout
layouts['chapter'] = chapter_layout
layouts['page'] = page_layout
layouts['flash_animation'] = flash_animation_layout

# other products
try:
    layouts.update(context.getCPSMailBoxerDocumentLayouts())
except AttributeError,e:
    pass


if loadcustom:
    clayouts = context.getCustomDocumentLayouts()
    layouts.update(clayouts)

return layouts
