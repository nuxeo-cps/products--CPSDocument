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
            ('news', "News", ''),
            ('society', "Society", ''),
            ('technology', "Technology", ''),
            )},
        },
    'language_voc_vocabulary': {
        'data': {'tuples': (
            ('label_language_fr', 'Français', 'label_language_fr'),
            ('label_language_en', 'English', 'label_language_en'),
            ('label_language_es', 'Castellano', 'label_language_es'),
            ('label_language_de', 'Deutsch', 'label_language_de'),
            ('label_language_it', 'Italiano', 'label_language_it'),
            ('label_language_nl', 'Nederlands', 'label_language_nl'),
            ('label_language_pt_BR', 'Brasileiro', 'label_language_pt_BR'),
            )},
        },
    }

cvocabularies = context.getCustomDocumentVocabularies()

vocabularies.update(cvocabularies)

return vocabularies
