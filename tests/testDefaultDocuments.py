import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from pprint import pprint
import unittest
from Testing import ZopeTestCase
import CPSDocumentTestCase

DEFAULT_DOCUMENT_TYPES = ['Flexible', 'FAQ', 'FAQitem', 'Glossary',
    'GlossaryItem', 'News', 'File', 'EventDoc', 'Link', 'Image',
    'ImageGallery']

class TestDocuments(CPSDocumentTestCase.CPSDocumentTestCase):
    def afterSetUp(self):
        self.login('root')
        self.schemas = self.portal.getDocumentSchemas()

    def beforeTearDown(self):
        self.logout()

    def testCreateDocumentsInWorkspacesRoot(self):
        ws = self.portal.workspaces
        for doc_type in DEFAULT_DOCUMENT_TYPES:
            doc_id = doc_type.lower()
            ws.invokeFactory(doc_type, doc_id)
            self._testDefaultAttributes(doc_id)

    def _testDefaultAttributes(self, doc_id):
        doc = getattr(self.portal.workspaces, doc_id)
        # Edit doc to set default values
        doc = doc.getContent()
        doc.edit()

        # Retrieve doc schema and test if attributes have been created
        doc_type = doc.portal_type
        tt = self.portal.portal_types
        fti = tt[doc_type]
        for schema in fti.schemas:
            for prop_name in self.schemas[schema].keys():
                self.assert_(hasattr(doc, prop_name))

    # XXX: this should work by fixing ZTC (add some methode to the
    # fake RESPONSE object)
    #def testCreateDocumentsInWorkspacesRootThroughWFTool(self):
    #    ws = self.portal.workspaces
    #    wft = self.portal.portal_workflow
    #    for doc_type in DEFAULT_DOCUMENT_TYPES:
    #        wft.invokeFactory(ws, doc_type, doc_type.lower())

    def testNews(self):
        ws = self.portal.workspaces
        ws.invokeFactory('News', 'news')
        # XXX: I don't get that part

        doc = ws.news.getContent()
        # XXX: you have to edit object before it has its default values.
        doc.edit()

        # Test doc has default values
        for prop_name in self.schemas['news'].keys():
            # XXX: Default values are not always as defined in
            # getDocumentSchemas(). I consider this as a bug.
            self.assert_(hasattr(doc, prop_name))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDocuments))
    return suite

