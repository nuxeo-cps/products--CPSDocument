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
from Products.CPSUtil.text import get_final_encoding

from Products.CPSDocument.upgrade import _upgrade_doc_unicode

from layer import CPSDocumentLayer

class TestUpgrade(CPSTestCase):

    layer = CPSDocumentLayer

    def afterSetUp(self):
        self.login('manager')
        self.fti = self.portal.portal_types['Test Upgrade']

    @classmethod
    def doc_set(self, doc, **kw):
        """Avoid datamodel present of future side effects.

        The goal is to reproduce situations anterior to upgrade or partially
        upgraded data

        assume AttributeStorageAdapter."""
        for k, v in kw.items():
            setattr(doc, k, v)

    def test_upgrade(self):
        # A whole run
        doc = self.fti.constructInstance(self.portal, 'upgrade')
        # avoiding dm side effects by setting attrs directly
        self.doc_set(doc, string='a\xe9', ascii_string='abcd',
                     string_list=['\xe0', 'abc', u'xy', '\xe9', u'\xe9'],
                     ascii_string_list=['abc', u'xy'])

        self.assertTrue(_upgrade_doc_unicode(doc))

        dm = doc.getDataModel()
        self.assertEquals(dm['string'], u'a\xe9')
        self.assertEquals(dm['ascii_string'], 'abcd')
        self.assertEquals(dm['string_list'], [u'\xe0', u'abc', u'xy',
                                              u'\xe9', u'\xe9'])
        self.assertEquals(dm['ascii_string_list'],
                          ['abc', 'xy'])


    def beforeTearDown(self):
        self.logout()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUpgrade))
    return suite
