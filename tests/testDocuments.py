import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing import ZopeTestCase
import CPSDocumentTestCase

DEFAULT_DOCUMENT_TYPES = ['Flexible', 'FAQ', 'FAQitem', 'Glossary',
    'GlossaryItem', 'News', 'File', 'EventDoc', 'Link', 'Image',
    'ImageGallery']

class TestDocuments(CPSDocumentTestCase.CPSDocumentTestCase):
    def afterSetUp(self):
        self.login('root')

    def beforeTearDown(self):
        self.logout()

    def testCreateDocumentsInWorkspacesRoot(self):
        ws = self.portal.workspaces
        for doc_type in DEFAULT_DOCUMENT_TYPES:
            ws.invokeFactory(doc_type, doc_type.lower())

    def testCreateDocumentsInWorkspacesRootThroughWFTool(self):
        ws = self.portal.workspaces
        wft = self.portal.portal_workflow
        for doc_type in DEFAULT_DOCUMENT_TYPES:
            wft.invokeFactory(ws, doc_type, doc_type.lower())

    #def testArticle(self):
    #    ws = self.portal.workspaces
    #    ws.invokeFactory('Article', 'article')
    #    # XXX: I don't get that part
    #    article = ws.article.getContent()
    #    article = article.getContent()
    #    article.edit(title="Le titre", auteurs="Les auteurs",
    #        description="La description", reference="La référence",
    #        source="La source", commentaire="Le commentaire")
    #        # XXX: add more...
    #    assert article.title == "Le titre"
    #    assert article.auteurs == "Les auteurs"
    #    assert article.description == "La description"
    #    assert article.reference == "La référence"
    #    assert article.source == "La source"
    #    assert article.commentaire == "Le commentaire"


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDocuments))
    return suite

