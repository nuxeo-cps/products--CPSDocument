# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
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
"""BasicWidgets

Definition of standard widget types.
"""

from zLOG import LOG, DEBUG
from cgi import escape
from types import IntType, StringType, UnicodeType
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo
from OFS.PropertyManager import PropertyManager

from Products.CMFCore.CMFCorePermissions import ManageProperties
from Products.CMFCore.utils import getToolByName

from Products.CPSDocument.Field import ValidationError
from Products.CPSDocument.Widget import CPSWidget
from Products.CPSDocument.Widget import CPSWidgetType
from Products.CPSDocument.WidgetsTool import WidgetTypeRegistry


##################################################

class CPSStringWidget(CPSWidget):
    """String widget."""
    meta_type = "CPS String Widget"

    def prepare(self, datastructure, datamodel):
        """Prepare datastructure from datamodel."""
        datastructure[self.getWidgetId()] = datamodel[self.fields[0]]

    def validate(self, datastructure, datamodel):
        """Update datamodel from user data in datastructure."""
        value = datastructure[self.getWidgetId()]
        try:
            v = str(value)
        except ValueError:
            datastructure.setError(self.getWidgetId(),
                                   "Bad str received")
            ok = 0
        else:
            datamodel[self.fields[0]] = v
            ok = 1
        return ok

    def render(self, mode, datastructure, datamodel):
        """Render this widget from the datastructure or datamodel."""
        value = datastructure[self.getWidgetId()]
        if mode == 'view':
            return escape(value)
        elif mode == 'edit':
            return ('<input type="text" name="%s" value="%s" />'
                    % (escape(self.getHtmlWidgetId()), escape(value)))
        else:
            return '[XXX unknown mode %s]' % mode

InitializeClass(CPSStringWidget)


class CPSStringWidgetType(CPSWidgetType):
    """String widget type."""
    meta_type = "CPS String Widget Type"
    cls = CPSStringWidget

InitializeClass(CPSStringWidgetType)

##################################################

class CPSIntWidget(CPSWidget):
    """Integer widget."""
    meta_type = "CPS Int Widget"

    def prepare(self, datastructure, datamodel):
        """Prepare datastructure from datamodel."""
        datastructure[self.getWidgetId()] = str(datamodel[self.fields[0]])

    def validate(self, datastructure, datamodel):
        """Update datamodel from user data in datastructure."""
        value = datastructure[self.getWidgetId()]
        try:
            v = int(value)
        except (ValueError, TypeError):
            datastructure.setError(self.getWidgetId(),
                                   "Bad int received")
            ok = 0
        else:
            datamodel[self.fields[0]] = v
            ok = 1
        return ok

    def render(self, mode, datastructure, datamodel):
        """Render this widget from the datastructure or datamodel."""
        value = datastructure[self.getWidgetId()]
        if mode == 'view':
            return escape(value)
        elif mode == 'edit':
            return ('<input type="text" name="%s" value="%s" />'
                    % (escape(self.getHtmlWidgetId()), escape(str(value))))
        else:
            return '[XXX unknown mode %s]' % mode

InitializeClass(CPSIntWidget)


class CPSIntWidgetType(CPSWidgetType):
    """Int widget type."""
    meta_type = "CPS Int Widget Type"
    cls = CPSIntWidget

InitializeClass(CPSIntWidgetType)

##################################################

class CPSCustomizableWidget(CPSWidget):
    """Widget with customizable logic and presentation."""
    meta_type = "CPS Customizable Widget"

    security = ClassSecurityInfo()

    _properties = CPSWidget._properties + (
        {'id': 'widget_type', 'type': 'string', 'mode': 'w',
         'label': 'Widget type'},
        )
    widget_type = ''

    def __init__(self, id, widget_type, **kw):
        self.widget_type = widget_type
        CPSWidget.__init__(self, id, **kw)

    security.declarePrivate('_getType')
    def _getType(self):
        """Get the type object for this widget."""
        wtool = getToolByName(self, 'portal_widgets')
        return getattr(wtool, self.widget_type)

    def prepare(self, datastructure, datamodel):
        """Prepare datastructure from datamodel."""
        return self._getType().prepare(self, datastructure, datamodel)

    def validate(self, datastructure, datamodel):
        """Update datamodel from user data in datastructure."""
        return self._getType().validate(self, datastructure, datamodel)

    def render(self, mode, datastructure, datamodel):
        """Render this widget from the datastructure or datamodel."""
        return self._getType().render(self, mode, datastructure, datamodel)

InitializeClass(CPSCustomizableWidget)


class CPSCustomizableWidgetType(CPSWidgetType):
    """Customizable widget type."""
    meta_type = "CPS Customizable Widget Type"

    security = ClassSecurityInfo()

    _properties = CPSWidgetType._properties + (
        {'id': 'prepare_validate_method', 'type': 'string', 'mode': 'w',
         'label': 'Prepare & Validate Method'},
        {'id': 'render_method', 'type': 'string', 'mode': 'w',
         'label': 'Render Method'},
        )
    prepare_validate_method = ''
    render_method = ''
    _class_props = [p['id'] for p in _properties]

    # Make properties editable.

    def manage_propertiesForm(self, REQUEST, *args, **kw):
        """Override to make the properties editable."""
        return PropertyManager.manage_propertiesForm(
            self, self, REQUEST, *args, **kw)

    security.declareProtected(ManageProperties, 'manage_addProperty')
    security.declareProtected(ManageProperties, 'manage_delProperties')

    # API

    security.declarePrivate('makeInstance')
    def makeInstance(self, id, **kw):
        """Create an instance of this widget type."""
        ob = CPSCustomizableWidget(id, self.getId(), **kw)
        # Copy user-added properties to the instance.
        for prop in self._properties:
            id = prop['id']
            if id in self._class_props:
                continue
            t = prop['type']
            ob.manage_addProperty(id, '', t)
        return ob

    security.declarePrivate('prepare')
    def prepare(self, widget, datastructure, datamodel):
        """Prepare datastructure from datamodel."""
        if not self.prepare_validate_method:
            raise RuntimeError("Missing Prepare Method in widget type %s"
                               % self.getId())
        meth = getattr(widget, self.prepare_validate_method, None)
        if meth is None:
            raise RuntimeError("Unknown Prepare Method %s for widget type %s"
                               % (self.prepare_validate_method, self.getId()))
        return meth('prepare', datastructure, datamodel)

    security.declarePrivate('validate')
    def validate(self, widget, datastructure, datamodel):
        """Update datamodel from user data in datastructure."""
        if not self.prepare_validate_method:
            raise RuntimeError("Missing Validate Method in widget type %s"
                               % self.getId())
        meth = getattr(widget, self.prepare_validate_method, None)
        if meth is None:
            raise RuntimeError("Unknown Validate Method %s for widget type %s"
                               % (self.prepare_validate_method, self.getId()))
        return meth('validate', datastructure, datamodel)

    security.declarePrivate('render')
    def render(self, widget, mode, datastructure, datamodel):
        """Render a widget from the datastructure or datamodel."""
        if not self.render_method:
            raise RuntimeError("Missing Render Method in widget type %s"
                               % self.getId())
        meth = getattr(widget, self.render_method, None)
        if meth is None:
            raise RuntimeError("Unknown Render Method %s for widget type %s"
                               % (self.render_method, self.getId()))
        return meth(mode=mode, datastructure=datastructure,
                    datamodel=datamodel)

InitializeClass(CPSCustomizableWidgetType)

#
# Register widget types.
#

WidgetTypeRegistry.register(CPSCustomizableWidgetType, CPSCustomizableWidget)
WidgetTypeRegistry.register(CPSStringWidgetType, CPSStringWidget)
WidgetTypeRegistry.register(CPSIntWidgetType, CPSIntWidget)
