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
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.PortalFolder import PortalFolder


class CPSDocumentMixin(ExtensionClass.Base):
    """Mixin giving CPS Document behaviour.

    This means that the definition for the document's fields and layout
    and widgets is indirected through its definition in the Types Tool,
    and from there to the Schemas Tool.
    """

    security = ClassSecurityInfo()
    _size = 0

    security.declareProtected(View, 'render')
    def render(self, mode='view', layout_id=None, **kw):
        """Render the object according to a mode."""
        ti = self.getTypeInfo()
        return ti.renderObject(self, mode=mode, layout_id=layout_id, **kw)

    # This is not protected using ModifyPortalContent because the object
    # may be frozen, and will only be unfrozen just before committing.
    # The security check on ModifyPortalContent is now done by DataModel
    # just before commit.
    security.declareProtected(View, 'renderEditDetailed')
    def renderEditDetailed(self, request=None, mode='edit', errmode='edit',
                           layout_id=None, **kw):
        """Modify the object from the request (if present), and return
        the HTML rendering and some detailed information.

        Renders the mode, or the errmode if a validation error occurred.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and the backend.
        """
        ti = self.getTypeInfo()
        return ti.renderEditObjectDetailed(self, request,
                                           mode=mode, errmode=errmode,
                                           layout_id=layout_id, **kw)

    # See remark about security above.
    security.declareProtected(View, 'renderEdit')
    def renderEdit(self, request=None, mode='edit', errmode='edit',
                   layout_id=None, **kw):
        """Modify the object from the request (if present), and return
        the HTML rendering.

        See renderEditDetailed for more.
        """
        ti = self.getTypeInfo()
        return ti.renderEditObject(self, request,
                                   mode=mode, errmode=errmode,
                                   layout_id=layout_id, **kw)

    # See remark about security above.
    security.declareProtected(View, 'validateStoreRender')
    def validateStoreRender(self, request=None,
                            mode='edit', okmode='edit', errmode='edit',
                            layout_id=None, **kw):
        """Modify the object from request, store data, and renders to new mode.

        If no request was passed, renders mode.

        If request was passed, renders okmode, or errmode if validation
        failed.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and the backend.
        """
        ti = self.getTypeInfo()
        return ti.validateStoreRenderObject(self, request, mode=mode,
                                            okmode=okmode, errmode=errmode,
                                            layout_id=layout_id, **kw)

    # XXX make this a WorkflowMethod
    security.declareProtected(ModifyPortalContent, 'edit')
    def edit(self, **kw):
        """Edit the document.

        The keyword arguments describes fields, not widgets.

        This method assumes that self really is editable, thus is not a
        frozen document.
        """
        ti = self.getTypeInfo()
        return ti.editObject(self, kw)


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
        max_len = 418
        summary_fields = ['body', 'content']
        sum = ''
        for f in summary_fields:
            if hasattr(aq_base(self), f):
                sum += getattr(self, f)
                if len(sum) > max_len:
                    sum = sum[:max_len] + '...'
                    break
        if sum:
            infos['summary'] = sum

        if hasattr(aq_base(self), 'preview') and self.preview:
            infos['preview'] = self.absolute_url(1) + '/preview'
        return infos


    security.declareProtected(View, 'get_size')
    def get_size(self):
        """ return the size of the data """
        if self._size:
            return self._size
        return self._compute_size()


    security.declarePrivate('_compute_size')
    def _compute_size(self):
        s = 0
        dm = self.getTypeInfo().getDataModel(self)
        # XXX uses internal knowledge of DataModel
        for fieldid, field in dm._fields.items():
            try:
                if hasattr(aq_base(dm[fieldid]), 'get_size'):
                    s += dm[fieldid].get_size()
                else:
                    s  += len(str(dm[fieldid]))
            except KeyError:
                pass

        for item in self.propdict().keys():
            s += len(str(getattr(self, item, '')))

        return s

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
