# -*- coding: iso-8859-15 -*-
# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
# Author: Julien Anguenot <ja@nuxeo.com>
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
"""Tests CPSDocument
"""

import unittest

from Acquisition import aq_base
from OFS.Image import File

from Products.CPSDefault.tests.CPSTestCase import CPSTestCase

class TestCPSDocument(CPSTestCase):

    def test_get_add_content_info_virtual_hosting(self):
        # http://svn.nuxeo.org/trac/pub/ticket/967

        self.login('manager')

        utool = self.portal.portal_url

        file_ = File("filename", "filename", "")
        id_ = self.portal.workspaces.invokeFactory('File', 'file',
                                                  file=file_)
        proxy = getattr(self.portal.workspaces, id_)

        # For testing purpose
        setattr(proxy.getContent(), 'preview', True)
        setattr(proxy.getContent(), 'image', True)

        # Generate info
        info = proxy.getContent().getAdditionalContentInfo(proxy)

        f = getattr(proxy.getContent(), 'file')
        self.assertEqual(info['download_url'],
                         "%s/downloadFile/file/%s?nocache=%s" %
                         (utool.getRelativeUrl(proxy), "filename",
                          ""))

        self.assertEqual(info['preview'],
                         utool.getRelativeUrl(proxy) + '/preview')

        self.assertEqual(info['photo'],
                         utool.getRelativeUrl(proxy) + '/'+ 'image')


    def testCss(self):
        ALL_CSS = ['document.css']
        for css_name in ALL_CSS:
            css_body = self.portal[css_name](self.portal)
            self.assertValidCss(css_body, css_name)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestCPSDocument),
        ))

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
