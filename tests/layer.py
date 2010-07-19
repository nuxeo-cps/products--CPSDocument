# Copyright (c) 2010 Georges Racinet
# Author : Georges Racinet <gracinet@nuxeo.com>
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

import transaction
import unittest
from Testing import ZopeTestCase
from Products.GenericSetup import profile_registry
from Products.GenericSetup import EXTENSION
from Products.CMFCore.utils import getToolByName
from Products.CPSCore.interfaces import ICPSSite


from Products.CPSSchemas.tests.testWidgets import (
    FakeDataModel, FakeDataStructure, fakePortal,
    )
from Products.CPSDefault.tests.CPSTestCase import (
    CPSTestCase,
    ExtensionProfileLayerClass)

# CPSDocument:tests : add more schemas, layouts and types
profile_registry.registerProfile(
    'tests',
    'CPS Documents Tests',
    "Tests",
    'tests/profile',
    'CPSDocument',
    EXTENSION,
    for_=ICPSSite)

class CPSDocumentLayerClass(ExtensionProfileLayerClass):
    extension_ids = ('CPSDocument:tests',)

CPSDocumentLayer = CPSDocumentLayerClass(
    __name__,
    'CPSDocumentLayer'
    )
