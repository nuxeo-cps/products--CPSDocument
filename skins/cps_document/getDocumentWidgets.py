##parameters=
#$Id$

"""
Here are defined the list of widgets to be registred
Please, follow the same pattern to add new ones
"""

widgets = {
        'Boolean Widget': {
            'type': 'CPS Boolean Widget Type',
            'data': {},
            },
        'Int Widget': {
            'type': 'CPS Int Widget Type',
            'data': {},
            },
        'Long Widget': {
            'type': 'CPS Long Widget Type',
            'data': {},
            },
        'Float Widget': {
            'type': 'CPS Float Widget Type',
            'data': {},
            },
        'String Widget': {
            'type': 'CPS String Widget Type',
            'data': {},
            },
        'URL Widget': {
            'type': 'CPS URL Widget Type',
            'data': {},
            },
        'Email Widget': {
            'type': 'CPS Email Widget Type',
            'data': {},
            },
        'Identifier Widget': {
            'type': 'CPS Identifier Widget Type',
            'data': {},
            },
        'Heading Widget': {
            'type': 'CPS Heading Widget Type',
            'data': {},
            },
        'Password Widget': {
            'type': 'CPS Password Widget Type',
            'data': {},
            },
        'CheckBox Widget': {
            'type': 'CPS CheckBox Widget Type',
            'data': {},
            },
        'TextArea Widget': {
            'type': 'CPS TextArea Widget Type',
            'data': {},
            },
        'Text Widget': {
            'type': 'CPS Text Widget Type',
            'data': {},
            },
        'Lines Widget': {
            'type': 'CPS Lines Widget Type',
            'data': {},
            },
        'Date Widget': {
            'type': 'CPS Date Widget Type',
            'data': {},
            },
        'DateTime Widget': {
            'type': 'CPS DateTime Widget Type',
            'data': {},
            },
        'File Widget': {
            'type': 'CPS File Widget Type',
            'data': {},
            },
        'AttachedFile Widget': {
            'type': 'CPS AttachedFile Widget Type',
            'data': {},
            },
        'Image Widget': {
            'type': 'CPS Image Widget Type',
            'data': {},
            },
        'Photo Widget': {
            'type': 'CPS Photo Widget Type',
            'data': {},
            },
        'Html Widget': {
            'type': 'CPS Html Widget Type',
            'data': {},
            },
         'Method Widget': {
            'type': 'CPS Method Widget Type',
            'data': {},
            },
        'Rich Text Editor Widget': {
            'type': 'CPS Rich Text Editor Widget Type',
            'data': {},
            },
        'Select Widget': {
            'type': 'CPS Select Widget Type',
            'data': {},
            },
        'Dummy Widget': {
            'type': 'CPS Customizable Widget Type',
            'data': {
                'field_types': ['CPS String Field'],
                'prepare_validate_method': 'widget_dummy_prepare_validate',
                'render_method': 'widget_dummy_render',
                },
            },
        'MultiSelect Widget': {
            'type': 'CPS MultiSelect Widget Type',
            'data': {},
            },
        'ExtendedSelect Widget': {
            'type': 'CPS ExtendedSelect Widget Type',
            'data': {},
            },
        'InternalLinks Widget': {
            'type': 'CPS InternalLinks Widget Type',
            'data': {},
            },
        'Link Widget': {
            'type': 'CPS Compound Widget Type',
            'data': {
                'render_method': 'widget_link_render',
                },
            },
        'Text Image Widget': {
            'type': 'CPS Compound Widget Type',
            'data': {
                'prepare_validate_method': 'widget_textimage_prepare_validate',
                'render_method': 'widget_textimage_render',
                },
            },
        'Ordered List Widget': {
            'type': 'CPS Ordered List Widget Type',
            'data': {},
            },
        'Unordered List Widget': {
            'type': 'CPS Unordered List Widget Type',
            'data': {},
            },
        }

cwidgets = context.getCustomDocumentWidgets()

widgets.update(cwidgets)

return widgets
