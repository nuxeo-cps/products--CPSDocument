# $Id$

import unittest, os, StringIO

from Products.CPSDefault.tests.CPSTestCase import CPSTestCase
from Products.CPSDocument.createFile import createFile
from Products.CMFCore.utils import getToolByName

class TestCreateFile(CPSTestCase):
    def afterSetUp(self):
        self.login('manager')
        self.ws = self.portal.workspaces

    def _makeZipFile(self):
        filename = os.path.join(os.path.dirname(__file__), 'toto.zip')
        file = StringIO.StringIO(open(filename).read())
        return file

    def test_withNone(self):
        createFile(self.ws, None)

    def test_createFileWithName(self):
        archive = self._makeZipFile()
        archive.name = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=False)
        self.assert_('endives.gif' in self.ws.objectIds())
        self.assert_('felix.jpg' in self.ws.objectIds())
        self.assert_('petit-chat.png' in self.ws.objectIds())
        self.assert_('testCreateFile.py' in self.ws.objectIds())

    def test_createFileWithFileName(self):
        archive = self._makeZipFile()
        archive.archivename = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=False)
        self.assert_('endives.gif' in self.ws.objectIds())
        self.assert_('felix.jpg' in self.ws.objectIds())
        self.assert_('petit-chat.png' in self.ws.objectIds())
        self.assert_('testCreateFile.py' in self.ws.objectIds())

    def test_detectPortalType(self):
        archive = self._makeZipFile()
        archive.name = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=False)
        image_ids = ('endives.gif', 'felix.jpg', 'petit-chat.png')
        for id in image_ids:
            image = getattr(self.ws, id)
            self.assertEquals(image.portal_type, 'Image')
            self.assert_(image.getContent()['preview'] is not None)

        otherfile = getattr(self.ws, 'testCreateFile.py')
        self.assertEquals(otherfile.portal_type, 'File')
        self.assert_(otherfile.getContent()['file'] is not None)

    def test_createFileWithCheckAllowedContentTypes(self):
        archive = self._makeZipFile()
        archive.archivename = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=True)
        self.failIf('endives.gif' in self.ws.objectIds())
        self.failIf('felix.jpg' in self.ws.objectIds())
        self.failIf('petit-chat.png' in self.ws.objectIds())
        self.assert_('testCreateFile.py' in self.ws.objectIds())

    def test_createFileWithCheckAllowedContentTypes2(self):
        archive = self._makeZipFile()
        archive.name = "toto.zip"
        wftool = getToolByName(self.portal, 'portal_workflow')

        # create a sample image gallery
        ig_id = wftool.invokeFactoryFor(self.ws, 'ImageGallery', 'test_ig')
        ig = getattr(self.ws, ig_id)

        # do not create file as sub objects of an image gallery
        createFile(ig, archive, check_allowed_content_types=True)
        self.assert_('endives.gif' in ig.objectIds())
        self.assert_('felix.jpg' in ig.objectIds())
        self.assert_('petit-chat.png' in ig.objectIds())
        self.failIf('testCreateFile.py' in ig.objectIds())




def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCreateFile))
    return suite
