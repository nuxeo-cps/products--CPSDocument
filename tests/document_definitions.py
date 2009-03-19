# (C) Copyright 2003-2009 Nuxeo SA <http://nuxeo.com>
# Authors:
# M.-A. Darche <madarche@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$

#########################################################
# Metadata
#########################################################
metadata_schema = {
    'Title': {'type': 'CPS String Field',
              'data': {'is_searchabletext': 1,}},
    'Description': {'type': 'CPS String Field',
                    'data': {'is_searchabletext': 1}},
    'Subject': {'type': 'CPS String List Field',
                'data': {'is_searchabletext': 0}},
    'Contributors': {'type': 'CPS String List Field',
                     'data': {'is_searchabletext': 0,
                              'write_process_expr':
                              'python: modules["Products.CPSDefault.utils"].computeContributors(portal, value)'
                              },},
    'CreationDate': {'type': 'CPS DateTime Field',
                     'data': {'write_ignore_storage': 1,}},
    'ModificationDate': {'type': 'CPS DateTime Field',
                         'data': {'write_ignore_storage': 1,}},
    'EffectiveDate': {'type': 'CPS DateTime Field', 'data': {}},
    'ExpirationDate': {'type': 'CPS DateTime Field', 'data': {}},
    'Format': {'type': 'CPS String Field',
               'data': {'write_ignore_storage': 1,}},
    'Language': {'type': 'CPS String Field',
                 'data': {'write_ignore_storage': 1,
                          'default_expr':
                          'portal/translation_service/getSelectedLanguage|nothing'}},
    'Rights': {'type': 'CPS String Field', 'data': {'is_searchabletext': 0}},
    'Creator': {'type': 'CPS String Field',
                'data': {'is_searchabletext': 0,
                         'write_ignore_storage': 1,}},
    'Source': {'type': 'CPS String Field', 'data': {'is_searchabletext': 0}},
    'Relation': {'type': 'CPS String Field', 'data': {'is_searchabletext': 0}},
    'Coverage': {'type': 'CPS String Field', 'data': {'is_searchabletext': 0}},
    }

#########################################################
# Common
#########################################################
common_schema = {
    'allow_discussion': {
        'type': 'CPS Int Field',
        'data': {
            'default_expr': 'python:0',
            'is_searchabletext': 0,
            },
        },
    'preview': {
        'type': 'CPS Image Field',
        'data': {
            'default_expr': 'nothing',
            'is_searchabletext': 0,
            },
        },
    }

#########################################################
# Flexible content
#########################################################
flexible_content_schema = {
    # the schema will be created inside the document
    }

#########################################################
# Folder
#########################################################
folder_schema = {
    'hidden_folder': {
        'type': 'CPS Int Field',
        'data': {'default_expr': 'python:0',
                 'is_searchabletext': 0,
                 },
        },
    }

#########################################################
# Document
#########################################################
document_schema = {
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'content_position': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'content_format': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    }

#########################################################
# FAQ item
#########################################################
faqitem_schema = {
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'content_position': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'content_format': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    }

#########################################################
# Glossary
#########################################################
glossary_schema = {
    'display_all': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:0',
                'is_searchabletext': 0,
            },
        },
    }

########################################################
# News item
########################################################
newsitem_schema = {
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'content_position': {
        'type': 'CPS String Field',
        'data': {
            },
        },
    'content_format': {
        'type': 'CPS String Field',
        'data': {
            },
        },
    'photo': {
        'type': 'CPS Image Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'photo_subtitle': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'photo_position': {
        'type': 'CPS String Field',
        'data': {
            },
        },
    'photo_original': {
        'type': 'CPS Image Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    }

########################################################
# File
########################################################
file_schema = {
    'file': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
                'suffix_text': '_text',
                'suffix_html': '_html',
                'suffix_html_subfiles': '_html_subfiles',
            },
        },
    'file_text': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'file_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'file_html_subfiles': {
        'type': 'CPS SubObjects Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    }


########################################################
# ZippedHtml
########################################################
zippedhtml_schema = {
    'file': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
                'suffix_text': '_text',
                'suffix_html': '_html',
                'suffix_html_subfiles': '_html_subfiles',
            },
        },
    'file_text': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'file_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'file_html_subfiles': {
        'type': 'CPS SubObjects Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    }


########################################################
# Event
########################################################
event_schema = {
    'start': {
        'type': 'CPS DateTime Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'end': {
        'type': 'CPS DateTime Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'content_position': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'content_format': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    'attachedFile': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'attachedFile_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'attachedFile_text': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    }

########################################################
# Link
########################################################
# store href using Relation metadata

########################################################
# Image
########################################################
imagegallery_schema = {
    'preview_width': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:64',
                'is_searchabletext': 0,
            },
        },
    'preview_height': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:64',
                'is_searchabletext': 0,
            },
        },
    'nb_cols': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:3',
                'is_searchabletext': 0,
            },
        },
    'nb_items': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:9',
                'is_searchabletext': 0,
            },
        },
    'popup_mode': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:0',
                'is_searchabletext': 0,
            },
        },
    'popup_width': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:300',
                'is_searchabletext': 0,
            },
        },
    'popup_height': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:300',
                'is_searchabletext': 0,
            },
        },
    }

########################################################
# Book
########################################################
book_schema = {
    'nb_items_per_summary_page': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:20',
                'is_searchabletext': 0,
            },
        },
    'has_search_box': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:0',
                'is_searchabletext': 0,
            },
        },
    'display_mode': {
        'type': 'CPS Int Field',
        'data': {'is_searchabletext': 0,
                 'default_expr': 'python:0',}
        },
    }

########################################################
# Flash
########################################################
flash_animation_schema = {
    'flash_file': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
                'suffix_text': '_text',
                'suffix_html': '_html',
                'suffix_html_subfiles': '_html_subfiles',
            },
        },
    'flash_file_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'flash_file_html_subfiles': {
        'type': 'CPS SubObjects Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
}

ziparchiveuploader_schema = {
    'ziparchiveuploader': {
        'type': 'CPS File Field',
        'data': {
            'default_expr': 'nothing',
            'is_searchabletext': 0,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': True,
            'read_process_expr': '',
            'read_process_dependent_fields': (),
            'write_ignore_storage': True,
            'write_process_expr': "python: modules['Products.CPSDocument.createFile'].createFile(proxy, value)",
            'suffix_text': '',
            'suffix_html': '',
            'suffix_html_subfiles': '',
        },
    },
}

schemas = {}
schemas['metadata'] = metadata_schema
schemas['common'] = common_schema
schemas['flexible_content'] = flexible_content_schema
schemas['folder'] = folder_schema
schemas['document'] = document_schema
schemas['faqitem'] = faqitem_schema
schemas['glossary'] = glossary_schema
schemas['newsitem'] = newsitem_schema
schemas['file'] = file_schema
schemas['zippedhtml'] = zippedhtml_schema
schemas['event'] = event_schema
schemas['imagegallery'] = imagegallery_schema
schemas['book'] = book_schema
schemas['flash_animation'] = flash_animation_schema
schemas['ziparchiveuploader'] = ziparchiveuploader_schema

def getDocumentSchemas():
    return schemas
