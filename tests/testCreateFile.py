# $Id$

import unittest, os, StringIO
from Products.CPSDefault.tests.CPSTestCase import CPSTestCase

from Products.CPSDocument.createFile import createFile

class TestCreateFile(CPSTestCase):
    def afterSetUp(self):
        self.login('manager')
        self.ws = self.portal.workspaces

    def _makeZipFile(self):
        filename = os.path.join(os.path.dirname(__file__), 'toto.zip')
        file = StringIO.StringIO(open(filename).read())
        return file

    def test_createFileWithName(self):
        file = self._makeZipFile()
        file.name = "toto.zip"
        createFile(self.ws, file)
        self.assert_('endives.gif' in self.ws.objectIds())
        self.assert_('felix.jpg' in self.ws.objectIds())
        self.assert_('petit-chat.png' in self.ws.objectIds())
        self.assert_('testCreateFile.py' in self.ws.objectIds())

    def test_createFileWithFileName(self):
        file = self._makeZipFile()
        file.filename = "toto.zip"
        createFile(self.ws, file)
        self.assert_('endives.gif' in self.ws.objectIds())
        self.assert_('felix.jpg' in self.ws.objectIds())
        self.assert_('petit-chat.png' in self.ws.objectIds())
        self.assert_('testCreateFile.py' in self.ws.objectIds())

    def test_detectPortalType(self):
        archive = self._makeZipFile()
        archive.name = "toto.zip"
        createFile(self.ws, archive)
        image_ids = ('endives.gif', 'felix.jpg', 'petit-chat.png')
        for id in image_ids:
            image = getattr(self.ws, id)
            self.assertEquals(image.portal_type, 'Image')
            self.assert_(image.getContent()['preview'] is not None)

        otherfile = getattr(self.ws, 'testCreateFile.py')
        self.assertEquals(otherfile.portal_type, 'File')
        self.assert_(otherfile.getContent()['file'] is not None)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCreateFile))
    return suite
