##parameters=
#$Id$
"""
Here are defined the vocabularies.
Please, follow the same pattern to add new ones.
"""

def make_dict(voc):
    d = {}
    l = []
    for v in voc:
        d[v] = v
        l.append(v)
    return {'data': {'dict': d, 'list': l}}

subject_voc = ("Arts", "Business", "Computers", "Games", "Health",
               "Home", "Kids and Teens", "News", "Recreation",
               "Reference", "Regional", "Science", "Shopping",
               "Society", "Sports")

vocabularies = {
    'subject_voc': make_dict(subject_voc),
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
