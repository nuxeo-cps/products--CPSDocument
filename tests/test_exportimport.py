# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
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
"""Test GenericSetup I/O
"""

import unittest
from Testing.ZopeTestCase import ZopeTestCase

from zope.interface import implements
from zope.app.testing import placelesssetup
from Products.Five import zcml

from Products.CPSDocument.interfaces import ICPSDocument

from Products.GenericSetup.tests.common import DummyImportContext
from Products.GenericSetup.tests.common import DummyExportContext
from Products.GenericSetup.testing import DummyLogger
from Products.GenericSetup.tests.common import DOMComparator
from OFS.Image import File
from OFS.Folder import Folder

from Products.CPSDocument.exportimport import importCPSObjects
from Products.CPSDocument.exportimport import exportCPSObjects


class FakeTI(object):
    def _commitDM(self, datamodel):
        pass

class FakeDM(object):
    def _itemsWithFields(self):
        return ()

class FakeCPSDocument(Folder):
    implements(ICPSDocument)
    meta_type = "fakedoc"
    def getTypeInfo(self):
        return FakeTI()
    def getDataModel(self):
        return FakeDM()
    def getPortalTypeName(self):
        return 'Fake Doc'

def dummyLog(self, level, msg, *args, **kwargs):
    self._messages.append((level, self._id, msg))
DummyLogger.log = dummyLog


_IMPORT_FOLDER = """\
<?xml version="1.0"?>
<object>
  <object name="sub" meta_type="File" title="thetitle"/>
</object>
"""

_IMPORT_FOLDER_NOTITLE = """\
<?xml version="1.0"?>
<object>
  <object name="sub" meta_type="File"/>
</object>
"""

_EXPORT_FOLDER = """\
<?xml version="1.0"?>
<object name="folder" meta_type="fakedoc" portal_type="Fake Doc">
  <object name="sub" meta_type="File" title="thetitle"/>
</object>
"""

_FILE_CONTENT = """some file content"""


class OFSFileIOTests(ZopeTestCase, DOMComparator):

    # Tests File IO. Also tests in part importCPSObjects and
    # exportCPSObjects and the CPSObjectManagerHelpers class

    def afterSetUp(self):
        import Products.Five
        import Products.CPSCore
        import Products.CPSDocument
        placelesssetup.setUp()
        zcml.load_config('meta.zcml', Products.Five)
        zcml.load_config('permissions.zcml', Products.Five)
        zcml.load_config('meta.zcml', Products.CPSCore)
        zcml.load_config('configure.zcml', Products.CPSDocument)

    def beforeTearDown(self):
        placelesssetup.tearDown()

    def test_import(self):
        site = Folder('site')
        context = DummyImportContext(site)
        context._files['folder.xml'] = _IMPORT_FOLDER
        context._files['folder/sub'] = _FILE_CONTENT

        ob = FakeCPSDocument('folder')
        importCPSObjects(ob, '', context)

        self.assertEquals(ob.objectIds(), ['sub'])
        self.assertEquals(ob.sub.getId(), 'sub')
        self.assertEquals(str(ob.sub), _FILE_CONTENT)
        self.assertEquals(ob.sub.title, 'thetitle')

    def test_import_notitle(self):
        site = Folder('site')
        context = DummyImportContext(site)
        context._files['folder.xml'] = _IMPORT_FOLDER_NOTITLE
        context._files['folder/sub'] = _FILE_CONTENT

        ob = FakeCPSDocument('folder')
        importCPSObjects(ob, '', context)

        self.assertEquals(ob.objectIds(), ['sub'])
        self.assertEquals(ob.sub.getId(), 'sub')
        self.assertEquals(str(ob.sub), _FILE_CONTENT)
        self.assertEquals(ob.sub.title, 'sub') # default title to id

    def test_export(self):
        site = Folder('site')
        context = DummyExportContext(site)

        ob = FakeCPSDocument('folder')
        f = File('sub', 'thetitle', _FILE_CONTENT, content_type='image/test')
        ob._setObject('sub', f)

        exportCPSObjects(ob, '', context)
        self.assertEquals(len(context._wrote), 2)

        filename, text, content_type = context._wrote[0]
        self.assertEquals(filename, 'folder.xml' )
        self._compareDOM(text, _EXPORT_FOLDER)
        self.assertEquals(content_type, 'text/xml' )

        filename, text, content_type = context._wrote[1]
        self.assertEquals(filename, 'folder/sub' )
        self.assertEquals(text, _FILE_CONTENT)
        self.assertEquals(content_type, 'image/test' )


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(OFSFileIOTests),
        ))
