from Testing import ZopeTestCase

from Products.ExternalMethod.ExternalMethod import ExternalMethod

try:
    from Products.CPSDefault.tests import CPSTestCase
    IS_CPS3 = 1
except ImportError:
    from Products.CPSDocument.tests import CMFTestCase
    IS_CPS3 = 0

# CPS3 or stock CMF
# Use a different installer class
if IS_CPS3:
    CPSTestCase.setupPortal()
    CPSDocumentTestCase = CPSTestCase.CPSTestCase
else:
    class CPSDocumentInstaller(CMFTestCase.CMFInstaller):
        def addPortal(self, id):
            """Override the Default addPortal method installing
            a Default CMF Site

            Will launch the external method for CPSDocument
            """

            # CMF Default Site
            CMFTestCase.CMFInstaller.addPortal(self, id)
            portal = getattr(self.app, id)

            # Install the CPSDocument product
            if 'cpsdocument_installer' not in portal.objectIds():
                cpsdocument_installer = ExternalMethod('cpsdocument_installer',
                                                       '',
                                                       'CPSDocument.install',
                                                       'install')
                portal._setObject('cpsdocument_installer', cpsdocument_installer)
            portal.cpsdocument_installer()

    CMFTestCase.setupPortal(PortalInstaller=CPSDocumentInstaller)
    CPSDocumentTestCase = CMFTestCase.CMFTestCase
