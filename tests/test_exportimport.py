# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
# Author: Florent Guillaume <fg@nuxeo.com>
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

import unittest
import cgi
from difflib import ndiff
from xml.dom.minidom import parseString

from Products.CPSDocument.exportimport import CPSDocumentXMLAdapter
from Products.CPSDocument.exportimport import StrictTextElement


class FakeLogger(object):
    def debug(self, text):
        pass

class FakeEnviron(object):
    def getLogger(self, id):
        return FakeLogger()


class TestStrictTextElement(unittest.TestCase):

    def setUp(self):
        context = None
        environ = FakeEnviron()
        self.adapter = CPSDocumentXMLAdapter(context, environ)
        self.doc = self.adapter._doc

    def test_that_thing(self):
        doc = self.doc
        node = self.adapter.createStrictTextElement('foo')
        doc.appendChild(node)
        source = (
            'a b    c\n'     # space in middle
            '    d e    \n'  # spaces at sides
            'f\n'            # no spaces
            '\n'             # empty line
            '<bah>&"&amp;\n' # special chars
            'caf\xe9\n'      # non-ascii data
            +'x '*80         # big line shouldn't wrap
            +'\n'
            )
        source = source.decode('iso-8859-15').encode('utf-8')
        textnode = doc.createTextNode(source)
        node.appendChild(textnode)
        expected = ('<?xml version="1.0"?>\n'
                    '<foo\n'
                    '  >'+cgi.escape(source)+'</foo>\n')
        result = self.doc.toprettyxml(' ')
        if expected != result:
            print "\nDifferences in output:"
            print ''.join(ndiff(expected.splitlines(1),
                                result.splitlines(1)))
        self.assertEquals(expected, result)

        # Now reparse this
        root = parseString(result).documentElement
        node = root.childNodes[0]
        self.assertEquals(node.nodeName, '#text')
        text = node.nodeValue.encode('utf-8')
        self.assertEquals(source, text)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestStrictTextElement),
        ))

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
