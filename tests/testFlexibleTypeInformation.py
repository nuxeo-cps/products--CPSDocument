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

from Interface.Verify import verifyClass

from Products.CMFCore.interfaces.portal_types \
     import ContentTypeInformation as IContentTypeInformation

from Products.CPSDocument.FlexibleTypeInformation \
    import FlexibleTypeInformation


class TestFlexibleTypeInformation(unittest.TestCase):

    def testInterfaces(self):
        verifyClass(IContentTypeInformation, FlexibleTypeInformation)

    def test_getLayoutIds(self):
        ti = FlexibleTypeInformation('myti')
        ti.layouts = ['foo', 'bar', 'baz']
        basic = ['foo', 'bar', 'baz']
        func = ti.getLayoutIds

        ti.layout_clusters = ['']
        self.assertEquals(func(), basic)
        self.assertEquals(func(cluster='view'), basic)

        ti.layout_clusters = ['view:blob']
        self.assertEquals(func(cluster='view'), ['blob'])

        ti.layout_clusters = ['view:-bar']
        self.assertEquals(func(cluster='view'), ['foo', 'baz'])

        ti.layout_clusters = ['default:hum,ham']
        self.assertEquals(func(cluster='view'), ['hum', 'ham'])

        ti.layout_clusters = ['default:-bar,h']
        self.assertEquals(func(cluster='view'), ['foo', 'baz', 'h'])

        ti.layout_clusters = ['default:be,bop,b', 'view:-bop,arf']
        self.assertEquals(func(cluster='view'), ['be', 'b', 'arf'])

        ti.layout_clusters = ['default:-bar,h', 'view:-baz,i']
        self.assertEquals(func(cluster='view'), ['foo', 'h', 'i'])


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestFlexibleTypeInformation),
        ))


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
