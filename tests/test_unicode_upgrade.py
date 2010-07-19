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

from Products.CPSDocument.upgrade import upgrade_doc_unicode

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

        self.assertTrue(upgrade_doc_unicode(doc))

        dm = doc.getDataModel()
        self.assertEquals(dm['string'], u'a\xe9')
        self.assertEquals(dm['ascii_string'], 'abcd')
        self.assertEquals(dm['string_list'], [u'\xe0', u'abc', u'xy',
                                              u'\xe9', u'\xe9'])
        self.assertEquals(dm['ascii_string_list'],
                          ['abc', 'xy'])

    def check_string(self, input, output):
        """Set the doc with input in string field, upgrade, check output"""
        doc = self.fti.constructInstance(self.portal, 'upgrade')
        self.doc_set(doc, string=input)

        self.assertTrue(upgrade_doc_unicode(doc))

        dm = doc.getDataModel()
        self.assertEquals(dm['string'], output)
        self.portal.manage_delObjects(['upgrade',])

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

    def beforeTearDown(self):
        self.logout()


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUpgrade))
    return suite
