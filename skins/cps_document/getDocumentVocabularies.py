##parameters=
#$Id$
"""
Here are defined the vocabularies.
Please, follow the same pattern to add new ones.
"""

vocabularies = {
    'subject_voc': {
        'type': 'CPS Vocabulary',
        'data': {'list': (
            "Arts", "Business", "Computers", "Games", "Health",
            "Home", "Kids and Teens", "News", "Recreation",
            "Reference", "Regional", "Science", "Shopping",
            "Society", "Sports",
            )},
        },
    'dummy_voc': {
        'type': 'CPS Vocabulary',
        'data': {'tuples': (
            ('news', "News"),
            ('society', "Society"),
            ('technology', "Technology"),
            )},
        },
    }

cvocabularies = context.getCustomDocumentVocabularies()

vocabularies.update(cvocabularies)

return vocabularies
