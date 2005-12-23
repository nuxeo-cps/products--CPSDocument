# Copyright (c) 2005 Nuxeo SARL <http://nuxeo.com>
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
##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
#
# $Id$
"""Types tool import/export for CMFSetup.

Knows about Flexible Type Information
"""

# XXX currently derived from CMFSetup/typeinfo.py HEAD, but will be
# removed when CMF 1.5.2 is out.


import os
import Products
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Globals import package_home
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

#from Products.CMFCore.TypesTool import typeClasses
from Products.CMFCore.utils import getToolByName

from Products.CMFCore.permissions import ManagePortal
from Products.CMFSetup.utils import ConfiguratorBase
from Products.CMFSetup.utils import CONVERTER, DEFAULT, KEY


_pkgdir = package_home(globals())
_xmldir = os.path.join(_pkgdir, 'xml')


#
#   Entry points
#
_TOOL_FILENAME = 'typestool.xml'

def importTypesTool( context ):

    """ Import types tool and content types from XML files.
    """
    site = context.getSite()
    encoding = context.getEncoding()

    types_tool = getToolByName( site, 'portal_types' )

    if context.shouldPurge():

        for type in types_tool.objectIds():
            types_tool._delObject(type)

    ttc = TypesToolConfigurator( site, encoding )
    xml = context.readDataFile( _TOOL_FILENAME )
    if xml is None:
        return 'Types tool: Nothing to import.'

    tool_info = ttc.parseXML( xml )
    tic = TypeInfoConfigurator( site, encoding )
    old_tic = OldTypeInfoConfigurator( site, encoding )

    for type_info in tool_info[ 'types' ]:

        filename = type_info[ 'filename' ]
        sep = filename.rfind( '/' )
        if sep == -1:
            text = context.readDataFile( filename )
        else:
            text = context.readDataFile( filename[sep+1:], filename[:sep] )

        is_old = '<description>' in text
        if is_old:
            info = old_tic.parseXML( text )
        else:
            info = tic.parseXML( text )

        type_id = str(info['id'])
        if 'kind' in info:
            klass_info = [ x for x in typeClasses
                           if x[ 'name' ] == info[ 'kind' ] ][ 0 ]

            type_info = klass_info['class'](type_id)

            if type_id in types_tool.objectIds():
                types_tool._delObject(type_id)

            types_tool._setObject(type_id, type_info)
            type_info = types_tool._getOb(type_id)
            type_info._updateProperty('title', info['id'])
            type_info._updateProperty('content_meta_type', info['id'])
            type_info._updateProperty('content_icon', '%s.png' % info['id'])
            type_info._updateProperty('immediate_view',
                                      '%s_edit' % info['id'])
        else:
            type_info = types_tool._getOb(type_id)

        if is_old:
            type_info.manage_changeProperties(**info)
        else:
            for prop_info in info['properties']:
                tic.initProperty(type_info, prop_info)

        if 'actions' in info:
            type_info._actions = info['actions']

        if 'aliases' in info:
            if not getattr(type_info, '_aliases', False):
                aliases = info['aliases']
            else:
                aliases = type_info.getMethodAliases()
                aliases.update(info['aliases'])
            type_info.setMethodAliases(aliases)

    # XXX: YAGNI?
    # importScriptsToContainer(types_tool, ('typestool_scripts',),
    #                          context)

    return 'Types tool imported.'

def exportTypesTool( context ):

    """ Export types tool content types as a set of XML files.
    """
    site = context.getSite()
    types_tool = getToolByName( site, 'portal_types' )

    ttc = TypesToolConfigurator( site ).__of__( site )
    tic = TypeInfoConfigurator( site ).__of__( site )

    tool_xml = ttc.generateXML()
    context.writeDataFile( _TOOL_FILENAME, tool_xml, 'text/xml' )

    for type_id in types_tool.listContentTypes():

        type_filename = '%s.xml' % type_id.replace( ' ', '_' )
        type_xml = tic.generateXML( type_id=type_id )
        context.writeDataFile( type_filename
                             , type_xml
                             , 'text/xml'
                             , 'types'
                             )

    # XXX: YAGNI?
    # exportScriptsFromContainer(types_tool, ('typestool_scripts',))

    return 'Types tool exported'


class TypesToolConfigurator(ConfiguratorBase):

    security = ClassSecurityInfo()

    def _getImportMapping(self):

        return {
          'types-tool':
            { 'type':     {KEY: 'types', DEFAULT: (),
                           CONVERTER: self._convertTypes} },
          'type':
            { 'id':       {},
              'filename': {DEFAULT: '%(id)s'} } }

    def _convertTypes(self, val):

        for type in val:
            if type['filename'] == type['id']:
                type['filename'] = _getTypeFilename( type['filename'] )

        return val

    security.declareProtected( ManagePortal, 'listTypeInfo' )
    def listTypeInfo( self ):

        """ Return a list of mappings for each type info in the site.

        o These mappings are pretty much equivalent to the stock
          'factory_type_information' elements used everywhere in the
          CMF.
        """
        result = []
        typestool = getToolByName( self._site, 'portal_types' )

        type_ids = typestool.listContentTypes()

        for type_id in type_ids:
            info = {'id': type_id}

            if ' ' in type_id:
                info['filename'] = _getTypeFilename(type_id)

            result.append(info)

        return result

    def _getExportTemplate(self):

        return PageTemplateFile('ticToolExport.xml', _xmldir)

InitializeClass(TypesToolConfigurator)



# BBB: will be removed in CMF 1.6
class OldTypeInfoConfigurator(ConfiguratorBase):

    def _getImportMapping(self):

        return {
          'type-info':
            { 'id':                   {},
              'kind':                 {},
              'title':                {},
              'description':          {CONVERTER: self._convertToUnique},
              'meta_type':            {KEY: 'content_meta_type'},
              'icon':                 {KEY: 'content_icon'},
              'immediate_view':       {},
              'global_allow':         {CONVERTER: self._convertToBoolean},
              'filter_content_types': {CONVERTER: self._convertToBoolean},
              'allowed_content_type': {KEY: 'allowed_content_types'},
              'allow_discussion':     {CONVERTER: self._convertToBoolean},
              'aliases':              {CONVERTER: self._convertAliases},
              'action':               {KEY: 'actions'},
              'product':              {},
              'factory':              {},
              'constructor_path':     {},
              'permission':           {} },
          'allowed_content_type':
            { '#text':                {KEY: None} },
          'aliases':
            { 'alias':                {KEY: None} },
          'alias':
            { 'from':                 {},
              'to':                   {} },
          'action':
            { 'action_id':            {KEY: 'id'},
              'title':                {},
              'description':          {CONVERTER: self._convertToUnique},
              'category':             {},
              'condition_expr':       {KEY: 'condition'},
              'permission':           {KEY: 'permissions', DEFAULT: ()},
              'visible':              {CONVERTER: self._convertToBoolean},
              'url_expr':             {KEY: 'action'} },
          'permission':
            { '#text':                {KEY: None} } }

    def _convertAliases(self, val):

        result = {}

        for alias in val[0]:
            result[ alias['from'] ] = alias['to']

        return result

    def _getExportTemplate(self):
        return None

InitializeClass(OldTypeInfoConfigurator)


class TypeInfoConfigurator(ConfiguratorBase):

    security = ClassSecurityInfo()

    def _getImportMapping(self):

        return {
          'type-info':
            { 'id':                   {},
              'kind':                 {},
              'aliases':              {CONVERTER: self._convertAliases},
              'action':               {KEY: 'actions'},
              'property':             {KEY: 'properties', DEFAULT: ()},
              },
          'aliases':
            { 'alias':                {KEY: None} },
          'alias':
            { 'from':                 {},
              'to':                   {} },
          'action':
            { 'action_id':            {KEY: 'id'},
              'title':                {},
              'description':          {CONVERTER: self._convertToUnique},
              'category':             {},
              'condition_expr':       {KEY: 'condition'},
              'permission':           {KEY: 'permissions', DEFAULT: ()},
              'visible':              {CONVERTER: self._convertToBoolean},
              'url_expr':             {KEY: 'action'} },
          'permission':
            { '#text':                {KEY: None} } }

    def _convertAliases(self, val):

        result = {}

        for alias in val[0]:
            result[ alias['from'] ] = alias['to']

        return result

    security.declareProtected( ManagePortal, 'getTypeInfo' )
    def getTypeInfo( self, type_id ):

        """ Return a mapping for the given type info in the site.

        o These mappings are pretty much equivalent to the stock
          'factory_type_information' elements used everywhere in the
          CMF.
        """
        ti = self._getTI(type_id)
        return self._makeTIMapping(ti)

    security.declarePrivate('_getTI' )
    def _getTI(self, type_id):
        """Get the TI from its id."""
        typestool = getToolByName(self._site, 'portal_types')
        try:
            return typestool.getTypeInfo(str(type_id)) # gTI expects ASCII?
        except KeyError:
            raise ValueError("Unknown type: %s" % type_id)

    security.declarePrivate( '_makeTIMapping' )
    def _makeTIMapping( self, ti ):

        """ Convert a TypeInformation object into the appropriate mapping.
        """
        return {
            'id': ti.getId(),
            'kind': ti.meta_type,
            'aliases': ti.getMethodAliases(),
            'actions': [ai.getMapping() for ai in ti.listActions()],
            }

    security.declareProtected(ManagePortal, 'generateProperties')
    def generateProperties(self, type_id):
        """Get a sequence of mappings for properties."""
        ti = self._getTI(type_id)
        prop_infos = [self._extractProperty(ti, prop_map)
                      for prop_map in ti._propertyMap()]
        return self.generatePropertyNodes(prop_infos)

    def _getExportTemplate(self):

        return PageTemplateFile('ticTypeExport.xml', _xmldir)

InitializeClass(TypeInfoConfigurator)


def _getTypeFilename( type_id ):

    """ Return the name of the file which holds info for a given type.
    """
    return 'types/%s.xml' % type_id.replace( ' ', '_' )
