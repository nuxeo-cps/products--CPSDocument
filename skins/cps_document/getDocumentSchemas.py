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
    'Title': {'type': 'CPS String Field', 'data': {}},
    'Description': {'type': 'CPS String Field', 'data': {}},
    'Subject': {'type': 'CPS String List Field', 'data': {}},
    'Contributors': {'type': 'CPS String List Field', 'data': {}},
    'CreationDate': {'type': 'CPS DateTime Field', 'data': {}},
    'ModificationDate': {'type': 'CPS DateTime Field', 'data': {}},
    'EffectiveDate': {'type': 'CPS DateTime Field', 'data': {}},
    'ExpirationDate': {'type': 'CPS DateTime Field', 'data': {}},
    'Format': {'type': 'CPS String Field', 'data': {}},
    'Language': {'type': 'CPS String Field', 'data': {}},
    'Rights': {'type': 'CPS String Field', 'data': {}},
    'Creator': {'type': 'CPS String Field', 'data': {}},
    }


# common schema
common_schema = {
    'date': {
        'type': 'CPS DateTime Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'theme': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'preview': {
        'type': 'CPS Image Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    }

# flexible content schema
flexible_content_schema = {
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'content_format': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'content_position': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    }

#########################################################
# FAQ SHEMA
#########################################################

faqitem_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }

faq_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }

#########################################################
# Glossary SCHEMA
#########################################################

glossaryitem_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }

glossary_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'display_all': {
        'type': 'CPS Int Field',
        'data': {
                'default': 0,
                'is_indexed': 0,
            },
        },
    }

########################################################
# DUMMY FORM SCHEMA
########################################################

dummy_form_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }

########################################################
# News SCHEMA
########################################################

news_schema = {
    'preview': {
        'type': 'CPS Image Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'attachedFile': {
        'type': 'CPS File Field',
        'data': {
                'default': '',
                'is_indexed': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'attachedFile_html': {
        'type': 'CPS File Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'attachedFile_text': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'newsdate': {
        'type': 'CPS DateTime Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'photo': {
        'type': 'CPS Image Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'theme': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'longTitle': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }

########################################################
# File SCHEMA
########################################################

file_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'file': {
        'type': 'CPS File Field',
        'data': {
                'default': '',
                'is_indexed': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'file_html': {
        'type': 'CPS File Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'file_text': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }


########################################################
# Event SCHEMA
########################################################

event_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'start': {
        'type': 'CPS DateTime Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'end': {
        'type': 'CPS DateTime Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'content': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'attachedFile': {
        'type': 'CPS File Field',
        'data': {
                'default': '',
                'is_indexed': 0,
                'suffix_html': '_html',
                'suffix_text': '_text',
            },
        },
    'attachedFile_html': {
        'type': 'CPS File Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    'attachedFile_text': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }

########################################################
# Link SCHEMA
########################################################

link_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'href': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    }



########################################################
# Image SCHEMA
########################################################

image_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'preview': {
        'type': 'CPS Image Field',
        'data': {
                'default': '',
                'is_indexed': 0,
            },
        },
    }

imagegallery_schema = {
    'title': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'description': {
        'type': 'CPS String Field',
        'data': {
                'default': '',
                'is_indexed': 1,
            },
        },
    'preview_width': {
        'type': 'CPS Int Field',
        'data': {
                'default': 64,
                'is_indexed': 0,
            },
        },
    'preview_height': {
        'type': 'CPS Int Field',
        'data': {
                'default': 64,
                'is_indexed': 0,
            },
        },
    'nb_cols': {
        'type': 'CPS Int Field',
        'data': {
                'default': 3,
                'is_indexed': 0,
            },
        },
    'nb_items': {
        'type': 'CPS Int Field',
        'data': {
                'default': 9,
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
