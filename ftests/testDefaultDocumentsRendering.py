# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Nuxeo SARL <http://nuxeo.com>
# Author: Anahide Tchertchian <at@nuxeo.com>
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
"""Tests for default documents rendering

Test are not really unit because rendering is involved, but not really
functional neither (just test that pages do not crash)
"""

import unittest
from Testing import ZopeTestCase

from AccessControl import Unauthorized

from Products.ExternalMethod.ExternalMethod import ExternalMethod

from Products.CMFCore.tests.base.dummy import DummyFolder
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import _getViewFor, getActionContext
from Products.CMFDefault.Portal import manage_addCMFSite

#
# Install products
#

# needed products
ZopeTestCase.installProduct('ZCTextIndex', quiet=1)
ZopeTestCase.installProduct('MailHost', quiet=1)

ZopeTestCase.installProduct('CMFCore', quiet=1)
ZopeTestCase.installProduct('CMFDefault', quiet=1)

ZopeTestCase.installProduct('CPSSchemas', quiet=1)
ZopeTestCase.installProduct('CPSDocument', quiet=1)
ZopeTestCase.installProduct('TranslationService', quiet=1)
ZopeTestCase.installProduct('Localizer', quiet=1)

# required by CPSSchemas
ZopeTestCase.installProduct('PortalTransforms', quiet=1)
ZopeTestCase.installProduct('Epoz', quiet=1)

# The folowing are patches needed because Localizer doesn't work
# well within ZTC

# This one is needed by ProxyTool.
def get_selected_language(self):
    """ """
    return 'en'

from Products.Localizer.Localizer import Localizer
Localizer.get_selected_language = get_selected_language


portal_name = 'portal'

class TestDefaultDocumentsRendering(ZopeTestCase.PortalTestCase):
    """Default document rendering test case:
    - test that actions do not crash for each document type
    """

    #
    # Test case Installer
    #

    def getPortal(self):
        if not hasattr(self.app, portal_name):
            manage_addCMFSite(self.app,
                              portal_name)
        return self.app[portal_name]

    def afterSetUp(self):
        try:
            self.login('manager')
        except AttributeError:
            uf = self.portal.acl_users
            uf._doAddUser('manager', '', ['Manager'], [])
            self.login('manager')
        # Set portal
        self.portal = self.getPortal()

        # Install CPSDocument using the CMF installer (not additional CPS
        # Products required), its installer will call the CPSSchemas installer.
        cpsdocument_installer = ExternalMethod('cpsdocument_installer',
                                               '',
                                               'CPSDocument.install',
                                               'cmfinstall')
        self.portal._setObject('cpsdocument_installer',
                               cpsdocument_installer)
        self.portal.cpsdocument_installer()

        ttool = getToolByName(self.portal, 'portal_types')

        self.content_types = ttool.listContentTypes()
        self.test_documents = self._createTestDocuments()

        self.portal.REQUEST.SESSION = {}
        self.portal.REQUEST.form = {}

    def beforeTearDown(self):
        self.logout()


    #
    # Helper methods
    #


    def _createTestDocuments(self):
        """Create a test document for each doctype in a dummyfolder
        """
        documents = []
        #self.portal._setObject('folder', DummyFolder(id='folder'))
        #self.folder = getattr(self.portal, 'folder')
        for doctype in self.content_types:
            docid = doctype.lower()
            print docid
            try:
                #docid = self.folder.invokeFactory(doctype, docid)
                docid = self.portal.invokeFactory(doctype, docid)
            except Unauthorized:
                # do is not supposed to be created like this, exp: Discussion
                # Item
                print "unauthorized for docid %s, doctype %s"%(docid, doctype)
                continue
            #doc = getattr(self.folder, docid, None)
            doc = getattr(self.portal, docid, None)
            print doc, repr(doc)
            if doc is not None:
                documents.append(doc)
        return documents

    def _getActionTargetAndArguments(self, target):
        """Remove arguments passed in target, to get the actual template/script
        to test.
        """
        if target.startswith('/'):
            target = target[1:]
        ret_kws = {}
        args = target.find('?')
        if args != -1:
            kwargs = target[args+1:].split('&')
            for kwarg in kwargs:
                kws = kwarg.split('=')
                if len(kws) == 2:
                    request.form[kws[0]] = kws[1]
                    ret_kws[kws[0]] = kws[1]
            target = target[:args]
        return (target, ret_kws)

    #
    # Tests begin here
    #

    def testAllDocumentActions(self):
        """Test each action for given document type
        """
        for doc in self.test_documents:
            print doc
            ti = doc.getTypeInfo()
            print ti
            view = _getViewFor(doc)
            if ti is not None:
                context = getActionContext(doc)
                actions = ti.listActions()
                for action in actions:
                    # only test visible actions
                    if action.getVisibility() and action.getId() != 'edit_online':
                        target = action.action(context).strip()
                        # remove args from target
                        target, args = self._getActionTargetAndArguments(target)
                        # some templates need REQUEST to be set
                        request = self.portal.REQUEST
                        meth = doc.restrictedTraverse(target)
                        if view == meth:
                            print "view checked"
                        try:
                            try:
                                self.assert_(meth(request, args))
                            except AssertionError:
                                raise AssertionError("Error for doctype %s and action %s"
                                                     % (ti, action))
                        except TypeError:
                            try:
                                self.assert_(meth(args))
                            except AssertionError:
                                raise AssertionError("Error for doctype %s and action %s"
                                                     % (ti, action))

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestDefaultDocumentsRendering),
        ))


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
