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
faq_schema = { 'title': {'type': 'CPS String Field',
                         'data': {'default': '',
                                  'is_indexed': 1,
                                  },
                         },
               'description': {'type': 'CPS String Field',
                               'data': {'default': '',
                                        'is_indexed': 1,
                                        },
                               },
               'question': {'type': 'CPS String Field',
                            'data': {'default': '',
                                     'is_indexed': 0,
                                     },
                            },
               'answer': {'type': 'CPS String Field',
                          'data': {'default': '',
                                   'is_indexed': 0,
                                   },
                          },
               }

########################################################
# DUMMY FORM SCHEMA
########################################################

dummy_form_schema = {'title': {'type': 'CPS String Field',
                               'data': {'default': '',
                                        'is_indexed': 1,
                                        },
                               },
                     'description': {'type': 'CPS String Field',
                                     'data': {'default': '',
                                              'is_indexed': 1,
                                              },
                                     },
                     }

########################################################
# NEWS SCHEMA
########################################################
news_schema = {'title': { 'type': 'CPS String Field',
                          'data': {'default': '',
                                   'is_indexed': 1,
                                   },
                          },
               'description': {'type': 'CPS String Field',
                               'data': {'default': 'resume',
                                        'is_indexed': 1,
                                        },
                               },
               'longTitle': {'type': 'CPS String Field',
                             'data': {'default': '',
                                      'is_indexed': 1,
                                      },
                             },
               'newsdate': {'type': 'CPS DateTime Field',
                            'data': {'default': '',
                                     'is_indexed': 0,
                                     },
                            },
               'content': {'type': 'CPS String Field',
                           'data': {'default': '',
                                    'is_indexed': 1,
                                    },
                           },
               'photo': {'type': 'CPS Image Field',
                         'data': {'default': '',
                                  'is_indexed': 0,
                                  },
                         },
               'preview': {'type': 'CPS Image Field',
                           'data': {'default': '',
                                    'is_indexed': 0,
                                    },
                           },
               'attachedFile': {'type': 'CPS File Field',
                           'data': {'default': '',
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
schemas['dummy_form'] = dummy_form_schema
schemas['news'] = news_schema

cschemas = context.getCustomDocumentSchemas()

schemas.update(cschemas)

return schemas