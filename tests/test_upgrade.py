# (C) Copyright 2010 Nuxeo SA <http://nuxeo.com>
# Authors:
# G. Racinet <georges@racinet.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id$

import unittest
from Products.CPSDefault.tests.CPSTestCase import CPSTestCase

import os

from Acquisition import aq_base
from OFS.Image import Image
from Products.CPSUtil.text import get_final_encoding

from Products.CPSSchemas.BasicWidgets import CPSImageWidget as OldImageWidget
from Products.CPSSchemas.BasicWidgets import CPSStringWidget
from Products.CPSSchemas.ExtendedWidgets import CPSPhotoWidget as OldPhotoWidget
from Products.CPSSchemas.widgets.image import CPSImageWidget
from Products.CPSSchemas.widgets.indirect import IndirectWidget
from Products.CPSSchemas.tests.testWidgets import TEST_IMAGE

from Products.CPSDocument.upgrade import upgrade_flexible_widget_indirect
from Products.CPSDocument.upgrade import upgrade_flexible_widgets_indirect
from Products.CPSDocument.upgrade import FLEXIBLE_LAYOUTS
from Products.CPSDocument.upgrade import upgrade_doc_unicode
from Products.CPSDocument.upgrade import upgrade_image_widget
from Products.CPSDocument.upgrade import upgrade_image_widgets_global
from Products.CPSDocument.upgrade import upgrade_photo_widget

from layer import CPSDocumentLayer

FLEXIBLE_LAYOUTS.append('test_flexible')

class BaseTestUpgrade(CPSTestCase):

    layer = CPSDocumentLayer

    def afterSetUp(self):
        self.login('manager')
        self.fti = self.portal.portal_types['Test Upgrade']

    def initDoc(self):
        fti = self.fti
        self.doc = fti._constructInstance(self.portal, 'upgrade')
        self.doc.portal_type = fti.getId()

    def initLayout(self, layout_id):
        self.layout_id = layout_id
        layout = self.layout = self.portal.portal_layouts[layout_id]
        return layout

    def makeOldFlexibleWidget(self, tplwid, wid=''):
        """Return widget, layout, template widget, template layout
        doesn't rely on official methods: they now make Indirect Widget
        instances.
        """
        if not wid:
            wid = tplwid

        layout_id = self.layout_id
        tpl_layout = self.layout
        tpl_widget = tpl_layout[tplwid]
        doc = self.doc
        fti = self.fti
        fti._makeObjectFlexible(doc)
        layout, schema = fti._getFlexibleLayoutAndSchemaFor(doc, layout_id)
        widget = aq_base(tpl_widget)
        widget._setId(wid)
        layout.addSubObject(widget)
        widget = layout[wid]
        fti._createFieldsForFlexibleWidget(schema, widget, tpl_widget)

        return layout[wid], layout, tpl_widget, tpl_layout

    @classmethod
    def doc_set(self, doc, **kw):
        """Avoid datamodel present of future side effects.

        The goal is to reproduce situations anterior to upgrade or partially
        upgraded data

        assume AttributeStorageAdapter."""
        for k, v in kw.items():
            setattr(doc, k, v)

    def beforeTearDown(self):
        self.logout()

class TestFlexibleUpgrade(BaseTestUpgrade):
    """Provide helpers for upgrade tests on flexible widgets."""

    def afterSetUp(self):
        BaseTestUpgrade.afterSetUp(self)
        self.initLayout('test_flexible')
        self.initDoc()

    def test_upgrade_indirect(self):
        utool = self.portal.portal_url
        widget, layout, tpl_w, tpl_l = self.makeOldFlexibleWidget('link_title')
        upgrade_flexible_widget_indirect(utool, self.doc, widget,
                                         layout, tpl_w, tpl_l)

        widget = layout['link_title']
        self.assertEquals(widget.fields, ('link_title_f0',))

    def test_upgrade_indirect_compound(self):
        utool = self.portal.portal_url
        subw_ids = ('link_title', 'link_href', 'link_description')
        for swid in subw_ids:
            self.makeOldFlexibleWidget(swid)
        widget, layout, tpl_w, tpl_l = self.makeOldFlexibleWidget('link')
        widget.widget_ids = subw_ids

        upgrade_flexible_widget_indirect(utool, self.doc, widget,
                                         layout, tpl_w, tpl_l)

        for swid in subw_ids:
            self.assertTrue(layout.has_key(swid))
        widget = layout['link']
        self.assertEquals(widget.widget_ids, subw_ids)

    def test_upgrade_indirect_template(self):
        # #2394: skip old templates widgets
        utool = self.portal.portal_url
        widget, layout, tpl_w, tpl_l = self.makeOldFlexibleWidget('link_title')
        widget.fields = ('?',)
        upgrade_flexible_widget_indirect(utool, self.doc, widget,
                                         layout, tpl_w, tpl_l)

        self.assertEquals(layout.keys(), [])

    def test_upgrade_indirect_compound_tpl(self):
        # #2394: skip compound of old templates widgets
        # these compounds may have an empty tuple of fields instead of ('?')
        utool = self.portal.portal_url
        subw_ids = ('link_title', 'link_href', 'link_description')
        for swid in subw_ids:
            sw = self.makeOldFlexibleWidget(swid)[0]
            sw.fields = ('?',)

        widget, layout, tpl_w, tpl_l = self.makeOldFlexibleWidget('link')
        widget.widget_ids = subw_ids

        upgrade_flexible_widget_indirect(utool, self.doc, widget,
                                         layout, tpl_w, tpl_l)

        self.assertEquals(layout.keys(), [])

    def test_full_upgrade(self):
        # test the whole looping
        portal = self.portal
        ws = portal.workspaces
        portal.portal_workflow.invokeFactoryFor(ws, self.fti.getId(), 'test')
        proxy = ws.test
        self.doc = proxy.getContent()
        self.makeOldFlexibleWidget('link_title')

        upgrade_flexible_widgets_indirect(self.portal, commit=False)
        w = self.doc['.cps_layouts'][self.layout_id]['link_title']
        self.assertTrue(isinstance(w, IndirectWidget))

class TestUnicodeUpgrade(BaseTestUpgrade):

    def check_string(self, input, output):
        """Set the doc with input in string field, upgrade, check output"""
        doc = self.fti.constructInstance(self.portal, 'upgrade')
        self.doc_set(doc, string=input)

        self.assertTrue(upgrade_doc_unicode(doc))

        dm = doc.getDataModel()
        self.assertEquals(dm['string'], output)
        self.portal.manage_delObjects(['upgrade',])

    def test_upgrade(self):
        # A whole run
        doc = self.fti.constructInstance(self.portal, 'upgrade')

        # avoiding dm side effects by setting attrs directly
        self.doc_set(doc, string='a\xe9', ascii_string='abcd',
                     string_list=['\xe0', 'abc', u'xy', '\xe9', u'\xe9'],
                     ascii_string_list=['abc', u'xy'])

        self.assertTrue(upgrade_doc_unicode(doc))

        dm = doc.getDataModel()
        self.assertEquals(dm['string'], u'a\xe9')
        self.assertEquals(dm['ascii_string'], 'abcd')
        self.assertEquals(dm['string_list'], [u'\xe0', u'abc', u'xy',
                                              u'\xe9', u'\xe9'])
        self.assertEquals(dm['ascii_string_list'],
                          ['abc', 'xy'])
    def test_upgrade_entities(self):
        self.check_string('See what I mean &#8230;', u'See what I mean \u2026')
        self.check_string('&#8230; Abusing of ellipsis &#8230;',
                          u'\u2026 Abusing of ellipsis \u2026')
        self.check_string('Av\xe9 l&#8217;assent !', u'Av\xe9 l\u2019assent !')

    def test_upgrade_entities_list(self):
        doc = self.fti.constructInstance(self.portal, 'upgrade')
        self.doc_set(doc, string_list=[u'\xe0', '\xe9', 'I mean &#8230;'])
        self.assertTrue(upgrade_doc_unicode(doc))

        dm = doc.getDataModel()
        self.assertEquals(dm['string_list'],
                          [u'\xe0', u'\xe9', u'I mean \u2026'])

    def test_upgrade_entities_u2u(self):
        # Here input is already unicode, but entities haven't been decoded yet
        # typical of partial upgrades
        self.check_string(u'See what I mean &#8230;', u'See what I mean \u2026')
        self.check_string(u'&#8230; Abusing of ellipsis &#8230;',
                          u'\u2026 Abusing of ellipsis \u2026')
        self.check_string(u'Av\xe9 l&#8217;assent !', u'Av\xe9 l\u2019assent !')

class TestImageWidgetUpgrade(BaseTestUpgrade):

    layer = CPSDocumentLayer

    petit_chat_path = os.path.join(os.path.dirname(__file__), 'petit-chat.png')

    def afterSetUp(self):
        self.login('manager')
        fti = self.fti = self.portal.portal_types['Test Image Upgrade']
        self.initDoc()
        layout = self.initLayout('test_image_upgrade')

        layout.addSubObject(OldImageWidget('res_ok'))
        widget = layout['res_ok']
        widget.manage_changeProperties(display_width=320, display_height=200,
                                       fields=('?',), allow_resize=True)

        layout.addSubObject(OldImageWidget('no_res'))
        widget = layout['no_res']
        widget.manage_changeProperties(display_width=320, display_height=200,
                                       fields=('?',), allow_resize=False)

        layout.addSubObject(OldPhotoWidget('photo'))
        widget = layout['photo']
        widget.manage_changeProperties(display_width=320, display_height=200,
                                       fields=('?',))

    def test_upgrade_no_resize(self):
        wid = 'no_res'
        widget, layout, tpl_widget, tpl_layout = self.makeOldFlexibleWidget(wid)
        self.assertEquals(widget.__class__, OldImageWidget)

        upgrade_image_widget(self.doc, layout[wid], layout,
                             tpl_layout, tpl_widget)

        upgraded = layout[wid]
        self.assertEquals(upgraded.__class__, CPSImageWidget)
        self.assertEquals(upgraded.size_spec, 'l320')
        self.assertEquals(upgraded.widget_ids, ())

    def test_upgrade_resize_2411(self):
        # see issue #2411
        self.layout.addSubObject(CPSStringWidget('display_size'))
        upgrade_image_widgets_global(self.portal)

    def test_upgrade_resize(self):
        wid = 'res_ok'
        widget, layout, tpl_widget, tpl_layout = self.makeOldFlexibleWidget(wid)
        self.assertEquals(widget.__class__, OldImageWidget)

        doc = self.doc
        fid = widget.fields[0]
        dm = doc.getDataModel()
        dm[fid] = Image(fid, 'ze_image.png', TEST_IMAGE)
        dm._commitData()

        upgrade_image_widget(doc, layout[wid], layout, tpl_layout, tpl_widget)
        upgraded = layout[wid]
        self.assertEquals(upgraded.__class__, CPSImageWidget)
        self.assertEquals(upgraded.size_spec, 'l320')
        self.assertEquals(upgraded.widget_ids, ('display_size',))

        size_widget = layout['display_size']
        dm = doc.getDataModel()
        self.assertEquals(dm[size_widget.fields[0]], 32)

    def test_upgrade_with_suffix(self):
        doc = self.doc
        # upgrade a first version of the template widget so that we'll get _1
        widget, layout, tpl_widget, tpl_layout = self.makeOldFlexibleWidget(
            'res_ok')
        upgrade_image_widget(doc, layout['res_ok'], layout,
                             tpl_layout, tpl_widget)

        widget, layout, tpl_widget, tpl_layout = self.makeOldFlexibleWidget(
            'res_ok', wid='res_ok_1')
        fid = widget.fields[0]
        dm = doc.getDataModel()
        dm[fid] = Image(fid, 'ze_image.png', TEST_IMAGE)
        dm._commitData()

        upgrade_image_widget(self.doc, widget, layout, tpl_layout, tpl_widget)

        upgraded = layout['res_ok_1']
        self.assertEquals(upgraded.__class__, CPSImageWidget)
        self.assertEquals(upgraded.size_spec, 'l320')
        self.assertEquals(upgraded.widget_ids, ('display_size_1',))

        size_widget = layout['display_size_1']
        dm = doc.getDataModel()
        self.assertEquals(dm[size_widget.fields[0]], 32)

    def test_upgrade_photo(self):
        wid = 'photo'
        widget, layout, tpl_widget, tpl_layout = self.makeOldFlexibleWidget(wid)
        self.assertEquals(widget.__class__, OldPhotoWidget)

        doc = self.doc
        fid = widget.fields[0]
        original_fid = widget.fields[3]
        dm = doc.getDataModel()
        dm[fid] = Image(fid, 'ze_image.png', TEST_IMAGE)
        dm[original_fid] = Image(original_fid, 'petit chat',
                                 open(self.petit_chat_path))
        dm._commitData()

        upgrade_photo_widget(doc, layout[wid], layout, tpl_layout, tpl_widget)

        upgraded = layout[wid]
        self.assertEquals(upgraded.__class__, CPSImageWidget)
        self.assertEquals(upgraded.size_spec, 'l320')
        self.assertEquals(upgraded.widget_ids, ('display_size',))
        self.assertEquals(len(upgraded.fields), 5)

        size_widget = layout['display_size']
        dm = doc.getDataModel()
        self.assertEquals(dm[size_widget.fields[0]], 32)
        self.assertEquals(dm[upgraded.fields[0]].title, 'petit chat')

    def test_upgrade_photo_zombie(self):
        # see #2415
        wid = 'photo'
        widget, layout, tpl_widget, tpl_layout = self.makeOldFlexibleWidget(wid)
        self.assertEquals(widget.__class__, OldPhotoWidget)

        doc = self.doc
        fid = widget.fields[0]
        original_fid = widget.fields[3]
        dm = doc.getDataModel()
        dm[original_fid] = Image(original_fid, 'petit chat',
                                 open(self.petit_chat_path))
        # no main field : as if the image had been deleted
        dm._commitData()

        upgrade_photo_widget(doc, layout[wid], layout, tpl_layout, tpl_widget)

        upgraded = layout[wid]
        dm = doc.getDataModel()
        self.assertEquals(dm[upgraded.fields[0]], None) # no zombie raised


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFlexibleUpgrade))
    suite.addTest(unittest.makeSuite(TestUnicodeUpgrade))
    suite.addTest(unittest.makeSuite(TestImageWidgetUpgrade))
    return suite
