##parameters=
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
              'data': {'is_indexed': 1,}},
    'Description': {'type': 'CPS String Field',
                    'data': {'is_indexed': 1}},
    'Subject': {'type': 'CPS String List Field',
                'data': {'is_indexed': 1}},
    'Contributors': {'type': 'CPS String List Field',
                     'data': {'is_indexed': 1}},
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
    'Rights': {'type': 'CPS String Field', 'data': {'is_indexed': 1}},
    'Creator': {'type': 'CPS String Field',
                'data': {'is_indexed': 1,
                         'write_ignore_storage': 1,}},
    }


# common schema
common_schema = {
    'preview': {
        'type': 'CPS Image Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    }

# flexible content schema
flexible_content_schema = {
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    'content_format': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 0,
            },
        },
    'content_position': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 0,
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
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    }

faq_schema = {
    }

#########################################################
# Glossary SCHEMA
#########################################################

glossaryitem_schema = {
    }

glossary_schema = {
    'display_all': {
        'type': 'CPS Int Field',
        'data': {
                'default_expression_str': 'python:0',
                'is_indexed': 0,
            },
        },
    }

########################################################
# DUMMY FORM SCHEMA
########################################################

dummy_form_schema = {
    }

########################################################
# News SCHEMA
########################################################

news_schema = {
    'preview': {
        'type': 'CPS Image Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'attachedFile': {
        'type': 'CPS File Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'attachedFile_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'attachedFile_text': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    'newsdate': {
        'type': 'CPS DateTime Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'photo': {
        'type': 'CPS Image Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'theme': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    'longTitle': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
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
                'default_expression_str': 'nothing',
                'is_indexed': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'file_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'file_text': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
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
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'end': {
        'type': 'CPS DateTime Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    'attachedFile': {
        'type': 'CPS File Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'attachedFile_html': {
        'type': 'CPS File Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    'attachedFile_text': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    }

########################################################
# Link SCHEMA
########################################################

link_schema = {
    'href': {
        'type': 'CPS String Field',
        'data': {
                'default_expression_str': 'string:',
                'is_indexed': 1,
            },
        },
    }



########################################################
# Image SCHEMA
########################################################

image_schema = {
    'preview': {
        'type': 'CPS Image Field',
        'data': {
                'default_expression_str': 'nothing',
                'is_indexed': 0,
            },
        },
    }

imagegallery_schema = {
    'preview_width': {
        'type': 'CPS Int Field',
        'data': {
                'default_expression_str': 'python:64',
                'is_indexed': 0,
            },
        },
    'preview_height': {
        'type': 'CPS Int Field',
        'data': {
                'default_expression_str': 'python:64',
                'is_indexed': 0,
            },
        },
    'nb_cols': {
        'type': 'CPS Int Field',
        'data': {
                'default_expression_str': 'python:3',
                'is_indexed': 0,
            },
        },
    'nb_items': {
        'type': 'CPS Int Field',
        'data': {
                'default_expression_str': 'python:9',
                'is_indexed': 0,
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

schemas['faq'] = faq_schema
schemas['faqitem'] = faqitem_schema
schemas['glossary'] = glossary_schema
schemas['glossaryitem'] = glossaryitem_schema
schemas['news'] = news_schema
schemas['file'] = file_schema
schemas['event'] = event_schema
schemas['link'] = link_schema
schemas['image'] = image_schema
schemas['imagegallery'] = imagegallery_schema
#schemas['dummy_form'] = dummy_form_schema

cschemas = context.getCustomDocumentSchemas()

schemas.update(cschemas)

return schemas
