# $Id$

import unittest, os, StringIO
import CPSDocumentTestCase
from Products.CPSDocument.createFile import createFile


class TestCreateFile(CPSDocumentTestCase.CPSDocumentTestCase):
    def afterSetUp(self):
        try:
            self.login('manager')
        except AttributeError:
            # CMF
            uf = self.portal.acl_users
            uf._doAddUser('manager', '', ['Manager'], [])
            self.login('manager')
        try:
            self.ws = self.portal.workspaces
        except AttributeError:
            self.ws = self.portal

    def _makeZipFile(self):
        filename = os.path.join(os.path.dirname(__file__), 'toto.zip')
        file = StringIO.StringIO(open(filename).read())
        file.seek(0)
        return file

    def test_createFileWithName(self):
        file = self._makeZipFile()
        file.name = "toto.zip"
        createFile(self.ws, file)
        self.assert_('Makefile' in self.ws.objectIds())
        self.assert_('framework.py' in self.ws.objectIds())

    def test_createFileWithFileName(self):
        file = self._makeZipFile()
        file.filename = "toto.zip"
        createFile(self.ws, file)
        self.assert_('Makefile' in self.ws.objectIds())
        self.assert_('framework.py' in self.ws.objectIds())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCreateFile))
    return suite
