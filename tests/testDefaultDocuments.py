# TODO: 
# - don't depend on getDocumentSchemas / getDocumentTypes but is there
#   an API for that ?

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from pprint import pprint
import unittest
from Testing import ZopeTestCase
import CPSDocumentTestCase


class TestDocuments(CPSDocumentTestCase.CPSDocumentTestCase):
    def afterSetUp(self):
        self.login('root')
        self.ws = self.portal.workspaces
        self.document_schemas = self.portal.getDocumentSchemas()
        self.document_types = self.portal.getDocumentTypes()

    def beforeTearDown(self):
        self.logout()

    def testCreateDocumentsInWorkspacesRoot(self):
        for doc_type in self.document_types.keys():
            doc_id = doc_type.lower()
            self.ws.invokeFactory(doc_type, doc_id)
            self._testDefaultAttributes(doc_id)
            self._testInterfaces(doc_id)

    def _testDefaultAttributes(self, doc_id):
        doc = getattr(self.ws, doc_id)
        # Edit doc to set default values
        doc = doc.getContent()
        doc.edit()

        type_info = doc.getTypeInfo()

        for schema in type_info.schemas:
            for prop_name in self.document_schemas[schema].keys():
                self.assert_(hasattr(doc, prop_name))

    def _testInterfaces(self, doc_id):
        from Interface.Verify import verifyClass
        from Products.CMFCore.interfaces.Dynamic \
            import DynamicType as IDynamicType
        from Products.CMFCore.interfaces.Contentish \
            import Contentish as IContentish
        from Products.CMFCore.interfaces.DublinCore \
            import DublinCore as IDublinCore

        doc = getattr(self.ws, doc_id).getContent()
        verifyClass(IDynamicType, doc.__class__)
        verifyClass(IContentish, doc.__class__)
        # XXX: CPSDocument inherits from DefaultDublinCoreImpl
        # so this test should pass -> ???
        #verifyClass(IDublinCore, doc.__class__)


    # XXX: this should work by fixing ZTC (add some methode to the
    # fake RESPONSE object)
    #def testCreateDocumentsInWorkspacesRootThroughWFTool(self):
    #    wft = self.portal.portal_workflow
    #    for doc_type in DEFAULT_DOCUMENT_TYPES:
    #        wft.invokeFactory(self.ws, doc_type, doc_type.lower())

    def testNews(self):
        self.ws.invokeFactory('News', 'news')
        # XXX: I don't get that part

        doc = self.ws.news.getContent()
        # XXX: you have to edit object before it has its default values.
        doc.edit()

        # Test doc has default values
        for prop_name in self.document_schemas['news'].keys():
            # XXX: Default values are not always as defined in
            # getDocumentSchemas(). I consider this as a bug.
            self.assert_(hasattr(doc, prop_name))

    def testFlexible(self):
        self.ws.invokeFactory('Flexible', 'flex')
        doc = self.ws.flex.getContent()
        doc.edit()

        # XXX: what next?


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDocuments))
    return suite

