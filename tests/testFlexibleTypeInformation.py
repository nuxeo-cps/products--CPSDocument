import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from pprint import pprint
import unittest
from Testing import ZopeTestCase
import CPSDocumentTestCase

from Products.CPSDocument.FlexibleTypeInformation \
    import FlexibleTypeInformation


class TestFlexibleTypeInformation(CPSDocumentTestCase.CPSDocumentTestCase):
    #def afterSetUp(self):
    #    self.login('root')

    #def beforeTearDown(self):
    #    self.logout()

    def testInterfaces(self):
        from Interface.Verify import verifyClass
        from Products.CMFCore.interfaces.portal_types \
            import ContentTypeInformation as IContentTypeInformation

        verifyClass(IContentTypeInformation, FlexibleTypeInformation)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFlexibleTypeInformation))
    return suite

