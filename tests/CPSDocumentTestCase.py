from Testing import ZopeTestCase
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSDocument')
ZopeTestCase.installProduct('CPSSchemas')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('Epoz')

CPSTestCase.setupPortal()

CPSDocumentTestCase = CPSTestCase.CPSTestCase

