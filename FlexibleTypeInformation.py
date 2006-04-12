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

import warnings
from zLOG import LOG, DEBUG, WARNING
from Acquisition import aq_base, aq_parent, aq_inner
from Globals import InitializeClass, DTMLFile
from AccessControl import ClassSecurityInfo, Unauthorized
from OFS.Image import File, Image

from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import ChangePermissions
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.TypesTool import FactoryTypeInformation
from Products.CMFCore.interfaces import ITypeInformation

from Products.CPSCore.EventServiceTool import getEventService
from Products.CPSSchemas.utils import copyFile, copyImage
from Products.CPSSchemas.Schema import SchemaContainer
from Products.CPSSchemas.Layout import LayoutContainer
from Products.CPSSchemas.DataModel import DataModel
from Products.CPSSchemas.DataStructure import DataStructure
from Products.CPSSchemas.StorageAdapter import AttributeStorageAdapter, \
     MetaDataStorageAdapter

from Products.CPSDocument.CPSDocument import addCPSDocument
from Products.CPSSchemas.BasicWidgets import CPSCompoundWidget

from Products.CPSDocument.utils import getFormUid

import zope.interface


def addFlexibleTypeInformation(container, id, REQUEST=None):
    """Add a Flexible Type Information."""
    flexti = FlexibleTypeInformation(id)
    container._setObject(id, flexti)
    flexti = container._getOb(id)

    flexti.addAction('view',
                     'action_view',
                     'string:${object_url}/cpsdocument_view',
                     '',
                     View,
                     'object')
    flexti.addAction('new_content',
                     'action_new_content',
                     'string:${object_url}/folder_factories',
                     "python:object.getTypeInfo().cps_proxy_type != 'document'",
                     ModifyPortalContent,
                     'object')
    flexti.addAction('contents',
                     'action_folder_contents',
                     'string:${object_url}/folder_contents',
                     "python:object.getTypeInfo().cps_proxy_type != 'document'",
                     ModifyPortalContent,
                     'object')
    flexti.addAction('edit',
                     'action_edit',
                     'string:${object_url}/cpsdocument_edit_form',
                     '',
                     ModifyPortalContent,
                     'object')
    flexti.addAction('metadata',
                     'action_metadata',
                     'string:${object_url}/cpsdocument_metadata',
                     'not:portal/portal_membership/isAnonymousUser',
                     View,
                     'object')
    flexti.addAction('localroles',
                     'action_local_roles',
                     'string:${object_url}/folder_localrole_form',
                     "python:object.getTypeInfo().cps_proxy_type != 'document'",
                     ChangePermissions,
                     'object')

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(container.absolute_url() + "/manage_main")
    else:
        return flexti

# Patch TypesTool to add this method (BBB used by CPSInstaller)
from Products.CMFCore.TypesTool import TypesTool
TypesTool.addFlexibleTypeInformation = addFlexibleTypeInformation


class FlexibleTypeInformation(FactoryTypeInformation):
    """Flexible Type Information

    Describes how to construct a form-based document.
    Provides resources to manage them.
    """

    meta_type = 'CPS Flexible Type Information'

    zope.interface.implements(ITypeInformation)

    security = ClassSecurityInfo()

    _properties = (
        FactoryTypeInformation._properties + (
        {'id': 'schemas', 'type': 'tokens', 'mode': 'w',
         'label': 'Schemas'},
        {'id': 'layouts', 'type': 'tokens', 'mode': 'w',
         'label': 'Layouts'},
        {'id': 'layout_clusters', 'type': 'tokens', 'mode': 'w',
         'label': 'Layout clusters'},
        # Layout clusters: sequence of tokens of the form
        #  clusterid:layoutid_1,layoutid_2,layoutid_3...
        # Layout ids do not need to be listed in the 'layouts' property. This
        # list of layouts can be considered as the default cluster.
        {'id': 'flexible_layouts', 'type': 'tokens', 'mode': 'w',
         'label': 'Flexible layouts'}, # XXX layout1:schema1 layout2:schema2
        {'id': 'storage_methods', 'type': 'tokens', 'mode': 'w',
         'label': 'Storage methods'}, # XXX use schema storage adapters later
        )
        )
    content_meta_type = 'CPS Document'
    product = 'CPSDocument'
    factory = 'addCPSDocument'
    schemas = ()
    # XXX assume fixed storage adapters for now
    layouts = ()
    layout_clusters = ()
    flexible_layouts = ()
    storage_methods = () # XXX will later use a storage adapter in the schema
    cps_is_searchable = 1
    cps_proxy_type = 'document'
    cps_display_as_document_in_listing = 0

    def __init__(self, id, **kw):
        FactoryTypeInformation.__init__(self, id, **kw)

    manage_options = FactoryTypeInformation.manage_options + (
        {'label': 'Export',
         'action': 'manage_genericSetupExport.html',
         },
        )

    security.declareProtected(ManagePortal, 'manage_export')
    manage_export = DTMLFile('zmi/type_export', globals())

    security.declarePublic('getProxyTypesAllowed')
    def getProxyTypesAllowed(self):
        """Return the list of allowed portal types strings."""
        # This method is monkey-patched by CPSCore.TypesToolPatches
        return ['',
                'document',
                'folder',
                'folderishdocument',
                'btreefolder',
                'btreefolderishdocument',
                ]

    #
    # Agent methods
    #

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
        Does not index the object.

        Returns the object.
        """
        # This is FactoryTypeInformation.constructInstance except
        # that no security checks are done.
        m = self._getFactoryMethodNoSec(container)
        id = str(id)
        if getattr(m, 'isDocTemp', 0):
            args = (m.aq_parent, self.REQUEST) + args
            kw['id'] = id
        else:
            args = (id,) + args

        id = m(*args, **kw) or id  # allow factory to munge ID
        ob = container._getOb( id )

        # Init from datamodel if present, or from an empty one
        # to get default values. In the latter case, we have no proxy.
        dm = kw.get('datamodel')
        proxy = dm and dm.getProxy()
        if dm is None or dm.getObject() is None:
            dm = self.getDataModel(None, context=container)

        # Initialize the dm with values within the kw. Take care : the values
        # corresponding to arguments of functions such as container, id,
        # type_name etc... won't work in here since they won't be taken within
        # the kw.
        # It is typically used this way :
        # wftool.invokeFactoryFor(container, type_name, id, Title=xxx,
        # Description=xxxx)
        for k, v in kw.items():
            if dm.has_key(k):
                dm.set(k, v)

        dm._setObject(ob, proxy=proxy)
        dm._commit(check_perms=0)

        return ob

    security.declarePrivate('_getFactoryMethodNoSec')
    def _getFactoryMethodNoSec(self, container):
        """Get the factory method, no security checks."""
        if not self.product or not self.factory:
            raise ValueError("Product factory for %s was undefined" %
                             self.getId())
        p = container.manage_addProduct[self.product]
        m = getattr(p, self.factory, None)
        if m is None:
            raise ValueError("Product factory for %s was invalid" %
                             self.getId())
        return m

    #
    # Flexible behavior
    #

    def _copyPasteObject(self, obj, dst, dst_id=None):
        if dst_id:
            id = dst_id
        else:
            id = obj.getId()
        container = aq_parent(aq_inner(obj))
        obj = obj._getCopy(container)
        dst._setObject(id, obj)
        obj._setId(id)
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
            # remove template widget
            layout = layouts[layout_id]
            widget2del = [w.getId() for k, w in layout.items() if w.isHidden()]
            layout.manage_delObjects(widget2del)

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

        Takes care of compound widget.

        Returns the widget id.
        """
        ltool = getToolByName(self, 'portal_layouts')
        layout_ob = ltool._getOb(layout_id)
        tpl_widget = layout_ob[wtid]
        if not isinstance(tpl_widget, CPSCompoundWidget):
            return self._flexibleAddSimpleWidget(ob, layout_id, wtid, **kw)

        # Compound widget - creating sub widgets
        new_widget_ids = []
        for widget_id in tpl_widget.widget_ids:
            id = self._flexibleAddSimpleWidget(ob, layout_id, widget_id,
                                              layout_register=0, **kw)
            new_widget_ids.append(id)

        # creating the compound widget
        widget_id = self._flexibleAddSimpleWidget(ob, layout_id, wtid, **kw)
        layout, schema = self._getFlexibleLayoutAndSchemaFor(ob, layout_id)
        widget = layout[widget_id]

        # set sub widget ids
        widget.widget_ids = new_widget_ids

        return widget_id


    security.declarePrivate('_flexibleAddSimpleWidget')
    def _flexibleAddSimpleWidget(self, ob, layout_id, wtid,
                                layout_register = 1, **kw):
        """Add a new widget to the flexible part of a document.

        Returns the widget id.
        """
        ltool = getToolByName(self, 'portal_layouts')
        layout_global = ltool._getOb(layout_id)

        self._makeObjectFlexible(ob)
        layout, schema = self._getFlexibleLayoutAndSchemaFor(ob, layout_id)

        if layout_global.has_key(wtid):
            tpl_widget = layout_global[wtid]
        else:
            tpl_widget = layout[wtid]

        widget_id = wtid
        widget_ids = layout.keys()
        n = 0
        while widget_id in widget_ids:
            n += 1
            widget_id = '%s_%d' % (wtid, n)

        LOG('FlexibleAddWidget', DEBUG, 'adding widget_id %s' % widget_id)
        self._copyPasteObject(tpl_widget, layout,
                              dst_id=layout.prefix + widget_id)

        widget = layout[widget_id]

        # Create the needed fields.
        field_types = widget.getFieldTypes()
        field_inits = widget.getFieldInits()
        fields = []
        i = 0
        for field_type in field_types:
            # Find free field id (based on the field type name).
            field_id = '%s_f%d' % (widget_id, 0)
            field_ids = schema.keys()
            n = 0
            while field_id in field_ids:
                n += 1
                field_id = '%s_f%d' % (widget_id, n)

            # Create the field.
            if field_inits:
                kw = field_inits[i]
            else:
                kw = {}
            i += 1
            schema.addField(field_id, field_type, **kw)
            LOG('FlexibleAddWidget', DEBUG, 'adding field_id %s init %s'
                % (field_id, str(kw)))
            fields.append(field_id)

        # Set the fields used by the widget.
        widget.fields = fields
        if layout_register:
            # Add the widget to the end of the layout definition.
            layoutdef = layout.getLayoutDefinition()
            layoutdef['rows'].append([{'widget_id': widget_id}])
            layout.setLayoutDefinition(layoutdef)

        return widget.getWidgetId()

    security.declareProtected(ModifyPortalContent, 'flexibleDelWidgets')
    def flexibleDelWidgets(self, ob, layout_id, widget_ids):
        """Delete widgets from the flexible part of a document.

        Takes care of Compound widget.
        """
        self._makeObjectFlexible(ob)
        layout, schema = self._getFlexibleLayoutAndSchemaFor(ob, layout_id)
        new_widget_ids = []
        for widget_id in widget_ids:
            widget = layout[widget_id]
            if widget.meta_type == 'CPS Compound Widget':
                new_widget_ids.extend(widget.widget_ids)
            new_widget_ids.append(widget_id)

        return self._flexibleDelSimpleWidgets(ob, layout_id, new_widget_ids)

    security.declarePrivate('_flexibleDelSimpleWidgets')
    def _flexibleDelSimpleWidgets(self, ob, layout_id, widget_ids):
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
        flexible_widgets = layout.getFlexibleWidgetIds()
        for widget_id in widget_ids:
            widget = layout[widget_id]
            for field_id in widget.fields:
                LOG('FlexibleTypeInformation', DEBUG, 'deleting field %s' %
                        field_id)
                # Delete the field.
                schema.delSubObject(field_id)
                # XXX FIXME it has to be handle differently
                # It assumes it is an AttributeStorage.
                # Though, this one is enough to prevent the file to be proposed
                # again next time you create the same kind of widget.
                # Delete from the object otherweise the same content appears
                # each time you wanna add the same kind of widget again.
                # Was the case with the attached file.
                if field_id in ob.objectIds():
                    LOG('FlexibleTypeInformation', DEBUG, 'deleting object %s' %
                            field_id)
                    ob.manage_delObjects([field_id])
                else:
                    # Other fields such as string Fields are stored as
                    # non-object attributes
                    delattr(ob, field_id)
            if widget_id in flexible_widgets:
                # Hide the widget as we may need it to create new widget.
                LOG('FlexibleTypeInformation', DEBUG, 'hiding widget %s' %
                        widget_id)
                widget.hide()
            else:
                # Delete the widget.
                LOG('FlexibleTypeInformation', DEBUG, 'deleting widget %s' %
                        widget_id)
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

    security.declarePrivate('_listSchemas')
    def _listSchemas(self, ob=None):
        """Get the schemas for our type.

        Takes into account flexible schemas from ob.

        Returns a list of Schema objects.
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
        schemas = self._listSchemas(ob)
        adapters = []
        for schema in schemas:
            if schema.id.startswith('metadata'):
                adapters.append(MetaDataStorageAdapter(schema, ob, proxy=proxy))
            else:
                adapters.append(AttributeStorageAdapter(schema, ob, proxy=proxy))
        dm = DataModel(ob, adapters, proxy=proxy, context=context)
        dm._fetch()
        return dm

    security.declarePrivate('getLayout')
    def getLayout(self, layout_id, ob=None):
        """Get a layout for our type.

        Takes into account flexible layouts from ob.
        """
        ltool = getToolByName(self, 'portal_layouts')
        flexible_layouts = self._getFlexibleLayouts()
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

    security.declarePrivate('getLayoutIds')
    def getLayoutIds(self, layout_id=None, cluster=None):
        """Get the list of layout ids for our type.

        If layout_id is specified, uses it (it may be a tuple).

        Otherwise if cluster is specified, uses the layouts defined by
        that cluster in the layout_clusters mapping.

        Otherwise uses the default layouts.

        Returns a list of layout ids.
        """
        layout_ids = None
        if layout_id is not None:
            if isinstance(layout_id, str):
                layout_ids = [layout_id]
            elif isinstance(layout_id, (tuple, list)):
                layout_ids = list(layout_id)
            else:
                raise ValueError("Invalid layout id %s in portal_type '%s'"
                                 % (`layout_id`, self.getId()))
        elif cluster is not None:
            for s in self.layout_clusters:
                try:
                    cl, v = s.split(':')
                    if v:
                        v = v.split(',')
                    else:
                        v = []
                except ValueError:
                    LOG('getLayoutIds', WARNING,
                        "Invalid layout cluster %s in portal_type '%s'"
                        %(`s`, self.getId()))
                    continue
                if cl != cluster:
                    continue
                layout_ids = v
                break

        if layout_ids is None:
            layout_ids = list(self.layouts)

        return layout_ids

    security.declarePrivate('_computeLayoutStructures')
    def _computeLayoutStructures(self, datastructure, layout_mode,
                                 layout_id=None, cluster=None,
                                 ob=None, request=None,
                                 use_session=False):
        """Initialize the datastructure and compute the layout.

        Datastructure is initialized according to the widgets, and
        if available from the request and the session.

        Computes the layout structure.

        Returns a list of layout_structures.
        """
        lids = self.getLayoutIds(layout_id=layout_id, cluster=cluster)
        layouts = [self.getLayout(lid, ob) for lid in lids]

        for layout in layouts:
            layout.prepareLayoutWidgets(datastructure)
        if request is not None:
            if use_session:
                # Restore data from the session
                formuid = getFormUid(request)
                datastructure._updateFromSession(request, formuid)
            # Update with the form itself
            datastructure.updateFromMapping(request.form)

        layout_structures = []
        datamodel = datastructure.getDataModel()
        for layout in layouts:
            layout_structure = layout.computeLayoutStructure(layout_mode,
                                                             datamodel)
            layout_structures.append(layout_structure)

        return layout_structures

    security.declarePrivate('_validateLayoutStructures')
    def _validateLayoutStructures(self, layout_structures,
                                  datastructure, request=None,
                                  use_session=False, **kw):
        """Validate all layout structures.

        Returns a boolean is_valid.
        """
        datastructure.clearErrors()
        is_valid = True
        for layout_structure in layout_structures:
            layout = layout_structure['layout']
            ok = layout.validateLayoutStructure(layout_structure,
                                                datastructure, **kw)
            is_valid = is_valid and ok
        if use_session:
            if is_valid:
                # We don't need anything from the session anymore
                datastructure._removeFromSession(request)
            else:
                # Backup data in the session
                formuid = getFormUid(request)
                datastructure._saveToSession(request, formuid)
        return is_valid

    security.declarePrivate('_renderLayouts')
    def _renderLayouts(self, layout_structures, datastructure, context,
                       no_form=False, **kw):
        """Get HTML rendering of all layouts.

        ``context`` is the rendering context.

        BBB: no_form will be implicit in CPS 3.5.0
        """
        layout_mode = kw['layout_mode']
        all_rendered = ''
        nb_layouts = len(layout_structures)
        flexible_layouts = self._getFlexibleLayouts()
        for i, layout_structure in enumerate(layout_structures):
            if no_form:
                # We don't want to generate form header/footer
                first_layout = last_layout = False
            else:
                # find if is the first/last layout
                first_layout = (i == 0)
                last_layout = (i == nb_layouts-1)
            is_flexible = layout_mode != 'create' and \
                          layout_structure['layout_id'] in flexible_layouts
            # Render layout structure.
            layout = layout_structure['layout']
            layout.renderLayoutStructure(layout_structure, datastructure, **kw)
            # Apply layout style.
            rendered = layout.renderLayoutStyle(layout_structure,
                                                datastructure, context,
                                                first_layout=first_layout,
                                                last_layout=last_layout,
                                                is_flexible=is_flexible,
                                                **kw)
            all_rendered += rendered
        return all_rendered

    #
    # API
    #

    security.declareProtected(View, 'renderObject')
    def renderObject(self, ob, layout_mode='view', layout_id=None,
                     cluster=None, request=None, context=None,
                     use_session=False, **kw):
        """Render the object.

        The datastructure information comes from the object, and, if
        available, the request (to be able to pass explicit values in
        the URL) and the session (if use_session is true).

        ``context`` is used to find the layout method.
        """
        proxy = kw.get('proxy')
        dm = self.getDataModel(ob, proxy=proxy, context=context)
        ds = DataStructure(datamodel=dm)

        layout_structures = self._computeLayoutStructures(
            ds, layout_mode, layout_id=layout_id, cluster=cluster,
            ob=ob, request=request, use_session=use_session)

        if context is None:
            context = ob
        return self._renderLayouts(layout_structures, ds, context,
                                   layout_mode=layout_mode, **kw)

    security.declareProtected(View, 'validateObject')
    def validateObject(self, ob, layout_mode='edit', layout_id=None,
                       cluster=None, request=None, use_session=False,
                       pre_commit_hook=None,
                       **kw):
        """Validate the modifications posted on an object.

        The data from the object, the request (and the session if
        use_session is True) is validated.

        If there is no validation error, the object modified. In
        creation mode, it's the caller's responsability to create the
        object using the datamodel.

        If there is a validation error and use_session is True, the
        datastructure is saved in the session.

        An optional 'proxy' arg will be passed to the layouts and used
        for getEditableContent if the object is modified.

        An optional 'context' arg will be used to provide context to the
        widgets.

        An optional 'pre_commit_hook' arg can be given. It takes the
        datamodel and request as arguments, and gets **kw forwarded. It
        can access the object through the datamodel, but must maintain
        consistency.

        Returns (is_valid, datastructure):
          - is_valid is the result of the validation,
          - datastructure is the resulting datastructure, it can be
            used to create an object if ob was None.
        """
        if request is None:
            raise ValueError("request is None")

        proxy = kw.get('proxy')
        context = kw.get('context')
        dm = self.getDataModel(ob, proxy=proxy, context=context)
        ds = DataStructure(datamodel=dm)

        # To validate we must have the layout structures to know
        # which widgets are present.
        # This also updates the datastructure from request/session.
        layout_structures = self._computeLayoutStructures(
            ds, layout_mode, layout_id=layout_id, cluster=cluster,
            ob=ob, request=request, use_session=use_session)

        # This also saves datastructure in session if there are errors.
        is_valid = self._validateLayoutStructures(
            layout_structures, ds, layout_mode=layout_mode,
            request=request, use_session=use_session)

        if is_valid and ob is not None:
            if pre_commit_hook is not None:
                pre_commit_hook(dm, request=request, **kw)
            ob = self._commitDM(dm)

        return is_valid, ds

    def _commitDM(self, dm, check_perms=1):
        """Commits the dm.

        Returns the object. Does all the CMF/CPS indexing and
        notification needed.
        """
        # Update the object from dm.
        ob = dm._commit(check_perms=check_perms)
        # CMF/CPS stuff.
        self._notifyModification(ob)
        return ob

    def _notifyModification(self, ob):
        # Note that the catalog won't index repository objects.
        ob.reindexObject()
        evtool = getEventService(self)
        evtool.notify('sys_modify_object', ob, {})
        # If the object is in the repository, the proxy tool
        # will do what's necessary to reindex the proxies
        # and send a notification for them.

    # BBB The following methods are now obsolete and will go away in CPS 3.5.0

    security.declarePrivate('renderEditObjectDetailed')
    def renderEditObjectDetailed(self, ob, request=None,
                                 layout_mode='edit',
                                 layout_mode_err='edit',
                                 layout_id=None, cluster=None,
                                 **kw):
        """Modify the object from request, returns detailed information
        about the rendering.

        If request is None, the object is not modified and is rendered
        in the specified layout_mode.

        If request is not None, the parameters are validated and the
        object modified, and rendered in the specified layout_mode. If
        there is a validation error, the object is rendered in
        layout_mode_err.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and used for getEditableContent if the object is
        modified.

        Optional 'pre_commit_hook' and 'post_commit_hook' args can be given.
        These are callables. The request and kw get forwarded to them.
        The first one takes datamodel as unique positional arg. It can access
        the object through the datamodel, but must maintain consistency. 
        The second one takes the object, and must return it in case it changed.

        Returns (rendered, ok, datastructure):
          - rendered is the rendered HTML,
          - ok is the result of the validation,
          - datastructure is the resulting datastructure.
        """

        warnings.warn("renderEditObjectDetailed is obsolete and will be "
                      "removed in CPS 3.5.0", DeprecationWarning, 2)

        proxy = kw.get('proxy')
        dm = self.getDataModel(ob, proxy=proxy)
        ds = DataStructure(datamodel=dm)

        layout_structures = self._computeLayoutStructures(
            ds, layout_mode, layout_id=layout_id, cluster=cluster,
            ob=ob, request=request)

        if request is None:
            is_valid = 1
        else:
            is_valid = self._validateLayoutStructures(layout_structures, ds,
                                                      layout_mode=layout_mode,
                                                      request=request)
            if is_valid:
                # apply pre-commit hook
                hook = kw.get('pre_commit_hook')
                if hook is not None:
                    hook(dm, request=request, **kw)
                ob = self._commitDM(dm)

                # apply post-commit hook
                hook = kw.get('post_commit_hook')
                if hook is not None:
                    n_ob = hook(ob, request=request, **kw)
                    if n_ob is not None: # 'or' is shorter but slowlier
                        ob = n_ob
            else:
                layout_mode = layout_mode_err

        rendered = self._renderLayouts(layout_structures, ds, ob,
                                       layout_mode=layout_mode, ok=is_valid,
                                       **kw)
        return rendered, is_valid, ds

    security.declarePrivate('renderEditObject')
    def renderEditObject(self, *args, **kw):
        """Modify the object from request, and renders to new layout mode.

        Returns the rendered HTML.

        See renderEditObjectDetailed for more.
        """
        warnings.warn("renderEditObject is obsolete and will be "
                      "removed in CPS 3.5.0", DeprecationWarning, 2)
        rendered, ok, ds = self.renderEditObjectDetailed(*args, **kw)
        return rendered

    security.declarePrivate('validateStoreRenderObject')
    def validateStoreRenderObject(self, ob, request=None,
                                  layout_mode='edit',
                                  layout_mode_ok='edit',
                                  layout_mode_err='edit',
                                  layout_id=None, cluster=None,
                                  **kw):
        """Modify the object from request, store data, and renders to
        new layout mode.

        If request is None, the object is rendered in the specified
        layout_mode.

        If request is not None:
          - the parameters are validated.
          - if there is a validation error:
            - the object is rendered in layout_mode_err.
          - if there is no validation error:
            - the object is modified, or a storage method is called,
            - the object is renderd in layout_mode_ok.

        An optional 'proxy' arg can be given, it will be passed to the
        layouts and used for getEditableContent if the object is
        modified.
        """
        warnings.warn("validateStoreRenderObject is obsolete and will be "
                      "removed in CPS 3.5.0", DeprecationWarning, 2)

        proxy = kw.get('proxy')
        dm = self.getDataModel(ob, proxy=proxy)
        ds = DataStructure(datamodel=dm)

        layout_structures = self._computeLayoutStructures(
            ds, layout_mode, layout_id=layout_id, cluster=cluster,
            ob=ob, request=request)

        is_valid = 1
        if request is not None:
            is_valid = self._validateLayoutStructures(layout_structures, ds,
                                                      layout_mode=layout_mode,
                                                      request=request)
            if not is_valid:
                layout_mode = layout_mode_err
            else:
                layout_mode = layout_mode_ok
                method_name = None
                for sm in self.storage_methods:
                    v = sm.split(':')
                    if len(v) != 2:
                        raise ValueError("Bad syntax in storage_methods")
                    if v[0] != layout_mode:
                        continue
                    method_name = v[1]
                    break
                if method_name is None:
                    ob = self._commitDM(dm)
                else:
                    # Do storage using a method.
                    method = getattr(ob, method_name, None)
                    if method is None:
                        raise ValueError("No storage method %s" %
                                         method_name)
                    method(layout_mode, datastructure=ds, **kw)

        return self._renderLayouts(layout_structures, ds, ob,
                                   layout_mode=layout_mode, ok=is_valid,
                                   **kw)

    security.declarePrivate('editObject')
    def editObject(self, ob, mapping, proxy=None):
        """Modify the object's fields from a mapping."""
        dm = self.getDataModel(ob, proxy=proxy)
        for key, value in mapping.items():
            if dm.has_key(key):
                dm[key] = value
        self._commitDM(dm)

    security.declarePublic('renderCreateObjectDetailed')
    def renderCreateObjectDetailed(self, container, request=None, validate=1,
                                   layout_mode='create',
                                   layout_id=None, cluster=None,
                                   create_callback=None,
                                   created_callback=None,
                                   **kw):
        """Render an object for creation, maybe create it.

        If validate is false, the object is rendered from default values
        or the ones in request, in the specified layout mode.

        If validate is true:
          - the parameters from request are validated,
          - if there is a validation error:
            - the object is rendered in layout_mode,
          - if there is no validation error:
            - the object is created by calling create_callback in the
              context of the container and with argument the type_name
              and the datamodel,
            - created_callback is called in the context of the object.

        Returns (rendered, is_valid, datastructure):
          - rendered is the rendered HTML (may also have redirected),
          - is_valid is the result of the validation,
          - datastructure is the resulting datastructure.
        """
        warnings.warn("renderCreateObjectDetailed is obsolete and will be "
                      "removed in CPS 3.5.0", DeprecationWarning, 2)

        dm = self.getDataModel(None, context=container)
        ds = DataStructure(datamodel=dm)

        layout_structures = self._computeLayoutStructures(
            ds, layout_mode, layout_id=layout_id, cluster=cluster,
            ob=None, request=request)

        is_valid = 1
        if validate:
            is_valid = self._validateLayoutStructures(layout_structures, ds,
                                                      layout_mode=layout_mode,
                                                      request=request)
        if not validate or not is_valid:
            rendered = self._renderLayouts(layout_structures, ds, container,
                                           layout_mode=layout_mode,
                                           ok=is_valid, **kw)
        else:
            # creation
            create_func = getattr(container, create_callback, None)
            if create_func is None:
                raise ValueError("Unknown create_callback %s" %
                                 create_callback)
            type_name = self.getId()
            proxy = create_func(type_name, dm)
            if hasattr(aq_base(proxy), 'getContent'):
                ob = proxy.getContent()
            else:
                ob = proxy
            self._notifyModification(ob)
            created_func = getattr(proxy, created_callback, None)
            if created_func is None:
                raise ValueError("Unknown created_callback %s" %
                                 created_callback)
            rendered = created_func() or ''

        return rendered, is_valid, ds

    security.declarePublic('renderCreateObject')
    def renderCreateObject(self, *args, **kw):
        """Render an object for creation, maybe create it.

        Returns the rendered HTML.

        See renderCreateObjectDetailed for more info.
        """
        warnings.warn("renderCreateObject is obsolete and will be "
                      "removed in CPS 3.5.0", DeprecationWarning, 2)
        rendered, ok, ds = self.renderCreateObjectDetailed(*args, **kw)
        return rendered

InitializeClass(FlexibleTypeInformation)
