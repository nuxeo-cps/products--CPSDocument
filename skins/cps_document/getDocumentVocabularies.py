##parameters=
#$Id$
"""
Here are defined the vocabularies.
Please, follow the same pattern to add new ones.
"""

vocabularies = {
    'dummy_voc': {
        'type': 'CPS Vocabulary',
        'data': {
            'dict': {
                'news': "News",
                'society': "Society",
                'technology': "Technology",
                },
            'list': [
                'society',
                'news',
                'technology',
                ],
            },
        },
    }

cvocabularies = context.getCustomDocumentVocabularies()

vocabularies.update(cvocabularies)

return vocabularies
