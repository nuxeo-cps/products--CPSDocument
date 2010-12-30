# -*- coding: iso-8859-15 -*-
# Copyright (C) 2003-2006 Nuxeo SAS <http://nuxeo.com>
# Author: Florent Guillaume <fg@nuxeo.com>
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
"""Tests for Flexible Type Information.
"""

import unittest

from DateTime import DateTime

from Interface.Verify import verifyClass

from Products.CPSDefault.tests.CPSTestCase import CPSTestCase

from Products.CMFCore.interfaces.portal_types \
     import ContentTypeInformation as IContentTypeInformation
from Products.CMFCore.utils import getToolByName

from Products.CPSSchemas.DataModel import DataModel
from Products.CPSDocument.FlexibleTypeInformation \
    import FlexibleTypeInformation
from Products.PortalTransforms.MimeTypesRegistry import MimeTypesRegistry

class TestFlexibleTypeInformation(unittest.TestCase):

    def test_interfaces(self):
        verifyClass(IContentTypeInformation, FlexibleTypeInformation)

    def test_getLayoutIds(self):
        default = ['foo', 'bar', 'baz']
        ti = FlexibleTypeInformation('myti', layouts=default)
        func = ti.getLayoutIds

        ti.layout_clusters = []
        self.assertEquals(func(), default)
        self.assertEquals(func(cluster='view'), default)
        self.assertEquals(func(cluster='babar'), default)

        ti.layout_clusters = ['view:']
        self.assertEquals(func(), default)
        self.assertEquals(func(cluster='view'), [])
        self.assertEquals(func(cluster='babar'), default)

        ti.layout_clusters = ['view:goldorak']
        self.assertEquals(func(), default)
        self.assertEquals(func(cluster='view'), ['goldorak'])
        self.assertEquals(func(cluster='babar'), default)

        ti.layout_clusters = ['view:blob,mickey']
        self.assertEquals(func(), default)
        self.assertEquals(func(cluster='view'), ['blob', 'mickey'])
        self.assertEquals(func(cluster='babar'), default)

    def test_getAutoContentInfo(self):
        ti = FlexibleTypeInformation('myti')
        ti.mimetypes_registry = MimeTypesRegistry(fill=1)

        # default values for BBB in createFile
        self.assertEquals(ti.getAutoContentInfo(file_name='truc.jpg'),
                          ('Image', 'preview'))
        self.assertEquals(ti.getAutoContentInfo(file_name='truc.ogg'),
                          ('File', 'file'))

        # now let's put some new value
        ti.manage_changeProperties(auto_content_types=(
            ('image/.*:Image:preview'),
            ('audio/.*:Audio Track:audio_file'),
            ('.*:File:file'),
            ))

        self.assertEquals(ti.getAutoContentInfo(file_name='truc.jpg'),
                          ('Image', 'preview'))
        self.assertEquals(ti.getAutoContentInfo(file_name='truc.mp3'),
                          ('Audio Track', 'audio_file'))
        self.assertEquals(ti.getAutoContentInfo(file_name='truc.bin'),
                          ('File', 'file'))
        self.assertEquals(ti.getAutoContentInfo(file_name='truc.bin',
                                                check_allowed=True),
                          (None, None))
        ti.manage_changeProperties(allowed_content_types=('Image', 'File'))
        self.assertEquals(ti.getAutoContentInfo(file_name='truc.bin',
                                                check_allowed=True),
                          ('File', 'file'))


class IntegrationTestFlexibleTypeInformation(CPSTestCase):
    """Tests needing full CPS rig. Warning: depends on structure of News Item.
    """

    def afterSetUp(self):
        self.login('manager')
        self.ttool = ttool = getToolByName(self.portal, 'portal_types')
        self.fti = ttool['News Item']
        wftool = getToolByName(self.portal, 'portal_workflow')
        ws = self.portal.workspaces
        wftool.invokeFactoryFor(ws, 'Workspace', 'testFTI_sandbox')
        self.sandbox = ws.testFTI_sandbox

    def beforeTearDown(self):
        self.portal.workspaces.manage_delObjects(['testFTI_sandbox'])

    def test_constructInstance(self):
        # when supplied with prefilled dm, don't wipe it
        dm = self.fti.getDataModel(None)
        dm['Title'] = 'User written'

        ob = self.fti._constructInstance(self.sandbox, 'the_id', datamodel=dm)
        self.assertEquals(ob.Title(), 'User written')

        # when supplied with bare dm, produce a new dm
        # (couldn't set Title otherwise)
        dm = DataModel(None)
        ob = self.fti._constructInstance(self.sandbox, 'other',
                                         datamodel=dm,
                                         Title='User written')
        self.assertEquals(ob.Title(), 'User written')

    def test_contructInstance_languages(self):
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.invokeFactoryFor(self.sandbox, 'News Item', 'some_news',
                                Title="Some News")
        some_news = self.sandbox.some_news
        first_lang = some_news.getContent().Language()
        some_news.addLanguageToProxy('exotic_language')

        # assertion for #1714
        self.assertEquals(some_news.getContent(lang=first_lang).Title(),
                          "Some News")

    def test_getDataModel(self):
        # fti has metadata and attribute storage adapters
        dm = self.fti.getDataModel(self.sandbox)
        # test keys, may break if new item schema changes
        keys = [
            'Contributors',
            'Coverage',
            'CreationDate',
            'Creator',
            'Description',
            'EffectiveDate',
            'ExpirationDate',
            'Format',
            'Language',
            'ModificationDate',
            'Relation',
            'Rights',
            'Source',
            'Subject',
            'Title',
            'allow_discussion',
            'content',
            'content_format',
            'content_position',
            'keywords',
            'photo',
            'photo_alt',
            'photo_original',
            'photo_position',
            'photo_subtitle',
            'photo_title',
            'preview',
            'preview_alt',
            'preview_title',
            ]
        dm_keys = dm.keys()
        dm_keys.sort()
        self.assertEquals(dm_keys, keys)
        # test set default values
        self.assertEquals(dm['Format'], 'text/html')
        self.assertEquals(dm['Creator'], 'manager')
        self.assertEquals(isinstance(dm['ModificationDate'], DateTime), True)
        self.assertEquals(isinstance(dm['CreationDate'], DateTime), True)

    def testFlexibleAddWidget(self):
        # note that News Item is flexible
        dm = DataModel(None)
        ob = self.fti._constructInstance(self.sandbox, 'ze_ob', datamodel=dm)

        # simple widget
        lid = 'newsitem_flexible'
        simple_w = 'attachedFile'
        self.fti.flexibleAddWidget(ob, lid, simple_w)
        lay, sch = self.fti._getFlexibleLayoutAndSchemaFor(ob, lid)
        self.assertEquals(lay.keys(), [simple_w])
        self.assertEquals(sch.keys(), [('%s_' + f) % simple_w
                                       for f in ('f0', 'f1', 'f2', 'f3')])

    def testFlexibleAddWidget_compound(self):
        # Add a compound widget to News Item
        from Products.CPSSchemas.BasicWidgets import CPSCompoundWidget
        lid = 'newsitem_flexible'
        layout = self.portal.portal_layouts[lid]
        compid = 'comp'
        layout.addSubObject(CPSCompoundWidget(compid))
        comp = layout[compid]
        comp.manage_changeProperties(widget_ids=('attachedFile', 'link_title'),
                                     fields=['?'])

        # make a News Item
        dm = DataModel(None)
        ob = self.fti._constructInstance(self.sandbox, 'ze_ob', datamodel=dm)

        # flexible compound
        self.fti.flexibleAddWidget(ob, lid, compid)
        lay, sch = self.fti._getFlexibleLayoutAndSchemaFor(ob, lid)
        expected = set(comp.widget_ids)
        expected.add(compid)
        self.assertEquals(set(lay.keys()), expected)

        expected = set(lay[comp.widget_ids[0]].fields)
        expected.update(lay[comp.widget_ids[1]].fields)
        self.assertEquals(set(sch.keys()), expected)

        # now test deletion (see #1758, #1817)
        self.fti.flexibleDelWidgets(ob, lid, [compid])
        self.assertEquals(lay.keys(), [])
        self.assertEquals(sch.keys(), [])

    def testFlexibleAddWidget_compound_nested(self):
        # Add a compound widget to News Item
        from Products.CPSSchemas.BasicWidgets import CPSCompoundWidget
        lid = 'newsitem_flexible'
        layout = self.portal.portal_layouts[lid]
        compid = 'comp'
        subcompid = 'link'
        layout.addSubObject(CPSCompoundWidget(compid))
        comp = layout[compid]
        subcomp = layout[subcompid]
        comp.manage_changeProperties(widget_ids=('attachedFile', subcompid),
                                     fields=['?'])
        # make a News Item
        dm = DataModel(None)
        ob = self.fti._constructInstance(self.sandbox, 'ze_ob', datamodel=dm)

        # flexible compound
        self.fti.flexibleAddWidget(ob, lid, compid)
        lay, sch = self.fti._getFlexibleLayoutAndSchemaFor(ob, lid)
        expected = set(comp.widget_ids)
        expected.update(subcomp.widget_ids)
        expected.add(compid)
        self.assertEquals(set(lay.keys()), expected)

        expected = set(lay[comp.widget_ids[0]].fields)
        expected.update(lay[comp.widget_ids[1]].fields)
        for subwid in subcomp.widget_ids:
            expected.update(lay[subwid].fields)
        self.assertEquals(set(sch.keys()), expected)

        # now test deletion (see #1758, #1817)
        self.fti.flexibleDelWidgets(ob, lid, [compid])
        self.assertEquals(lay.keys(), [])
        self.assertEquals(sch.keys(), [])

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestFlexibleTypeInformation),
        unittest.makeSuite(IntegrationTestFlexibleTypeInformation),
        ))


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
