# -*- coding: iso-8859-15 -*-
# Copyright (C) 2003-2005 Nuxeo SARL <http://nuxeo.com>
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

import Testing.ZopeTestCase.ZopeLite
import unittest
from Products.CPSDefault.tests.CPSTestCase import CPSTestCase

from Interface.Verify import verifyClass

from Products.CMFCore.interfaces.portal_types \
     import ContentTypeInformation as IContentTypeInformation

from Products.CMFCore.utils import getToolByName
from Products.CPSSchemas.DataModel import DataModel
from Products.CPSDocument.FlexibleTypeInformation \
    import FlexibleTypeInformation

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

class IntegrationTestFlexibleTypeInformation(CPSTestCase):

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

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestFlexibleTypeInformation),
        unittest.makeSuite(IntegrationTestFlexibleTypeInformation),
        ))


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
