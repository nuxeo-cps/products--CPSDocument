# $Id$
# TODO:
# - don't depend on getDocumentSchemas / getDocumentTypes but is there
#   an API for that ?

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from pprint import pprint
import unittest
from DateTime import DateTime
from Testing import ZopeTestCase
import CPSDocumentTestCase
from Products.CPSSchemas.Widget import widgetname

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


def myGetViewFor(obj, view='view'):
    ti = obj.getTypeInfo()
    actions = ti.listActions()
    for action in actions:
        if action.getId() == view:
            return getattr(obj, action.action.text)
    raise "Unverified assumption"


class TestDocuments(CPSDocumentTestCase.CPSDocumentTestCase):
    def afterSetUp(self):
        self.login('root')
        self.ws = self.portal.workspaces
        self.document_schemas = self.portal.getDocumentSchemas()
        self.document_types = self.portal.getDocumentTypes()
        # getFolderContents check SESSION to get user display choice
        self.portal.REQUEST.SESSION = {}
        self.portal.REQUEST.form = {}

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

            # XXX: should be 0 for an empty object, right?
            self.assert_(doc.get_size() >= 0)

            self.assertEquals(doc.getAdditionalContentInfo(proxy), {})

            # Rendering / default view test (on the proxy)
            self._testRendering(doc, proxy=proxy)
            self._testMetadataRendering(doc, proxy=proxy)
            self._testEditRendering(doc, proxy=proxy)

            # XXX: Doesn't work and I don't know why.
            # doc.view()
            # So I'm using this hack instead:
            self.assert_(myGetViewFor(proxy)())

        # Now testing global view for the container
        self.assert_(self.ws.folder_view())


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
        res = doc.render(proxy=proxy)
        self.assert_(res)

    def _testMetadataRendering(self, doc, proxy):
        res = doc.renderEditDetailed(request=None, proxy=proxy,
                                     layout_id='metadata')
        self.assert_(res)

    def _testEditRendering(self, doc, proxy):
        res = doc.renderEditDetailed(request=None, proxy=proxy)
        self.assert_(res)


    def testCreateDocumentsInWorkspacesRootThroughWFTool(self):
        wft = self.portal.portal_workflow
        for doc_type in self.document_types.keys():
            wft.invokeFactoryFor(self.ws, doc_type, doc_type.lower())

    def testMetadata(self):
        id = 'testMetadataNews'
        self.ws.invokeFactory('News', id)
        proxy = getattr(self.ws, id)
        doc = proxy.getContent()
        metadata = ('Title', 'Description', 'Subject',
                    'Contributors', 'EffectiveDate', 'ExpirationDate',
                    'Rights', 'Relation', 'Source', 'Coverage')
        data = {}
        form = {}
        for d in metadata:
            if d == 'Relation':
                v = 'http://www.nuxeo.com'
            elif d in ('EffectiveDate', 'ExpirationDate'):
                date = '01/01/2004'
                hour = '23'
                minute = '59'
                v = DateTime('%s %s:%s' % (date, hour, minute))
                form[widgetname(d + '_date')] = date
                form[widgetname(d + '_hour')] = hour
                form[widgetname(d + '_minute')] = minute
            elif d == 'Contributors':
                v = ['The %s' % d]
            elif d in ('Subject',):
                v = []
            else:
                v = 'The %s' % d
            data[d] = v
            form[widgetname(d)] = v

        request = self.portal.REQUEST
        request.form = form
        rendered, is_valid, ds = doc.renderEditDetailed(request=request,
                                                        layout_id='metadata')
        self.assert_(is_valid, 'invalid input: ' + str(ds.getErrors()) +
                     'ds = ' + str(ds))
        for k, v in data.items():
            self.assertEquals(ds[k], v)

    def testNews(self):
        self.ws.invokeFactory('News', 'news')
        proxy = getattr(self.ws, 'news')

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
            doc.getAdditionalContentInfo(proxy)['summary'], 'The content')

        from Products.CPSDocument.CPSDocument import SUMMARY_MAX_LEN
        very_long_content = 'A very long content' * 100
        doc.edit(content=very_long_content)
        self.assertEquals(
            doc.getAdditionalContentInfo(proxy)['summary'],
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
