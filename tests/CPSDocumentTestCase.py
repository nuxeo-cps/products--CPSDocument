from Testing import ZopeTestCase
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSDocument')
ZopeTestCase.installProduct('CPSSchemas')

CPSTestCase.setupPortal(CPSTestCase.CPSInstaller)

CPSDocumentTestCase = CPSTestCase.CPSTestCase

