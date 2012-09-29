# -*- coding: iso-8859-15 -*-
# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
# Authors: Julien Anguenot <ja@nuxeo.com>
#          Georges Racinet <gracinet@cps-cms.org>
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
"""Tests CPSDocument
"""

import unittest

from OFS.Image import File

from Products.CPSDefault.tests.CPSTestCase import CPSTestCase
from Products.CPSUtil.tests.web_conformance import assertValidCss

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

        self.assertEqual(info['download_url'],
                         "%s/downloadFile/file/%s?nocache=%s" %
                         (utool.getRelativeUrl(proxy), "filename",
                          ""))

        self.assertEqual(info['preview'],
                         utool.getRelativeUrl(proxy) + '/preview')

        self.assertEqual(info['photo'],
                         utool.getRelativeUrl(proxy) + '/'+ 'image')

    def test_get_attached_files_info(self):
        self.login('manager')

        fobj = File("filename", "filename.pdf", "")

        # first, a basic document type
        proxy_id = self.portal.workspaces.invokeFactory('File', 'file',
                                                        file=fobj)
        proxy = getattr(self.portal.workspaces, proxy_id)
        doc = proxy.getContent()
        files = doc.getAttachedFilesInfo()
        self.assertEquals(len(files), 1)
        self.assertEquals(str(files[0]['mimetype']), 'application/pdf')
        dm = doc.getDataModel(proxy=proxy)
        uri = files[0]['content_url']
        self.assertEquals(uri, dm.fileUri('file'))
        self.assertTrue(uri.endswith('filename.pdf'))

        # now, a flexible document type
        proxy_id = self.portal.workspaces.invokeFactory('Document', 'doc')
        proxy = getattr(self.portal.workspaces, proxy_id)
        doc = proxy.getEditableContent()
        self.assertEquals(len(doc.getAttachedFilesInfo()), 0)

        doc.flexibleAddWidget('flexible_content', 'attachedFile')
        self.assertEquals(len(doc.getAttachedFilesInfo()), 0)

        doc.edit(attachedFile_f0=fobj)
        files = doc.getAttachedFilesInfo()
        self.assertEquals(len(files), 1)
        self.assertEquals(str(files[0]['mimetype']), 'application/pdf')
        dm = doc.getDataModel(proxy=proxy)
        self.assertEquals(files[0]['content_url'],
                          dm.fileUri('attachedFile_f0'))

        doc.flexibleAddWidget('flexible_content', 'attachedFile')
        self.assertEquals(len(doc.getAttachedFilesInfo()), 1)

        fobj2 = File('spam', 'track.ogg', '')
        doc.edit(attachedFile_1_f0=fobj2)
        files = doc.getAttachedFilesInfo()
        self.assertEquals(len(files), 2)
        self.assertEquals(str(files[1]['mimetype']), 'audio/ogg')
        dm = doc.getDataModel(proxy=proxy)
        self.assertEquals(files[1]['content_url'],
                          dm.fileUri('attachedFile_1_f0'))

    def testCss(self):
        ALL_CSS = ['document.css']
        for css_name in ALL_CSS:
            css_body = self.portal[css_name](self.portal)
            assertValidCss(css_body, css_name)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestCPSDocument),
        ))
