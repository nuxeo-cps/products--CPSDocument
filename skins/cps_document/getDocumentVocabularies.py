##parameters=loadcustom=1
#$Id$
"""
Here are defined the vocabularies.
Please, follow the same pattern to add new ones.
"""

vocabularies = {
    'subject_voc': {
        'type': 'CPS Vocabulary',
        'data': {'tuples': (
            ("Arts", "Arts", "label_subject_Arts"),
            ("Business", "Business", "label_subject_Business"),
            ("Computers", "Computers", "label_subject_Computers"),
            ("Games", "Games", "label_subject_Games"),
            ("Health", "Health", "label_subject_Health"),
            ("Home", "Home", "label_subject_Home"),
            ("Kids and Teens", "Kids and Teens",
             "label_subject_Kids and Teens"),
            ("News", "News", "label_subject_News"),
            ("Recreation", "Recreation", "label_subject_Recreation"),
            ("Reference", "Reference", "label_subject_Reference"),
            ("Regional", "Regional", "label_subject_Regional"),
            ("Science", "Science", "label_subject_Science"),
            ("Shopping", "Shopping", "label_subject_Shopping"),
            ("Society", "Society", "label_subject_Society"),
            ("Sports", "Sports", "label_subject_Sports"),
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
            ('pt_BR', 'Brasileiro', 'label_language_pt_BR'),
            ('mg', 'Malagasy', 'label_language_mg'),
            ('ro', 'Romana', 'label_language_ro'),
            ('eu', 'Euskara', 'label_language_eu'),
            )},
        },
    'search_sort_results_by': {
        'type': 'CPS Vocabulary',
        'data': {'tuples': (
                ('', "No sort", "label_sort_by"),
                ('title_asc', "Title ascending", "label_title_asc"),
                ('title_desc', "Title descending", "label_title_desc"),
                ('date_asc', "Date ascending", "label_date_asc"),
                ('date_desc', "Date descending", "label_date_desc"),
                ('status_asc', "Status ascending", "label_status_asc"),
                ('status_desc', "Status descending", "label_status_desc"),
                ('author_asc', "Author ascending", "label_author_asc"),
                ('author_desc', "Author descending", "label_author_desc"),
                )
        },
        },
    }

if loadcustom:
    cvocabularies = context.getCustomDocumentVocabularies()
    vocabularies.update(cvocabularies)

return vocabularies
