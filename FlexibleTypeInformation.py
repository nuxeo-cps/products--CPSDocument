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
"""Flexible Type Information

Type information for types described by a flexible set of schemas and layout.
"""

from zLOG import LOG, DEBUG
from Acquisition import aq_base, aq_parent, aq_inner
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo, Unauthorized

from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.CMFCorePermissions import ModifyPortalContent
from Products.CMFCore.CMFCorePermissions import ChangePermissions
from Products.CMFCore.CMFCorePermissions import ManagePortal
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.TypesTool import TypeInformation

from Products.CPSSchemas.Schema import SchemaContainer
from Products.CPSSchemas.Layout import LayoutContainer
from Products.CPSSchemas.DataModel import DataModel
from Products.CPSSchemas.DataStructure import DataStructure
from Products.CPSSchemas.StorageAdapter import AttributeStorageAdapter

from Products.CPSDocument.CPSDocument import addCPSDocument


# inserted into TypesTool by PatchTypesTool
addFlexibleTypeInformationForm = DTMLFile('zmi/addflextiform', globals())

def addFlexibleTypeInformation(container, id, REQUEST=None):
    """Add a Flexible Type Information."""
    flexti = FlexibleTypeInformation(id)
    container._setObject(id, flexti)
    flexti = container._getOb(id)

    flexti.addAction('view',
                     'action_view',
                     'cpsdocument_view',
                     '',
                     View,
                     'object')
    flexti.addAction('contents',
                     'action_folder_contents',
                     'folder_contents',
                     "python: object.portal_types[object.getPortalTypeName()].cps_proxy_type != 'document'",
                     ModifyPortalContent,
                     'object')
    flexti.addAction('edit',
                     'action_edit',
                     'cpsdocument_edit_form',
                     '',
                     ModifyPortalContent,
                     'object')
    flexti.addAction('edit_layout',
                     'action_edit_layout',
                     'cpsdocument_editlayout_form',
                     'python: object.portal_types[object.getPortalTypeName()].flexible_layouts', # condition: only for CMF 1.4 and above
                     ModifyPortalContent,
                     'object')
    flexti.addAction('metadata',
                     'action_metadata',
                     'metadata_edit_form',
                     '',
                     ModifyPortalContent,
                     'object')
    flexti.addAction('localroles',
                     'action_local_roles',
                     'folder_localrole_form',
                     "python: object.portal_types[object.getPortalTypeName()].cps_proxy_type != 'document'",
                     ChangePermissions,
                     'object')

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(container.absolute_url() + "/manage_main")
    else:
        return flexti

# XXX add this at construction above
# this does nothing...
factory_type_information = (
    {'id': 'CPS Document',
     'title': "CPS Document",
     'description': "A base CPS document.",
     'icon': 'cpsdocument_icon.gif',
     'immediate_view': 'metadata_edit_form',
     #'product': 'CPSDocument',
     #'factory': 'addCPSDocument',
     #'meta_type': 'Dummy',
     # CPS attr
     'actions': ({'id': 'view',
                  'name': 'View',
                  'action': 'dummy_view',
                  'permissions': (View,),
                  },
                 {'id': 'edit',
                  'name': 'Edit',
                  'action': 'dummy_edit_form',
                  'permissions': (ModifyPortalContent,),
                  },
                 {'id': 'metadata',
                  'name': 'Metadata',
                  'action': 'metadata_edit_form',
                  'permissions': (ModifyPortalContent,),
                  },
                 ),
     },
    )


class FlexibleTypeInformation(TypeInformation):
    """Flexible Type Information

    Describes how to construct a form-based document.
    Provides resources to manage them.
    """

    meta_type = 'CPS Flexible Type Information'

    security = ClassSecurityInfo()

    _properties = (
        TypeInformation._basic_properties +
        ({'id': 'permission', 'type': 'string', 'mode': 'w',
          'label': 'Constructor permission'},
         # XXX Make above menus.
         ) +
        TypeInformation._advanced_properties +
        (
         {'id':'cps_is_searchable', 'type': 'boolean', 'mode':'w',
          'label':'CPS Searchable'},
         {'id':'cps_proxy_type', 'type': 'selection', 'mode':'w',
          'select_variable': 'getProxyTypesAllowed', 'label':'CPS Proxytype'},
         {'id': 'schemas', 'type': 'tokens', 'mode': 'w',
          'label': 'Schemas'},
         {'id': 'default_layout', 'type': 'string', 'mode': 'w',
          'label': 'Default layout'},
         {'id': 'layout_style_prefix', 'type': 'string', 'mode': 'w',
          'label': 'Layout style prefix'},
         {'id': 'flexible_layouts', 'type': 'tokens', 'mode': 'w',
          'label': 'Flexible layouts'}, # XXX layout1:schema1 layout2:schema2
         {'id': 'storage_methods', 'type': 'tokens', 'mode': 'w',
          'label': 'Storage methods'}, # XXX use schema storage adapters later
         )
        )
    content_meta_type = 'CPS Document'
    permission = 'Add portal content'
    schemas = []
    # XXX assume fixed storage adapters for now
    default_layout = ''
    layout_style_prefix = ''
    flexible_layouts = []
    storage_methods = [] # XXX will later use a storage adapter in the schema
    cps_is_searchable = 1
    cps_proxy_type = 'document'

    def __init__(self, id, **kw):
        TypeInformation.__init__(self, id, **kw)

    manage_options = TypeInformation.manage_options + (
        {'label': 'Export',
         'action': 'manage_export',
         },
        )

    security.declareProtected(ManagePortal, 'manage_export')
    manage_export = DTMLFile('zmi/type_export', globals())
        
    security.declarePublic('getProxyRolesAllowed')
    def getProxyTypesAllowed(self):
        """ return the list of allowed portal types strings """
        return ['','document','folder','folderishdocument']

    #
    # Agent methods
    #

    security.declarePublic('isConstructionAllowed')
    def isConstructionAllowed(self, container):
        """Does the current user have the permission required in
        order to construct an instance in the container?
        """
        return _checkPermission(self.permission, container)

    security.declarePublic('constructInstance')
    def constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type in
        'container', using 'id' as its id.

        Returns the object.
        """
        if not self.isConstructionAllowed(container):
            raise Unauthorized
        ob = self._constructInstance(container, id, *args, **kw)
        return self._finishConstruction(ob)

    security.declarePrivate('_constructInstance')
    def _constructInstance(self, container, id, *args, **kw):
        """Build a bare instance of the appropriate type.

        Does not do CMF-specific checks or workflow insertions.

        Returns the object.
        """
        ob = addCPSDocument(container, id, **kw)
        # XXX fill-in defaults
        # XXX
        return ob

    #
    # Flexible behavior
    #

    def _copyPasteObject(self, obj, dst):
        id = obj.getId()
        container = aq_parent(aq_inner(obj))
        obj = obj._getCopy(container)
        dst._setObject(id, obj)
        return dst._getOb(id)

    def _makeObjectFlexible(self, ob):
        """Make an object flexible.

        Creates an instance copy of the schemas defined in the type object.
        """
        flexible_schemas = self._getFlexibleSchemas()
        flexible_layouts = self._getFlexibleLayouts()
        if not (flexible_schemas or flexible_layouts):
            return

        if not hasattr(aq_base(ob), '.cps_schemas'):
            schemas = SchemaContainer('.cps_schemas')
            ob._setObject(schemas.getId(), schemas)
        schemas = ob._getOb('.cps_schemas')
        if not hasattr(aq_base(ob), '.cps_layouts'):
            layouts = LayoutContainer('.cps_layouts')
            ob._setObject(layouts.getId(), layouts)
        layouts = ob._getOb('.cps_layouts')
        stool = getToolByName(self, 'portal_schemas')
        ltool = getToolByName(self, 'portal_layouts')

        for schema_id in flexible_schemas:
            if not hasattr(aq_base(schemas), schema_id):
                obj = stool._getOb(schema_id)
                self._copyPasteObject(obj, schemas)

        for layout_id in flexible_layouts:
            if not hasattr(aq_base(layouts), layout_id):
                obj = ltool._getOb(layout_id)
                self._copyPasteObject(obj, layouts)

    def _getFlexibleInfo(self, n=None):
        flex = []
        for s in self.flexible_layouts:
            v = s.split(':')
            if len(v) != 2:
                raise RuntimeError("Bad syntax for flexible_layouts, must be"
                                   "'layout1:schema1 layout2:schema2 ...'")
            if n is not None:
                flex.append(v[n])
            else:
                flex.append(v)
        return flex

    def _getFlexibleLayouts(self):
        return self._getFlexibleInfo(0)

    def _getFlexibleSchemas(self):
        return self._getFlexibleInfo(1)

    def _getFlexibleLayoutAndSchemaFor(self, ob, layout_id):
        flex = self._getFlexibleInfo()
        schema_id = None
        for lid, sid in flex:
            if lid == layout_id:
                schema_id = sid
                break
            if sid is None:
                raise ValueError("Layout %s is not flexible" % layout_id)
        layout = ob._getOb('.cps_layouts')._getOb(layout_id)
        schema = ob._getOb('.cps_schemas')._getOb(schema_id)
        return (layout, schema)

    security.declareProtected(ModifyPortalContent, 'flexibleAddWidget')
    def flexibleAddWidget(self, ob, layout_id, wtid, **kw):
        """Add a new widget to the flexible part of a document.

        Returns the widget id.
        """
        self._makeObjectFlexible(ob)
        layout, schema = self._getFlexibleLayoutAndSchemaFor(ob, layout_id)

        # Find free widget id (based on the widget type name).
        widget_id_base = wtid.lower().replace(' widget', '').replace(' ', '')
        widget_id = widget_id_base
        widget_ids = layout.keys()
        n = 0
        while widget_id in widget_ids:
            n += 1
            widget_id = '%s_%d' % (widget_id_base, n)

        # Create the widget.
        widget = layout.addWidget(widget_id, wtid, **kw)

        # Create the needed fields.
        field_types = widget.getFieldTypes()
        fields = []
        for field_type in field_types:
            # Find free field id (based on the field type name).
            s = field_type.lower().replace(' field', '').replace('cps ', '')
            field_id_base = 'val_%s' % s.replace(' ', '') # Prefix with val_
            field_id = field_id_base
            n = 0
            all_field_ids = schema.keys()
            while field_id in all_field_ids:
                n += 1
                field_id = '%s_%d' % (field_id_base, n)

            # Create the field.
            schema.addField(field_id, field_type) # Use default parameters.
            fields.append(field_id)

        # Set the fields used by the widget.
        widget.fields = fields

        # Add the widget to the end of the layout definition.
        layoutdef = layout.getLayoutDefinition()
        layoutdef['rows'].append([{'widget_id': widget_id}])
        layout.setLayoutDefinition(layoutdef)
        return widget_id

    security.declareProtected(ModifyPortalContent, 'flexibleDelWidgets')
    def flexibleDelWidgets(self, ob, layout_id, widget_ids):
        """Delete widgets from the flexible part of a document.
        """
        self._makeObjectFlexible(ob)
        layout, schema = self._getFlexibleLayoutAndSchemaFor(ob, layout_id)

        # Remove the widgets from the layout.
        layoutdef = layout.getLayoutDefinition()
        rows = []
        for row in layoutdef['rows']:
            row = [cell for cell in row
                   if cell['widget_id'] not in widget_ids]
            rows.append(row)
        layoutdef['rows'] = rows
        layout.setLayoutDefinition(layoutdef)

        # Delete the widgets and the fields they use.
        for widget_id in widget_ids:
            widget = layout[widget_id]
            for field_id in widget.fields:
                # Delete the field.
                schema.delSubObject(field_id)
            # Delete the widget.
            layout.delSubObject(widget_id)

    security.declareProtected(ModifyPortalContent, 'flexibleChangeLayout')
    def flexibleChangeLayout(self, ob, layout_id, up_row=None, down_row=None,
                             **kw):
        """Change the flexible layout of a document..

        Can move a row up or down.
        """
        self._makeObjectFlexible(ob)
        layout, schema = self._getFlexibleLayoutAndSchemaFor(ob, layout_id)
        layoutdef = layout.getLayoutDefinition()
        # XXX this should be in the Layout class.
        rows = layoutdef['rows']
        if up_row is not None:
            if up_row >= 1 and up_row < len(rows):
                row = rows.pop(up_row)
                rows.insert(up_row-1, row)
        if down_row is not None:
            if down_row >= 0 and down_row < len(rows)-1:
                row = rows.pop(down_row)
                rows.insert(down_row+1, row)
        layoutdef['rows'] = rows
        layout.setLayoutDefinition(layoutdef)
        return

    security.declarePrivate('getSchemas')
    def getSchemas(self, ob=None):
        """Get the schemas for our type.

        Takes into account flexible schemas from ob.

        Returns a sequence of Schema objects.
        """
        stool = getToolByName(self, 'portal_schemas')
        flexible_schemas = self._getFlexibleSchemas()
        schemas = []
        for schema_id in self.schemas:
            schema = None
            if schema_id in flexible_schemas and ob is not None:
                sc = ob._getOb('.cps_schemas', None)
                if sc is not None:
                    schema = sc._getOb(schema_id, None)
            if schema is None:
                schema = stool._getOb(schema_id, None)
            if schema is None:
                raise RuntimeError("Missing schema '%s' in portal_type '%s'"
                                   % (schema_id, self.getId()))
            schemas.append(schema)
        return schemas

    security.declarePrivate('getDataModel')
    def getDataModel(self, ob, proxy=None, context=None):
        """Get the datamodel for an object of our type."""
        schemas = self.getSchemas(ob)
        adapters = [AttributeStorageAdapter(schema, ob)
                    for schema in schemas]
        dm = DataModel(ob, adapters, proxy=proxy, context=context)
        dm._fetch()
        return dm

    security.declarePrivate('getLayout')
    def getLayout(self, layout_id=None, ob=None):
        """Get the layout for our type.

        Takes into account flexible layouts from ob.
        """
        ltool = getToolByName(self, 'portal_layouts')
        flexible_layouts = self._getFlexibleLayouts()
        if not layout_id:
            layout_id = self.default_layout
        layout = None
        if layout_id in flexible_layouts and ob is not None:
            lc = ob._getOb('.cps_layouts', None)
            if lc is not None:
                layout = lc._getOb(layout_id, None)
        if layout is None:
            layout = ltool._getOb(layout_id, None)
        if layout is None:
            raise ValueError("No layout '%s' in portal_type '%s'"
                             % (layout_id, self.getId()))
        return layout

    security.declarePrivate('_renderLayoutStyle')
    def _renderLayoutStyle(self, context, mode, **kw):
        """Render a layout according to the style defined in
        the FlexTI and the mode.

        Uses context as a rendering context.
        """
        layout_meth = self.layout_style_prefix + mode
        layout_style = getattr(context, layout_meth, None)
        if layout_style is None:
            raise RuntimeError("No layout method '%s'" % layout_meth)
        return layout_style(mode=mode, **kw)

    security.declarePrivate('renderObject')
    def renderObject(self, ob, mode='view', layout_id=None, **kw):
        """Render the object."""
        proxy = kw.get('proxy')
        dm = self.getDataModel(ob, proxy=proxy)
        ds = DataStructure(datamodel=dm)
        layoutob = self.getLayout(layout_id, ob)
        layout = layoutob.getLayoutData(ds)
        return self._renderLayoutStyle(ob, mode, layout=layout,
                                       datastructure=ds, **kw)

    def _commitDM(self, dm):
        """Commits the dm.

        Returns the object. Does all the CMF/CPS indexing and
        notification needed.
        """
        # Update the object from dm.
        ob = dm._commit()
        # CMF/CPS stuff.
        ob.reindexObject()
        evtool = getToolByName(self, 'portal_eventservice', None)
        if evtool is not None:
            evtool.notify('sys_modify_object', ob, {})
        return ob

    security.declarePrivate('renderEditObjectDetailed')
    def renderEditObjectDetailed(self, ob, request=None,
                                 mode='edit', errmode='edit',
                                 layout_id=None, **kw):
        """Modify the object from request, returns detailed information
        about the rendering.

        If request is None, the object is not modified and is rendered
        in the specified mode.

        If request is not None, the parameters are validated and the
        object modified, and rendered in the specified mode. If there is
        a validation error, the object is rendered in mode errmode.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and used for getEditableContent if the object is
        modified.

        Returns (rendered, ok, datastructure):
        - rendered is the rendered HTML,
        - ok is the result of the validation,
        - datastructure is the resulting datastructure.
        """
        proxy = kw.get('proxy')
        dm = self.getDataModel(ob, proxy=proxy)
        ds = DataStructure(datamodel=dm)
        layoutob = self.getLayout(layout_id, ob)
        layoutdata = layoutob.getLayoutData(ds)
        if request is not None:
            ds.updateFromMapping(request.form)
            ok = layoutob.validateLayout(layoutdata, ds)
            if ok:
                ob = self._commitDM(dm)
            else:
                mode = errmode
        else:
            ok = 1
        rendered = self._renderLayoutStyle(ob, mode, layout=layoutdata,
                                           datastructure=ds, ok=ok, **kw)
        return rendered, ok, ds

    security.declarePrivate('renderEditObject')
    def renderEditObject(self, ob, request=None, mode='edit', errmode='edit',
                         layout_id=None, **kw):
        """Modify the object from request, and renders to new mode.

        Returns the rendered HTML.

        See renderEditObjectDetailed for more.
        """
        rendered, ok, ds = self.renderEditObjectDetailed(ob, request=request,
                                                         mode=mode,
                                                         errmode=errmode,
                                                         layout_id=layout_id,
                                                         **kw)
        return rendered

    security.declarePrivate('validateStoreRenderObject')
    def validateStoreRenderObject(self, ob, request=None, mode='edit',
                                  okmode='edit', errmode='edit',
                                  layout_id=None, **kw):
        """Modify the object from request, store data, and renders to new mode.

        If request is None, the object is rendered in the specified mode.

        If request is not None:
        - the parameters are validated.
        - if there is a validation error:
          - the object is rendered in mode errmode;
        - if there is no validation error:
          - the object is modified, or a storage method is called,
          - the object is renderd in mode okmode.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and used for getEditableContent if the object is
        modified.
        """
        proxy = kw.get('proxy')
        dm = self.getDataModel(ob, proxy=proxy)
        ds = DataStructure(datamodel=dm)
        layoutob = self.getLayout(layout_id, ob)
        # Prepare each widget, and so update the datastructure.
        layoutdata = layoutob.getLayoutData(ds)
        if request is not None:
            # Validate from request.
            ds.updateFromMapping(request.form)
            ok = layoutob.validateLayout(layoutdata, ds)
            if ok:
                method_name = None
                for sm in self.storage_methods:
                    v = sm.split(':')
                    if len(v) != 2:
                        raise ValueError("Bad syntax in storage_methods")
                    if v[0] != mode:
                        continue
                    method_name = v[1]
                    break
                if method_name:
                    # Do storage using a method.
                    method = getattr(ob, method_name, None)
                    if method is None:
                        raise ValueError("No storage method %s" %
                                         method_name)
                    method(mode, layout=layoutdata, datastructure=ds, **kw)
                else:
                    ob = self._commitDM(dm)
                mode = okmode
            else:
                mode = errmode
        else:
            ok = 1
        return self._renderLayoutStyle(ob, mode, layout=layoutdata,
                                       datastructure=ds, ok=ok, **kw)

    security.declarePrivate('editObject')
    def editObject(self, ob, mapping):
        """Modify the object's fields from a mapping."""
        proxy = mapping.get('proxy') # XXX Use mapping to get it?
        dm = self.getDataModel(ob, proxy=proxy)
        for key, value in mapping.items():
            if dm.has_key(key):
                dm[key] = value
        self._commitDM(dm)

    security.declarePublic('renderCreateObjectDetailed')
    def renderCreateObjectDetailed(self, container, request=None, validate=1,
                                   mode='create', layout_id=None,
                                   create_callback=None,
                                   created_callback=None,
                                   **kw):
        """Render an object for creation, maybe create it.

        If validate is false, the object is rendered from default values
        or the ones in request, in the specified mode.

        If validate is true:
        - the parameters from request are validated,
        - if there is a validation error:
          - the object is rendered in mode mode,
        - if there is no validation error:
          - the object is created by calling create_callback in the
            context of the container and with argument the type_name
            and the datamodel,
          - created_callback is called in the context of the object.

        Returns (rendered, ok, datastructure):
        - rendered is the rendered HTML (may also have redirected),
        - ok is the result of the validation,
        - datastructure is the resulting datastructure.
        """
        dm = self.getDataModel(None, context=container)
        ds = DataStructure(datamodel=dm)
        layoutob = self.getLayout(layout_id)
        # Prepare each widget, and so update the datastructure.
        layoutdata = layoutob.getLayoutData(ds)
        rendered = None
        if not validate:
            # Initial display, datastructure contains defaults.
            if request is not None:
                # Update with initial data from request
                ds.updateFromMapping(request.form)
            ok = 1
        else:
            # Validate from request.
            ds.updateFromMapping(request.form)
            ok = layoutob.validateLayout(layoutdata, ds)
        if validate and ok:
            create_func = getattr(container, create_callback, None)
            if create_func is None:
                raise ValueError("Unknown create_callback %s" %
                                 create_callback)
            type_name = self.getId()
            proxy = create_func(type_name, dm)
            # XXX check proxy is accessible?
            if hasattr(aq_base(proxy), 'getContent'):
                # Get CPS content object.
                ob = proxy.getContent()
            else:
                ob = proxy
            dm._setObject(ob, proxy=proxy)
            self._commitDM(dm)
            created_func = getattr(proxy, created_callback, None)
            if created_func is None:
                raise ValueError("Unknown created_callback %s" %
                                 created_callback)
            rendered = created_func() or ''
        else:
            rendered = self._renderLayoutStyle(container, mode,
                                               layout=layoutdata,
                                               datastructure=ds, ok=ok,
                                               **kw)
        return rendered, ok, ds

    security.declarePublic('renderCreateObject')
    def renderCreateObject(self, *args, **kw):
        """Render an object for creation, maybe create it.

        Returns the rendered HTML.

        See renderCreateObjectDetailed for more info.
        """
        rendered, ok, ds = self.renderCreateObjectDetailed(*args, **kw)
        return rendered

InitializeClass(FlexibleTypeInformation)
