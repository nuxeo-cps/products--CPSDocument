# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
# Authors: Lennart Regebro <lr@nuxeo.com>
#          Florent Guillaume <fg@nuxeo.com>
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

from zLOG import LOG, DEBUG, ERROR
from types import ListType, TupleType
from cgi import escape
import ExtensionClass
from Globals import InitializeClass
from AccessControl import Unauthorized
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.PortalFolder import PortalFolder

SUMMARY_MAX_LEN = 418  # XXX: better get rid of magical constants

class CPSDocumentMixin(ExtensionClass.Base):
    """Mixin giving CPS Document behaviour.

    This means that the definition for the document's fields and layout
    and widgets is indirected through its definition in the Types Tool,
    and from there to the Schemas Tool.
    """

    security = ClassSecurityInfo()
    _size = 0

    security.declareProtected(View, 'render')
    def render(self, **kw):
        """Render the object according to a layout mode.

        Arguments are layout_mode, layout_id, proxy.
        """
        return self.getTypeInfo().renderObject(self, **kw)

    # This is not protected using ModifyPortalContent because the object
    # may be frozen, and will only be unfrozen just before committing.
    # The security check on ModifyPortalContent is now done by DataModel
    # just before commit.
    security.declareProtected(View, 'renderEditDetailed')
    def renderEditDetailed(self, **kw):
        """Modify the object from the request (if present), and return
        the HTML rendering and some detailed information.

        Arguments are request, layout_mode, layout_mode_er, layout_id,
        proxy.

        Renders in layout_mode, or layout_mode_err if a validation error
        occurred.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and the backend.
        """
        return self.getTypeInfo().renderEditObjectDetailed(self, **kw)

    # See remark about security above.
    security.declareProtected(View, 'renderEdit')
    def renderEdit(self, **kw):
        """Modify the object from the request (if present), and return
        the HTML rendering.

        See renderEditDetailed for more.
        """
        return self.getTypeInfo().renderEditObject(self, **kw)

    # See remark about security above.
    security.declareProtected(View, 'validateStoreRender')
    def validateStoreRender(self, **kw):
        """Modify the object from request, store data, and renders to new mode.

        Arguments are request, layout_mode, layout_mode_ok,
        layout_mode_err, layout_id, proxy.

        If no request was passed, renders layout_mode.

        If request was passed, renders layout_mode_ok, or
        layout_mode_err if validation failed.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and the backend.
        """
        return self.getTypeInfo().validateStoreRenderObject(self, *kw)

    # XXX make this a WorkflowMethod
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, mapping={}, proxy=None, REQUEST=None, **kw):
        """Edit the document.

        The mapping and the keyword arguments describe fields, not
        widgets.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and the backend.

        This method assumes that self really is editable, thus is not a
        frozen document.
        """
        if REQUEST is not None:
            raise Unauthorized("Not accessible TTW.")
        mapping.update(kw)
        return self.getTypeInfo().editObject(self, mapping, proxy=proxy)


    security.declareProtected(View, 'SearchableText')
    def SearchableText(self):
        """Searchable text for CMF full-text indexing.

        Indexes all fields marked as indexable.
        """
        strings = []
        dm = self.getTypeInfo().getDataModel(self)
        # XXX uses internal knowledge of DataModel
        for fieldid, field in dm._fields.items():
            if not field.is_indexed:
                continue
            value = dm[fieldid]
            if (not isinstance(value, ListType) and
                not isinstance(value, TupleType)):
                value = (value,)
            for v in value:
                strings.append(str(v)) # XXX Use ustr ?
        # XXX Deal with Unicode properly...
        return ' '.join(strings)

    security.declareProtected(ModifyPortalContent, 'flexibleAddWidget')
    def flexibleAddWidget(self, layout_id, wtid, **kw):
        """Add a new widget to the flexible part of the document.

        Returns the widget id.
        """
        ti = self.getTypeInfo()
        return ti.flexibleAddWidget(self, layout_id, wtid, **kw)

    security.declareProtected(ModifyPortalContent, 'flexibleDelWidgets')
    def flexibleDelWidgets(self, layout_id, widget_ids):
        """Delete widgets from the flexible part of the document.
        """
        ti = self.getTypeInfo()
        return ti.flexibleDelWidgets(self, layout_id, widget_ids)

    security.declareProtected(ModifyPortalContent, 'flexibleDelWidgetRows')
    def flexibleDelWidgetRows(self, layout_id, rows):
        """Delete widget rows from the flexible part of the document.
        """
        ti = self.getTypeInfo()
        ti._makeObjectFlexible(self)
        layout, schema = ti._getFlexibleLayoutAndSchemaFor(self, layout_id)
        layoutdef = layout.getLayoutDefinition()
        widget_ids = {}
        i = -1
        for row in layoutdef['rows']:
            i += 1
            if i not in rows:
                continue
            for cell in row:
                widget_ids[cell['widget_id']] = None
        widget_ids = widget_ids.keys()
        return ti.flexibleDelWidgets(self, layout_id, widget_ids)

    security.declareProtected(ModifyPortalContent, 'flexibleChangeLayout')
    def flexibleChangeLayout(self, layout_id, **kw):
        """Change the layout.

        Can move a row up or down.
        """
        ti = self.getTypeInfo()
        return ti.flexibleChangeLayout(self, layout_id, **kw)


    #
    # CPSDefault integration
    #
    security.declarePrivate('postCommitHook')
    def postCommitHook(self):
        # this is called just after the dm commit
        self._size = self._compute_size()


    security.declareProtected(View, 'getAdditionalContentInfo')
    def getAdditionalContentInfo(self):
        """ Return a dictonary used in getContentInfo """
        infos = {}
        summary_fields = ['body', 'content']
        summary = ''
        for f in summary_fields:
            if hasattr(aq_base(self), f):
                summary += getattr(self, f)
                if len(summary) > max_len:
                    summary = summary[:SUMMARY_MAX_LEN] + '...'
                    break
        if summary:
            infos['summary'] = summary

        if hasattr(aq_base(self), 'preview') and self.preview:
            infos['preview'] = self.absolute_url(1) + '/preview'
        return infos


    security.declareProtected(View, 'get_size')
    def get_size(self):
        """Return the size of the data."""
        # XXX: what is exactly the 'size'?
        if self._size:
            return self._size
        return self._compute_size()


    security.declarePrivate('_compute_size')
    def _compute_size(self):
        # XXX: this needs some explanations
        # For instance, what is the 'size' of an empty object ?
        size = 0
        dm = self.getTypeInfo().getDataModel(self)
        # XXX uses internal knowledge of DataModel
        for fieldid, field in dm._fields.items():
            try:
                if hasattr(aq_base(dm[fieldid]), 'get_size'):
                    size += dm[fieldid].get_size()
                else:
                    size += len(str(dm[fieldid]))
            except KeyError:
                pass

        for item in self.propdict().keys():
            size += len(str(getattr(self, item, '')))

        return size

    security.declareProtected(View, 'exportAsXML')
    def exportAsXML(self, proxy=None):
        """Export as XML."""
        utool = getToolByName(self, 'portal_url')
        if proxy is None:
            proxy = self
        rpath = utool.getRelativeUrl(proxy)
        dm = self.getTypeInfo().getDataModel(self)
        xml = dm._exportAsXML()
        return ('<document type="%s" rpath="%s">\n%s\n</document>'
                % (escape(self.getPortalTypeName()),
                   escape(rpath),
                   xml))

InitializeClass(CPSDocumentMixin)


# XXX remove later
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl

class CPSDocument(CPSDocumentMixin, PortalContent, PortalFolder,
                  DefaultDublinCoreImpl):
    """CPS Document

    Basic document type from which real types are derived according to
    the schemas and layouts specified in the Types Tool.
    """

    meta_type = "CPS Document"
    portal_type = "CPS Document" # To ease testing.

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        self.id = id
        DefaultDublinCoreImpl.__init__(self)


InitializeClass(CPSDocument)


def addCPSDocument(container, id, REQUEST=None, **kw):
    """Add a bare CPS Document.

    The object doesn't have a portal_type yet, so we have no way to know
    its schema. This simply constructs a bare instance.
    """
    ob = CPSDocument(id, **kw)
    container._setObject(id, ob)
    ob = container._getOb(id)
    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(ob.absolute_url()+'/manage_main')
    return ob
