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
from types import ListType, TupleType, UnicodeType
from cgi import escape
import ExtensionClass
import re
from Globals import InitializeClass
from AccessControl import Unauthorized
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.PortalFolder import PortalFolder
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware

from Products.CMFCore.interfaces.DublinCore import DublinCore as IDublinCore
from Products.CMFCore.interfaces.Contentish import Contentish as IContentish
from Products.CMFCore.interfaces.Dynamic import DynamicType as IDynamicType

SUMMARY_MAX_LEN = 418  # XXX: better get rid of magical constants

class CPSDocumentMixin(ExtensionClass.Base):
    """Mixin giving CPS Document behaviour.

    This means that the definition for the document's fields and layout
    and widgets is indirected through its definition in the Types Tool,
    and from there to the Schemas Tool.
    """

    security = ClassSecurityInfo()
    _size = 0

    _has_generic_edit_method = 1 # Used by WebDAV in ProxyBase

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

    security.declareProtected(View, 'getDataModel')
    def getDataModel(self, proxy=None, REQUEST=None, **kw):
        """Return the data model.

        Modifying the returned data model has no effect on the structure of the
        document. For modifications to have any effects the data model has to be
        committed.
        """
        if REQUEST:
            raise Unauthorized("Not accessible TTW.")
        dm = self.getTypeInfo().getDataModel(self, proxy=proxy)
        return dm

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
        if REQUEST:
            raise Unauthorized("Not accessible TTW.")
        kw.update(mapping)
        return self.getTypeInfo().editObject(self, kw, proxy=proxy)


    security.declareProtected(View, 'SearchableText')
    def SearchableText(self):
        """Searchable text for CMF full-text indexing.

        Indexes all fields marked as indexable.
        """
        ti = self.getTypeInfo()

        # CMF object not fully created
        if ti is None:
            return ''

        dm = ti.getDataModel(self)
        strings = []
        # XXX uses internal knowledge of DataModel
        for fieldid, field in dm._fields.items():
            if not field.is_searchabletext:
                continue
            value = dm[fieldid]
            if (not isinstance(value, ListType) and
                not isinstance(value, TupleType)):
                value = (value,)
            for v in value:
                strings.append(str(v)) # XXX Use ustr ?
        # XXX Deal with fields that use a vocabulary, and add the
        #     translated value to the searchable text, not the key.
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
    def postCommitHook(self, datamodel=None):
        # this is called just after the dm commit
        self._size = self._compute_size(datamodel=datamodel)


    security.declareProtected(View, 'getAdditionalContentInfo')
    def getAdditionalContentInfo(self, proxy):
        """Return a dictionary used in getContentInfo."""
        infos = {}
        doc = aq_base(self)

        summary_fields = ('body', 'content', 'content_right')
        tag_pattern = re.compile(r'<[^>]*>')
        summary = ''
        for f in summary_fields:
            if hasattr(doc, f):
                try:
                    summary += tag_pattern.sub('', getattr(self, f))
                    # filtering &nbsp; characters
                    summary = summary.replace('&nbsp;', ' ')
                except TypeError:
                    pass
                if len(summary) > SUMMARY_MAX_LEN:
                    summary = summary[:SUMMARY_MAX_LEN] + '...'
                    break
        if summary:
            infos['summary'] = summary

        if hasattr(doc, 'preview') and self.preview:
            infos['preview'] =  proxy.absolute_url(1) + '/preview'

        photo_fields = ('photo', 'image', 'photo_1', 'preview')
        for f in photo_fields:
            if hasattr(doc, f) and getattr(doc, f, None):
                infos['photo'] = proxy.absolute_url(1) + '/'+ f
                break

        return infos


    security.declareProtected(View, 'get_size')
    def get_size(self):
        """Return the size of the data.

        This is informative only, for display purposes. It's used
        by the ZMI for instance, and also by CPS folder listing.

        NB: get_size() is part of the Zope and CMF API.
        """
        if self._size:
            return self._size
        return self._compute_size()

    security.declarePrivate('_compute_size')
    def _compute_size(self, datamodel=None):
        """Compute the _size attribute.

        The _size attribute is used by get_size, to return an
        informative size about the object (including hidden fields like
        file_html and file_txt).
        """
        # XXX this is not user-focused since the "size" for the user will
        # usually mean "how big will it be (and how long will it take) if
        # I download the file.
        size = 0
        if datamodel is None:
            dm = self.getTypeInfo().getDataModel(self)
        else:
            dm = datamodel
        # XXX uses internal knowledge of DataModel
        for field_id in dm._fields.keys():
            try:
                if hasattr(aq_base(dm[field_id]), 'get_size'):
                    field_size = dm[field_id].get_size()
                elif isinstance(dm[field_id], UnicodeType):
                    field_size = len(dm[field_id])
                else:
                    field_size = len(str(dm[field_id]))
                size += field_size
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

##     # XXX FG: we want to use this with any document type so we should
##     # probably patch Item instead. And ProxyBase must be changed too.
##     security.declareProtected(View, 'downloadFile')
##     def downloadFile(self, field_name, RESPONSE=None):
##         """Download File contained in attribute <field_name>"""
##         # XXX: add some checking here
##         file = getattr(self, field_name)
##         if file is None:
##             data = ''
##         else:
##             # XXX: it would be much more efficient not to retrieve
##             # whole file in memory (for big files)
##             data = str(file)
##         if RESPONSE:
##             content_type = getattr(file, 'content_type',
##                 'application/octet-stream')
##             filename = getattr(file, '__name__', 'file')
##             # XXX: Need some escaping here.
##             RESPONSE.setHeader('Content-Type', content_type)
##             RESPONSE.setHeader('Content-Disposition',
##                                "inline; filename=%s" % filename)
##             RESPONSE.setHeader('Content-Length', len(data))
##             RESPONSE.write(data)
##         else:
##             return data


InitializeClass(CPSDocumentMixin)


# XXX remove later
# XXX: please explain why
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl

class CPSDocument(CPSDocumentMixin, CMFCatalogAware, PortalFolder,
                  PortalContent, DefaultDublinCoreImpl):
    """CPS Document

    Basic document type from which real types are derived according to
    the schemas and layouts specified in the Types Tool.
    """

    meta_type = 'CPS Document'
    portal_type = 'CPS Document' # To ease testing.

    __implements__ = (IDublinCore, IContentish, IDynamicType)

    manage_options = (
        PortalContent.manage_options[:1] + # Dublin Core
        PortalFolder.manage_options[0:1] + # Contents
        PortalContent.manage_options[1:]   # View, Workflows...
        )

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
    if REQUEST:
        ob = container._getOb(id)
        REQUEST.RESPONSE.redirect(ob.absolute_url()+'/manage_main')
