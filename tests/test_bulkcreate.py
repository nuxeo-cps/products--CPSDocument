# This test involves CPSDefault document types and should move to CPSDefault
# or be rewritten in a different manner

import unittest, os, StringIO

from OFS.Image import File
from Products.CPSDefault.tests.CPSTestCase import CPSTestCase
from Products.CPSDocument.createFile import createFile
from Products.CMFCore.utils import getToolByName

class TestCreateFile(CPSTestCase):

    def afterSetUp(self):
        self.login('manager')
        self.ws = self.portal.workspaces
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        ttool = getToolByName(self.portal, 'portal_types')
        ttool['ImageGallery'].manage_changeProperties(
            auto_content_types=("image/.*:Image:preview",))
        ttool['Workspace'].manage_changeProperties(
            auto_content_types=("image/.*:Image:preview",
                                ".*:File:file",))

    def _makeZipFile(self, fname='toto.zip'):
        filename = os.path.join(os.path.dirname(__file__), fname)
        file = StringIO.StringIO(open(filename).read())
        return file

    def test_withNone(self):
        createFile(self.ws, None)

    def test_createFileWithName(self):
        archive = self._makeZipFile()
        archive.name = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=False)
        self.assert_('endives' in self.ws.objectIds())
        self.assert_('felix' in self.ws.objectIds())
        self.assert_('petit-chat' in self.ws.objectIds())
        self.assert_('testcreatefile' in self.ws.objectIds())

    def test_createFile_encoding_robustness(self):
        archive = self._makeZipFile('non-utf8.zip')
        archive.name = "non-utf8.zip"
        self.portal.default_charset = 'utf-8'
        from Products.CPSUtil.text import toAscii
        createFile(self.ws, archive, check_allowed_content_types=False)
        self.assert_(self.ws.hasObject(toAscii('f\xe9lin')))

    def test_createFileWithFileName(self):
        archive = self._makeZipFile()
        archive.archivename = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=False)
        self.assert_('endives' in self.ws.objectIds())
        self.assert_('felix' in self.ws.objectIds())
        self.assert_('petit-chat' in self.ws.objectIds())
        self.assert_('testcreatefile' in self.ws.objectIds())

    def test_detectPortalType(self):
        archive = self._makeZipFile()
        archive.name = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=False)
        image_ids = ('endives', 'felix', 'petit-chat')
        for id in image_ids:
            image = getattr(self.ws, id)
            self.assertEquals(image.portal_type, 'Image')
            self.assert_(image.getContent()['preview'] is not None)

        otherfile = getattr(self.ws, 'testcreatefile')
        self.assertEquals(otherfile.portal_type, 'File')
        self.assert_(otherfile.getContent()['file'] is not None)

    def test_createFileWithCheckAllowedContentTypes(self):
        archive = self._makeZipFile()
        archive.archivename = "toto.zip"
        createFile(self.ws, archive, check_allowed_content_types=True)
        ws = self.ws
        # Worspace allows File but not Image
        self.assert_(ws.hasObject('endives'))
        self.assert_(ws.hasObject('felix'))
        self.assert_(ws.hasObject('petit-chat'))
        self.assert_(ws.hasObject('testcreatefile'))
        self.assertEquals(ws['endives'].portal_type, 'File')
        self.assertEquals(ws['felix'].portal_type, 'File')
        self.assertEquals(ws['petit-chat'].portal_type, 'File')
        self.assertEquals(ws['testcreatefile'].portal_type, 'File')

    def test_createFileWithCheckAllowedContentTypes2(self):
        archive = self._makeZipFile()
        archive.name = "toto.zip"
        wftool = getToolByName(self.portal, 'portal_workflow')

        # create a sample image gallery
        ig_id = wftool.invokeFactoryFor(self.ws, 'ImageGallery', 'test_ig')
        ig = getattr(self.ws, ig_id)

        # do not create file as sub objects of an image gallery
        createFile(ig, archive, check_allowed_content_types=True)
        self.assert_(ig.hasObject('endives'))
        self.assert_(ig.hasObject('felix'))
        self.assert_(ig.hasObject('petit-chat'))
        self.failIf(ig.hasObject('testcreatefile'))
        self.assertEquals(ig['endives'].portal_type, 'Image')
        self.assertEquals(ig['felix'].portal_type, 'Image')
        self.assertEquals(ig['petit-chat'].portal_type, 'Image')

    def test_directBulkCreation(self):
        # test creation of the container and bulk import therein in one shot
        archive = File('ziparchiveuploader', 'toto.zip', self._makeZipFile())
        ig_id = self.wftool.invokeFactoryFor(
            self.ws, 'ImageGallery', 'test_ig',
            ziparchiveuploader=archive, wf_before_content=True)

        ig = getattr(self.ws, ig_id)
        self.assert_(ig.hasObject('endives'))
        self.assert_(ig.hasObject('felix'))
        self.assert_(ig.hasObject('petit-chat'))
        self.failIf(ig.hasObject('testcreatefile'))
        self.assertEquals(ig['endives'].portal_type, 'Image')
        self.assertEquals(ig['felix'].portal_type, 'Image')
        self.assertEquals(ig['petit-chat'].portal_type, 'Image')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCreateFile))
    return suite
