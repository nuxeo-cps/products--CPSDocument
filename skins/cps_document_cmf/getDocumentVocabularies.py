##parameters=loadcustom=1
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
    'language_voc': {
        'type': 'CPS Vocabulary',
        'data': {'tuples': (
            ('fr', 'Français', 'label_language_fr'),
            ('en', 'English', 'label_language_en'),
            ('es', 'Castellano', 'label_language_es'),
            ('de', 'Deutsch', 'label_language_de'),
            ('it', 'Italiano', 'label_language_it'),
            ('nl', 'Nederlands', 'label_language_nl'),
            ('pt_BR', 'Portugueses(Brasileiro)', 'label_language_pt_BR'),
            )},
        },
    }

if loadcustom:
    cvocabularies = context.getCustomDocumentVocabularies()
    vocabularies.update(cvocabularies)

return vocabularies
