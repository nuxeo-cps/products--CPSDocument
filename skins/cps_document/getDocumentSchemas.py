##parameters=loadcustom=1
#$Id$

"""
Here are defined the list of schemas to be registred
Please, follow the same pattern to add new schemas.
"""

#########################################################
# SHARED SCHEMAS
#########################################################
#metadata schema
metadata_schema = {
    'Title': {'type': 'CPS String Field',
              'data': {'is_searchabletext': 1,}},
    'Description': {'type': 'CPS String Field',
                    'data': {'is_searchabletext': 1}},
    'Subject': {'type': 'CPS String List Field',
                'data': {'is_searchabletext': 1}},
    'Contributors': {'type': 'CPS String List Field',
                     'data': {'is_searchabletext': 1,
                              'write_process_expr':
                              'python: portal.computeContributors(user, value)'
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
                 'data': {'write_ignore_storage': 1,}},
    'Rights': {'type': 'CPS String Field', 'data': {'is_searchabletext': 1}},
    'Creator': {'type': 'CPS String Field',
                'data': {'is_searchabletext': 1,
                         'write_ignore_storage': 1,}},
    'Source': {'type': 'CPS String Field', 'data': {'is_searchabletext': 1}},
    'Relation': {'type': 'CPS String Field', 'data': {'is_searchabletext': 1}},
    'Coverage': {'type': 'CPS String Field', 'data': {'is_searchabletext': 1}},
    }


# common schema
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

# flexible content schema
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
# FAQ SHEMA
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
                'default_expr': 'string:normal',
                'is_searchabletext': 1,
            },
        },
    'content_format': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:text',
                'is_searchabletext': 1,
            },
        },
    }

#########################################################
# Glossary SCHEMA
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
# News SCHEMA
########################################################

news_schema = {
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
    'newsdate': {
        'type': 'CPS DateTime Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'photo': {
        'type': 'CPS Image Field',
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
    }

########################################################
# File SCHEMA
########################################################

file_schema = {
    'file': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'file_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expr': 'nothing',
                'is_searchabletext': 0,
            },
        },
    'file_text': {
        'type': 'CPS String Field',
        'data': {
                'default_expr': 'string:',
                'is_searchabletext': 1,
            },
        },
    }


########################################################
# Event SCHEMA
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
# Link SCHEMA
########################################################

# store href using Relation metadata

########################################################
# Image SCHEMA
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
    }

########################################################
# Book SCHEMA
########################################################

book_schema = {
    'nb_items_per_summary_page': {
        'type': 'CPS Int Field',
        'data': {
                'default_expr': 'python:20',
                'is_searchabletext': 0,
            },
        },
    }

###########################################################
# END OF SCHEMAS DEFINITIONS
###########################################################

schemas = {}

#
# Building the dictionnary of schemas for the installer
#
schemas['metadata'] = metadata_schema
schemas['common'] = common_schema
schemas['flexible_content'] = flexible_content_schema
schemas['folder'] = folder_schema
schemas['faqitem'] = faqitem_schema
schemas['glossary'] = glossary_schema
schemas['news'] = news_schema
schemas['file'] = file_schema
schemas['event'] = event_schema
schemas['imagegallery'] = imagegallery_schema
schemas['book'] = book_schema

# other products
try:
    schemas.update(context.getCPSCollectorSchemas())
except AttributeError:
    pass
try:
    schemas.update(context.getCPSMailBoxerDocumentSchemas())
except AttributeError,e:
    pass


if loadcustom:
    cschemas = context.getCustomDocumentSchemas()
    schemas.update(cschemas)

return schemas
