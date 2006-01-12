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
"""CPSDocument XML Adapter.
"""

import cgi
from TAL.TALDefs import attrEscape
from xml.dom.minidom import Node

from zope.app import zapi
from zope.component import adapts
from zope.interface import implements

from Acquisition import aq_base
import Products
import OFS.Image
from ZODB.loglevels import BLATHER as VERBOSE
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import BodyAdapterBase
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import ObjectManagerHelpers
from Products.GenericSetup.utils import _LineWrapper
from Products.GenericSetup.utils import _Element
from Products.GenericSetup.interfaces import INode
from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.CPSDocument.CPSDocument import CPSDocumentMixin

from OFS.interfaces import IOrderedContainer
from Products.CPSDocument.interfaces import ICPSDocument
from Products.CPSDocument.interfaces import IOFSFile
from Products.CPSSchemas.interfaces import IFileField
from Products.CPSSchemas.interfaces import IFieldNodeIO


NAME = 'cpsdocument'


class CPSObjectManagerHelpers(object):
    """ObjectManager importer and export helpers for CPS subobjects.

    Knows how to deal with embedded File or Image fields of CPSDocuments
    or as subobjects.

    Knows how to create File or Images, or CPSDocuments according to
    their portal_type.
    """

    def _extractObjects(self):
        fragment = self._doc.createDocumentFragment()
        for obj in getCPSObjectValues(self.context):
            exporter = zapi.queryMultiAdapter((obj, self.environ), INode)
            if exporter:
                fragment.appendChild(exporter.node)
        return fragment

    def _purgeObjects(self):
        parent = self.context
        for id in list(parent.objectIds()):
            parent._delObject(id)

    def _initObjects(self, node):
        """Initialize subobjects from node children.
        """
        for child in node.childNodes:
            if child.nodeName != 'object':
                continue
            if child.hasAttribute('deprecated'):
                continue
            parent = self.context

            obj_id = str(child.getAttribute('name'))
            if obj_id not in parent.objectIds():
                self._addInstance(parent, obj_id, child)

            if child.hasAttribute('insert-before'):
                insert_before = child.getAttribute('insert-before')
                if insert_before == '*':
                    parent.moveObjectsToTop(obj_id)
                else:
                    try:
                        position = parent.getObjectPosition(insert_before)
                        parent.moveObjectToPosition(obj_id, position)
                    except ValueError:
                        pass
            elif child.hasAttribute('insert-after'):
                insert_after = child.getAttribute('insert-after')
                if insert_after == '*':
                    parent.moveObjectsToBottom(obj_id)
                else:
                    try:
                        position = parent.getObjectPosition(insert_after)
                        parent.moveObjectToPosition(obj_id, position+1)
                    except ValueError:
                        pass

            obj = getattr(parent, obj_id)
            importer = zapi.queryMultiAdapter((obj, self.environ), INode)
            if importer:
                importer.node = child

    def _addInstance(self, parent, id, node):
        if node.hasAttribute('portal_type'):
            portal_type = str(node.getAttribute('portal_type'))
            parent.invokeFactory(portal_type, id)
        else:
            ob = self._createInstance(id, node)
            parent._setObject(id, ob)

    def _createInstance(self, id, node):
        meta_type = str(node.getAttribute('meta_type'))
        __traceback_info__ = id, meta_type
        if meta_type == 'File':
            return OFS.Image.File(id, '', '')
        if meta_type == 'Image':
            return OFS.Image.Image(id, '', '')
        for mt in Products.meta_types:
            if mt['name'] == meta_type:
                return mt['instance'](id)
        raise ValueError("unknown meta_type '%s'" % meta_type)





class CPSDocumentXMLAdapter(XMLAdapterBase, CPSObjectManagerHelpers):
    """XML importer and exporter for CPS Document.
    """

    adapts(ICPSDocument, ISetupEnviron)
    implements(IBody)

    _LOGGER_ID = NAME

    def _getObjectNode(self, name, i18n=True):
        node = XMLAdapterBase._getObjectNode(self, name, i18n)
        node.setAttribute('portal_type', self.context.getPortalTypeName())
        return node

    def _exportNode(self):
        """Export the object as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractObjects())
        node.appendChild(self._extractDocumentFields())
        msg = "Document %r exported." % self.context.getId()
        self._logger.log(VERBOSE, msg)
        return node

    def _importNode(self, node):
        """Import the object from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeObjects()
            self._purgeDocumentFields()
        # Init fields before objects, as some None files may be objects
        # and need to be imported after their ini
        self._initDocumentFields(node)
        self._initObjects(node)
        msg = "Document %r imported." % self.context.getId()
        self._logger.log(VERBOSE, msg)

    def _extractDocumentFields(self):
        ob = self.context
        fragment = self._doc.createDocumentFragment()
        datamodel = ob.getDataModel()
        for key, value, field in datamodel._itemsWithFields():
            node = self.createStrictTextElement('f')
            node.setAttribute('id', key)
            nodeio = IFieldNodeIO(field)
            nodeio.setNodeValue(node, value, self)
            fragment.appendChild(node)
        return fragment

    def _purgeDocumentFields(self):
        pass

    def _initDocumentFields(self, node):
        ob = self.context
        ti = ob.getTypeInfo()
        datamodel = ob.getDataModel()
        datamodel._check_acls = False # XXX use API
        for child in node.childNodes:
            if child.nodeName != 'f':
                continue
            key = str(child.getAttribute('id'))
            field = datamodel._fields[key]
            nodeio = IFieldNodeIO(field)
            value = nodeio.getNodeValue(child, self)
            datamodel[key] = value
        ti._commitDM(datamodel)

    # Utility methods called from IFieldNodeIO methods.

    def setNodeValue(self, node, text):
        """Set node value.

        Passed text must be unicode.
        """
        if '\n' in text or '"' in text:
            # set as child text node
            self.setNodeText(node, text)
        else:
            # set as 'v' attribute
            text = text.encode('utf-8')
            node.setAttribute('v', text)

    def getNodeValue(self, node):
        """Get node value.

        Returns unicode.
        """
        if node.hasAttribute('v'):
            return node.getAttribute('v')
        else:
            return self.getNodeText(node)

    def setNodeText(self, node, text):
        """Set node text as child text element.

        Passed text must be unicode.
        """
        text = text.encode('utf-8')
        textnode = self._doc.createTextNode(text)
        node.appendChild(textnode)

    def getNodeText(self, node):
        """Get exact node text.

        Returns unicode.
        """
        texts = []
        for child in node.childNodes:
            if child.nodeName != '#text':
                continue
            texts.append(child.nodeValue)
        text = ''.join(texts)
        return text

    def createStrictTextElement(self, tagName):
        e = StrictTextElement(tagName)
        e.ownerDocument = self._doc
        return e


class StrictTextElement(_Element):
    """GenericSetup _Element but with stricter text node output.

    Text nodes are exported exactly as is, without added whitespace.
    """

    def writexml(self, writer, indent="", addindent="", newl=""):
        # indent = current indentation
        # addindent = indentation to add to higher levels
        # newl = newline string
        wrapper = _LineWrapper(writer, indent, addindent, newl, 78)
        wrapper.write('<%s' % self.tagName)

        # move 'name', 'meta_type' and 'title' to the top, sort the rest
        attrs = self._get_attributes()
        a_names = attrs.keys()
        a_names.sort()
        for special in ('title', 'meta_type', 'name'):
            if special in a_names:
                a_names.remove(special)
                a_names.insert(0, special)

        for a_name in a_names:
            wrapper.write()
            a_value = attrEscape(attrs[a_name].value)
            wrapper.queue(' %s="%s"' % (a_name, a_value))

        if self.childNodes:
            wrapper.queue('>')
            for node in self.childNodes:
                if node.nodeType == Node.TEXT_NODE:
                    data = cgi.escape(node.data)
                    # Here, simplified output, just queue the data
                    wrapper.queue(data)
                else:
                    wrapper.write('', True)
                    node.writexml(writer, indent+addindent, addindent, newl)
            wrapper.write('</%s>' % self.tagName, True)
        else:
            wrapper.write('/>', True)


class OFSFileBodyAdapter(BodyAdapterBase):
    """Body exporter/importer for OFS files and images.

    Dumps CMF Image and File documents as their simpler OFS version.
    """

    adapts(IOFSFile, ISetupEnviron)
    implements(IBody)

    _LOGGER_ID = 'file'

    def __init__(self, context, environ):
        BodyAdapterBase.__init__(self, context, environ)
        # Used during export
        self.mime_type = self.context.getContentType()

    def _getObjectNode(self, name, i18n=True):
        ob = self.context
        node = self._doc.createElement(name)
        node.setAttribute('name', ob.getId()) # XXX needs unique id, parent's
        meta_type = ob.meta_type
        # If they don't have specific adapters, change their type
        if meta_type == 'Portal Image':
            meta_type = 'Image'
        elif meta_type == 'Portal File':
            meta_type = 'File'
        node.setAttribute('meta_type', meta_type)
        return node

    def _exportBody(self):
        """Export the object as a file body.
        """
        ob = self.context
        msg = "%s %r exported." % (ob.meta_type, ob.getId())
        self._logger.log(VERBOSE, msg)
        return str(ob.data)

    def _importBody(self, body):
        """Import the object from the file body.
        """
        ob = self.context
        ob.manage_upload(body)
        msg = "%s %r imported." % (ob.meta_type, ob.getId())
        self._logger.log(VERBOSE, msg)

    body = property(_exportBody, _importBody)





def getCPSObjectValues(parent):
    items = list(parent.objectItems())
    addCPSFieldObjectItems(parent, items)
    if not IOrderedContainer.providedBy(parent):
        items.sort()
    return [i[1] for i in items]

def addCPSFieldObjectItems(parent, items):
    """IFileField are also exportable as subobjects.
    """
    if not isinstance(parent, CPSDocumentMixin):
        return
    datamodel = parent.getDataModel()
    bases = [aq_base(i[1]) for i in items]
    field_items = []
    for key, value, field in datamodel._itemsWithFields():
        if IFileField.providedBy(field):
            if value is not None and aq_base(value) not in bases:
                field_items.append((key, value))
    field_items.sort()
    items.extend(field_items)


def exportCPSObjects(obj, parent_path, context):
    """ Export subobjects recursively.

    Recursion also happens for specific CPS subobjects.
    """
    exporter = zapi.queryMultiAdapter((obj, context), IBody)
    path = '%s%s' % (parent_path, obj.getId().replace(' ', '_'))
    if exporter:
        if exporter.name:
            path = '%s%s' % (parent_path, exporter.name)
        filename = '%s%s' % (path, exporter.suffix)
        body = exporter.body
        if body is not None:
            context.writeDataFile(filename, body, exporter.mime_type)

    if getattr(aq_base(obj), 'objectValues', None) is not None:
        for sub in getCPSObjectValues(obj):
            exportCPSObjects(sub, path+'/', context)

def importCPSObjects(obj, parent_path, context):
    """ Import subobjects recursively.
    """
    importer = zapi.queryMultiAdapter((obj, context), IBody)
    path = '%s%s' % (parent_path, obj.getId().replace(' ', '_'))
    __traceback_info__ = path
    if importer:
        if importer.name:
            path = '%s%s' % (parent_path, importer.name)
        filename = '%s%s' % (path, importer.suffix)
        body = context.readDataFile(filename)
        if body is not None:
            importer.filename = filename # for error reporting
            importer.body = body

    if getattr(aq_base(obj), 'objectValues', None) is not None:
        for sub in getCPSObjectValues(obj):
            importCPSObjects(sub, path+'/', context)