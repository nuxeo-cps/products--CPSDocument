# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
# Authors: Lennart Regebro <regebro@nuxeo.com>
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
# $Id$
"""Layout

A layout describes how to render the basic fields of a schema.
"""

from zLOG import LOG, DEBUG
from copy import deepcopy
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo

from OFS.Folder import Folder

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.CMFCorePermissions import ManagePortal
from Products.CMFCore.CMFCorePermissions import ViewManagementScreens
from Products.CMFCore.utils import SimpleItemWithProperties

from Products.CPSDocument.OrderedDictionary import OrderedDictionary
from Products.CPSDocument.Renderer import BasicRenderer, HtmlRenderer

from Products.CPSDocument.Widget import WidgetRegistry

class BasicLayout(OrderedDictionary):
    """Defines a document layout

    """

    _renderer = BasicRenderer

    def __init__(self, id, title):
        OrderedDictionary.__init__(self)
        self.id = id
        self.title = title

    def render(self, model, data):
        """Renders the defined layout with data"""
        renderer = self._renderer
        rendering = ""

        for fieldid, widget in self.items():

            # TODO:
            # Fields that aren't reqired may have no data in the document, and
            # they will then have no data in the DataStructure.
            # The question is then, what to do with these fields?
            # Currently they are rendered with None, which may not be
            # the correct behaviour. Skip them completely?
            content = data.data.get(fieldid)
            error = data.errors.get(fieldid) # Both '' or None are acceptable as meaning no error
            field = model.getField(fieldid)
            rendering = rendering + widget.render(renderer, field, content, error)

        return rendering


class HtmlLayout(BasicLayout):
    """A layout for HTML

    TODO: Ponder about how styles gets into this.
    """
    _renderer = HtmlRenderer


######################################################################
######################################################################
######################################################################


class Layout(Folder, SimpleItemWithProperties):
    """Basic Layout.

    A layout describes how to render the basic fields of a schema.
    """

    security = ClassSecurityInfo()

    id = None

    def __init__(self, **kw):
        #layoutdef = {'ncols': 1, 'rows': []}
        layoutdef = {
            'ncols': 3,
            'rows': [[{'ncols': 1,
                       'widget_id': 'foo',
                       },
                      {'ncols': 2,
                       'widget_id': 'bar',
                       },
                      ],
                     [{'ncols': 3,
                       'widget_id': 'baz',
                       },
                      ],
                     ],
            }
        self.setLayoutDefinition(layoutdef)


    def _normalizeLayoutDefinition(self, layoutdef):
        """Normalize a layout definition."""
        rows = layoutdef['rows']
        # Find max width.
        maxw = 1
        for row in rows:
            w = 0
            for cell in row:
                w += cell.get('ncols', 1)
            if w > maxw:
                maxw = w
        # Normalize short widths.
        for row in rows:
            w = 0
            for cell in row:
                if cell is row[-1]:
                    cell['ncols'] = maxw - w
                else:
                    w += cell.get('ncols', 1)
        layoutdef['ncols'] = maxw
        layoutdef['rows'] = filter(None, rows)
        return layoutdef

    security.declarePrivate('setLayoutDefinition')
    def setLayoutDefinition(self, layoutdef):
        """Set the layout definition."""
        layoutdef = self._normalizeLayoutDefinition(layoutdef)
        self._layoutdef = layoutdef

    security.declareProtected(View, 'getLayoutDefinition')
    def getLayoutDefinition(self):
        """Get the layout definition."""
        return deepcopy(self._layoutdef)

    security.declarePrivate('getLayoutData')
    def getLayoutData(self, datastructure, datamodel):
        """Get the layout data.

        This has actuel widget instances.
        """
        layoutdata = self.getLayoutDefinition() # get a copy
        for row in layoutdata['rows']:
            for cell in row:
                widget_id = cell['widget_id']
                widget = self.getWidget(widget_id)
                cell['widget'] = widget
                # XXX here filtering according to permissions ?
                widget.prepare(datastructure, datamodel)
        return layoutdata

    security.declarePrivate('validateLayout')
    def validateLayout(self, layoutdata, datastructure, datamodel):
        """Validate the layout."""
        ok = 1
        for row in layoutdata['rows']:
            for cell in row:
                widget = cell['widget']
                ok = ok and widget.validate(datastructure, datamodel)
        return ok

    def __repr__(self):
        return '<Layout %s>' % `self.getLayoutDefinition()`


InitializeClass(Layout)


class CPSLayout(Layout):
    """Persistent Layout."""

    meta_type = "CPS Layout"

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        self.id = id
        Layout.__init__(self, **kw)

    security.declarePrivate('addWidget')
    def addWidget(self, id, widget):
        """Add a widget."""
        self._setObject(id, widget)
        return self._getOb(id)

    security.declarePrivate('getWidget')
    def getWidget(self, id):
        """Get a widget."""
        try:
            return self._getOb(id)
        except AttributeError:
            return ValueError("No widget '%s' in layout '%s'" %
                              (id, self.id))

    security.declareProtected(ViewManagementScreens, 'listWidgets')
    def listWidgets(self):
        """Get the list of widget ids."""
        ids = self.objectIds()
        ids.sort()
        return ids

    #
    # ZMI
    #

    manage_options = (
        {'label': 'Widgets',
         'action': 'manage_main',
         },
        {'label': 'Layout',
         'action': 'manage_editLayout',
         },
        ) + SimpleItemWithProperties.manage_options

    security.declareProtected(ManagePortal, 'manage_editLayout')
    manage_editLayout = DTMLFile('zmi/layout_editform', globals())

    def all_meta_types(self):
        return [
            {'name': widget_type,
             'action': 'manage_addCPSWidgetForm/'+widget_type.replace(' ', ''),
             'permission': ManagePortal}
            for widget_type in WidgetRegistry.listWidgetTypes()]

    security.declareProtected(ManagePortal, 'manage_addCPSWidgetForm')
    manage_addCPSWidgetForm = DTMLFile('zmi/widget_addform', globals())

    security.declareProtected(ManagePortal, 'get_unstripped_widget_type')
    def get_unstripped_widget_type(self, widget_type):
        """Get an unstripped version of a widget type."""
        wts = widget_type.replace(' ', '')
        for wt in WidgetRegistry.listWidgetTypes():
            if wt.replace(' ', '') == wts:
                return wt
        raise ValueError, widget_type

    security.declareProtected(ManagePortal, 'manage_addCPSWidget')
    def manage_addCPSWidget(self, id, widget_type_stripped, REQUEST=None):
        """Add a widget, called from the ZMI."""
        widget_type = self.get_unstripped_widget_type(widget_type_stripped)
        widget = WidgetRegistry.makeWidget(widget_type, id)
        widget = self.addWidget(id, widget)
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(widget.absolute_url()+
                                      '/manage_workspace')

    security.declareProtected(ManagePortal, 'manage_changeLayout')
    def manage_changeLayout(self, addrow=0,
                            delcell=0, widencell=0, shrinkcell=0, splitcell=0,
                            REQUEST=None, **kw):
        """Change a layout."""
        if REQUEST is not None:
            kw.update(REQUEST.form)
        layoutdef = self.getLayoutDefinition()
        nrow = 0
        rows = layoutdef['rows']
        for row in rows:
            nrow += 1
            ncell = 0
            somedel, somesplit = 0, 0
            for cell in row:
                ncell += 1
                cell['widget_id'] = kw.get('cell_%d_%d' % (nrow, ncell), '')
                if kw.get('check_%d_%d' % (nrow, ncell)):
                    if delcell:
                        cell['del'] = 1
                        somedel = 1
                    if splitcell:
                        cell['split'] = 1
                        somesplit = 1
                    if widencell:
                        cell['ncols'] = cell['ncols']+1
                    if shrinkcell:
                        cell['ncols'] = max(1, cell['ncols']-1)
            if somedel:
                newrow = [cell for cell in row if not cell.get('del')]
                rows[nrow-1] = newrow
            if somesplit:
                newrow = []
                for cell in row:
                    newrow.append(cell)
                    if cell.get('split'):
                        cell['ncols'] = max(1, cell['ncols']-1)
                        del cell['split']
                        newrow.append(
                            {'ncols': 1, 'widget_id': ''}
                            )
                rows[nrow-1] = newrow
        if addrow:
            rows.append(
                [{'ncols': 1, 'widget_id': ''}]
                )
        layoutdef['rows'] = rows
        self.setLayoutDefinition(layoutdef)
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url()+'/manage_editLayout'
                                      '?manage_tabs_message=Changed.')

    security.declareProtected(ManagePortal, 'manage_addLayoutRow')
    def manage_addLayoutRow(self, REQUEST=None, **kw):
        """Add a row to a layout."""
        return self.manage_changeLayout(addrow=1, REQUEST=REQUEST, **kw)

    security.declareProtected(ManagePortal, 'manage_deleteCell')
    def manage_deleteCell(self, REQUEST=None, **kw):
        """Delete a cell from a layout."""
        return self.manage_changeLayout(delcell=1, REQUEST=REQUEST, **kw)

    security.declareProtected(ManagePortal, 'manage_widenCell')
    def manage_widenCell(self, REQUEST=None, **kw):
        """Widen a cell from a layout."""
        return self.manage_changeLayout(widencell=1, REQUEST=REQUEST, **kw)

    security.declareProtected(ManagePortal, 'manage_shrinkCell')
    def manage_shrinkCell(self, REQUEST=None, **kw):
        """Shrink a cell from a layout."""
        return self.manage_changeLayout(shrinkcell=1, REQUEST=REQUEST, **kw)

    security.declareProtected(ManagePortal, 'manage_splitCell')
    def manage_splitCell(self, REQUEST=None, **kw):
        """Split a cell in two."""
        return self.manage_changeLayout(splitcell=1, REQUEST=REQUEST, **kw)

InitializeClass(CPSLayout)

