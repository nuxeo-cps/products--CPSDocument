# -*- coding: ISO-8859-15 -*-
# (C) Copyright 2006 Nuxeo SAS <http://nuxeo.com>
# Authors:
# Tarek Ziadé <tz@nuxeo.com>
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
import unittest

from Products.CPSDocument.utils import cleanAjaxParams

class TestUtils(unittest.TestCase):

    def test_cleanAjaxParams(self):

        class FakeRequest(object):
            form = {'yo': ['one,two,three']}

        req = FakeRequest()
        cleanAjaxParams(req)
        self.assertEquals(req.form['yo'], ['one', 'two', 'three'])

def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(TestUtils)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
