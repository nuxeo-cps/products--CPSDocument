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
                        'title': 'FAQ short question',
                        'description': 'FAQ short question for section display',
                        'css_class': 'title',
                        'display_width': 20,
                        'display_maxwidth': 0,
                        },
                    },
                'description': {
                    'type': 'TextArea Widget',
                    'data': {
                        'fields': ['description'],
                        'title': 'FAQ answer resume',
                        'description': 'FAQ answer resume for section display',
                        'css_class': 'description',
                        'width': 40,
                        'height': 5,
                        'render_mode': 'stx',
                        },
                    },
                'question': {
                    'type': 'TextArea Widget',
                    'data': {
                        'fields': ['question'],
                        'title': 'FAQ question',
                        'description': 'FAQ full question',
                        'css_class': 'title',
                        'width': 40,
                        'height': 5,
                        'render_mode': 'stx',
                        },
                    },
                'answer': {
                    'type': 'TextArea Widget',
                    'data': {
                        'fields': ['answer'],
                        'title': 'FAQ answer',
                        'description': 'FAQ full answer',
                        'css_class': 'stx',
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
                        'title': 'Dummy Form title field',
                        'description': 'Title for a dummy form',
                        'css_class': 'title',
                        'display_width': 20,
                        'display_maxwidth': 0,
                        },
                    },
                'description': {
                    'type': 'TextArea Widget',
                    'data': {
                        'fields': ['description'],
                        'title': 'Dummy Form Description field',
                        'description': 'Description field for a dummy form',
                        'css_class': 'description',
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
                'title': {
                    'type': 'String Widget',
                    'data': {
                        'fields': ['title'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_title_label_edit',
                        'description': 'cpsdoc_News_title_description',
                        'css_class': 'dtitle',
                        'display_width': 20,
                        'display_maxwidth': 0,
                        },
                    },
                'longTitle': {
                    'type': 'String Widget',
                    'data': {
                        'fields': ['longTitle'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_longTitle_label_edit',
                        'description': 'cpsdoc_News_longTitle_description',
                        'css_class': 'dtitle2',
                        'display_width': 50,
                        'display_maxwidth': 0,
                        'is_required': 1,
                        },
                    },
                'theme': {
                    'type': 'Select Widget',
                    'data': {
                        'fields': ['theme'],
                        'label_edit': 'Theme',
                        'description': 'Theme desc',
                        'css_class': '',
                        'vocabulary': 'dummy_voc',
                        },
                    },
                'description': {
                    'type': 'TextArea Widget',
                    'data': {
                        'fields': ['description'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_description_label_edit',
                        'description': 'cpsdoc_News_description_description',
                        'css_class': 'ddescription',
                        'width': 40,
                        'height': 5,
                        'render_mode': 'stx',
                        },
                    },
                'newsdate': {
                    'type': 'Date Widget',
                    'data': {
                        'fields': ['newsdate'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_newsdate_label_edit',
                        'label': 'cpsdoc_News_newsdate_label',
                        'description': 'cpsdoc_News_newsdate_description',
                        'css_class': 'dtitle5 dright',
                        'is_required': 1,
                        'view_format': '%d/%m/%Y',
                        'view_format_none': '-',

                        },
                    },
                'content': {
                    'type': 'TextArea Widget',
                    'data': {
                        'fields': ['content'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_content_label_edit',
                        'description': 'cpsdoc_News_content_description',
                        'css_class': 'dcontent',
                        'width': 40,
                        'height': 25,
                        'render_mode': 'stx',
                        },
                    },
                'photo': {
                    'type': 'Image Widget',
                    'data': {
                        'fields': ['photo'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_photo_label_edit',
                        'description': 'cpsdoc_News_photo_description',
                        'css_class': 'dleft',
                        'deletable': 1,
                        'display_width': 250,
                        'display_height': 150,
                        'maxsize': 1024*1024,
                        },
                    },
                'preview': {
                    'type': 'Image Widget',
                    'data': {
                        'fields': ['preview'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_preview_label_edit',
                        'description': 'cpsdoc_News_preview_description',
                        'css_class': '',
                        'deletable': 1,
                        'display_width': 200,
                        'display_height': 150,
                        'maxsize': 1024*1024,
                        'hidden_view': 1,
                        },
                    },
                'attachedFile': {
                    'type': 'File Widget',
                    'data': {
                        'fields': ['attachedFile'],
                        'is_i18n': 1,
                        'label_edit': 'cpsdoc_News_attachedFile_label_edit',
                        'label': 'cpsdoc_News_attachedFile_label',
                        'description': 'cpsdoc_News_attachedFile_description',
                        'css_class': '',
                        'deletable': 1,
                        'display_width': 200,
                        'display_height': 150,
                        'maxsize': 1024*1024,
                        'hidden_empty': 1,
                        },
                    },
                },
            'layout': {
                'ncols': 2,
                'rows': [[{'ncols': 1, 'widget_id': 'title'},
                          {'ncols': 1, 'widget_id': 'newsdate'},],
                         [{'ncols': 1, 'widget_id': 'longTitle'},],
                         [{'ncols': 1, 'widget_id': 'theme'},],
                         [{'ncols': 1, 'widget_id': 'description'},],
                         [{'ncols': 1, 'widget_id': 'photo'},
                          {'ncols': 1, 'widget_id': 'preview'},],
                         [{'ncols': 1, 'widget_id': 'content'},],
                         [{'ncols': 1, 'widget_id': 'attachedFile'},],
                         ]
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

clayouts = context.getCustomDocumentLayouts()

layouts.update(clayouts)

return layouts
