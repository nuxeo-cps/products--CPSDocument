## Script (Python) "getDocumentLayouts"
##parameters=
#$Id$

"""
Here are defined the list of schemas to be registred
Please, follow the same pattern to add new schemas.
"""

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
                'default': '64',
                'is_indexed': 0,
            },
        },
    'preview_height': {
        'type': 'CPS Int Field',
        'data': {
                'default': '64',
                'is_indexed': 0,
            },
        },
    'nb_cols': {
        'type': 'CPS Int Field',
        'data': {
                'default': '3',
                'is_indexed': 0,
            },
        },
    'nb_items': {
        'type': 'CPS Int Field',
        'data': {
                'default': '9',
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

schemas['faq'] = faq_schema
schemas['faqitem'] = faqitem_schema
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
