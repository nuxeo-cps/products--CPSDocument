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

class DummyResponse:
    def __init__(self):
        self.headers = {}
        self.data = ''

    def setHeader(self, key, value):
        self.headers[key] = value

    def write(self, data):
        self.data += data

    def redirect(self, url):
        self.redirect_url = url


def randomText(max_len=10):
    import random
    return ''.join(
        [chr(random.randint(32, 128)) for i in range(0, max_len)])


class TestDocuments(CPSDocumentTestCase.CPSDocumentTestCase):
    def afterSetUp(self):
        self.login('root')
        self.ws = self.portal.workspaces
        self.document_schemas = self.portal.getDocumentSchemas()
        self.document_types = self.portal.getDocumentTypes()
        # getFolderContents check SESSION to get user display choice
        self.portal.REQUEST.SESSION = {}

    def beforeTearDown(self):
        self.logout()

    def testCreateDocumentsInWorkspacesRoot(self):
        for doc_type in self.document_types.keys():
            doc_id = doc_type.lower()
            self.ws.invokeFactory(doc_type, doc_id)
            proxy = getattr(self.ws, doc_id)
            doc = proxy.getContent()
            # Edit doc to set default values
            doc.edit()

            self._testInterfaces(doc)
            self._testDefaultAttributes(doc)
            self._testRendering(doc, proxy=proxy)

            # XXX: should be 0 for an empty object, right?
            self.assert_(doc.get_size() >= 0)

            self.assertEquals(doc.getAdditionalContentInfo(), {})

    def _testDefaultAttributes(self, doc):
        type_info = doc.getTypeInfo()

        for schema in type_info.schemas:
            for prop_name in self.document_schemas[schema].keys():
                self.assert_(hasattr(doc, prop_name))

    def _testInterfaces(self, doc):
        from Interface.Verify import verifyObject
        from Products.CMFCore.interfaces.Dynamic \
            import DynamicType as IDynamicType
        from Products.CMFCore.interfaces.Contentish \
            import Contentish as IContentish
        from Products.CMFCore.interfaces.DublinCore \
            import DublinCore as IDublinCore

        verifyObject(IDynamicType, doc)
        verifyObject(IContentish, doc)
        verifyObject(IDublinCore, doc)

    def _testRendering(self, doc, proxy):
        doc.render( proxy=proxy )

    def testCreateDocumentsInWorkspacesRootThroughWFTool(self):
        wft = self.portal.portal_workflow
        for doc_type in self.document_types.keys():
            wft.invokeFactoryFor(self.ws, doc_type, doc_type.lower())

    def testNews(self):
        self.ws.invokeFactory('News', 'news')

        doc = self.ws.news.getContent()
        # you have to edit object before it has its default values.
        doc.edit()

        # Test doc has default values
        for prop_name in self.document_schemas['news'].keys():
            # XXX: Default values are not always as defined in
            # getDocumentSchemas(). I consider this as a bug.
            self.assert_(hasattr(doc, prop_name))

        doc.edit(Title='The title')
        self.assertEquals(doc.Title(), 'The title')

        doc.edit(content='The content')
        self.assertEquals(doc.content, 'The content')
        self.assertEquals(
            doc.getAdditionalContentInfo()['summary'], 'The content')

        from Products.CPSDocument.CPSDocument import SUMMARY_MAX_LEN
        very_long_content = 'A very long content' * 100
        doc.edit(content=very_long_content)
        self.assertEquals(
            doc.getAdditionalContentInfo()['summary'],
            very_long_content[0:SUMMARY_MAX_LEN] + '...')


    def testFile(self):
        self.ws.invokeFactory('File', 'file')

        doc = self.ws.file.getContent()
        # you have to edit object before it has its default values.
        doc.edit()

        # Default value. Shouldn't it be '' ?
        self.assertEquals(doc.file, None)

        # edit file as string
        text = randomText()
        doc.edit(file=text)
        self.assertEquals(doc.file, text)

        self.assertEquals(doc.downloadFile('file'), text)

        response = DummyResponse()
        doc.downloadFile('file', response)
        self.assertEquals(response.data, text)
        self.assertEquals(response.headers['Content-Type'],
            'application/octet-stream')
        self.assertEquals(response.headers['Content-Length'],
            len(text))
        self.assertEquals(response.headers['Content-Disposition'],
            "inline; filename=file")

    if 0: # Don't know hown to do that
        # edit
        class FieldStorage:
            def __init__(self, **kw):
                for k, v in kw.items():
                    setattr(self, k, v)
        from StringIO import StringIO
        from ZPublisher.HTTPRequest import FileUpload
        text = randomText()
        file = StringIO(text)
        fs = FieldStorage(file=file, headers={"Content-Type": "text/html"},
            filename="filename")
        fileupload = FileUpload(fs)

        doc.renderEdit(file=fileupload)

        response = DummyResponse()
        doc.downloadFile('file', response)
        self.assertEquals(response.data, text)
        self.assertEquals(response.headers['Content-Type'],
            'application/octet-stream')
        self.assertEquals(response.headers['Content-Length'],
            len(text))
        self.assertEquals(response.headers['Content-Disposition'],
            "inline; filename=filename")

    def testFlexible(self):
        self.ws.invokeFactory('Flexible', 'flex')
        doc = self.ws.flex.getContent()
        doc.edit()

        # XXX: what next?


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDocuments))
    return suite
