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

# to use CPSDocument in your product add the following line in your setup:
#     #  CPSDocument installer/updater
#     #
#     if not portalhas('cpsdocument_installer'):
#         from Products.ExternalMethod.ExternalMethod import ExternalMethod
#         pr('Adding cpsdocument installer')
#         cpsdocument_installer = ExternalMethod('cpsdocument_installer',
#                                       'CPSDocument Updater',
#                                       'CPSDocument.install',
#                                       'install')
#         portal._setObject('cpsdocument_installer', cpsdocument_installer)
#     pr(portal.cpsdocument_installer())

import os
from App.Extensions import getPath
from re import match

from Products.CPSDefault.Installer import BaseInstaller

SECTIONS_ID = 'sections'
WORKSPACES_ID = 'workspaces'
SKINS = (
    ('cps_document', 'Products/CPSDocument/skins/cps_document'),
)

class CPSInstaller(BaseInstaller):
    product_name = 'CPSDocument'

    def install(self):
        self.log("Starting CPSDocument install")
        self.setupSkins(SKINS)
        self.installCPSSchemas()
        self.setupPortalTypes()
        self.setupTranslations()
        self.log("End of specific CPSDocument install")


    #
    # These methods do the actual work
    #
    def installCPSSchemas(self):
        # call cpsschemas install
        from Products.CPSSchemas.Extensions.install import install as \
             cpschemas_install
        res = cpschemas_install(self.context)
        self.log(res)

    def setupPortalTypes(self):
        # setup portal_types
        self.log("Verifying portal types")
        self.flextypes = self.portal.getDocumentTypes()
        self.newptypes = self.flextypes.keys()
        self.ttool = self.portal.portal_types

        self.allowTypesInWorkspaces()
        self.registerTypes()
        self.updatePortalTree()
        self.updateWorkflowAssociations()

    def allowTypesInWorkspaces(self):
        if 'Workspace' in self.ttool.objectIds():
            workspace_act = list(self.ttool['Workspace'].allowed_content_types)
        else:
            raise "DependanceError", 'Workspace'
        for ptype in self.newptypes:
            if ptype not in workspace_act:
                workspace_act.append(ptype)
        self.ttool['Workspace'].allowed_content_types = workspace_act

    def registerTypes(self):
        ptypes_installed = self.ttool.objectIds()
        display_in_cmf_calendar = []
        for ptype, data in self.flextypes.items():
            self.log("  Type '%s'" % ptype)
            if ptype in ptypes_installed:
                self.ttool.manage_delObjects([ptype])
                self.log("   Deleted")
            ti = self.ttool.addFlexibleTypeInformation(id=ptype)
            if data.get('display_in_cmf_calendar'):
                display_in_cmf_calendar.append(ptype)
                del data['display_in_cmf_calendar']
            ti.manage_changeProperties(**data)
            self.log("   Installation")

        # register ptypes to portal_calendar
        if display_in_cmf_calendar and hasattr(self.portal, 'portal_calendar'):
            self.portal.portal_calendar.calendar_types = display_in_cmf_calendar

    def updateWorkflowAssociations(self):
        # check workflow association
        self.log("Verifying local workflow association")

        sections = self.portal[SECTIONS_ID]
        workspaces = self.portal[WORKSPACES_ID]

        if not '.cps_workflow_configuration' in workspaces.objectIds():
            raise "DependanceError", 'no .cps_workflow_configuration in Workspace'
        else:
            wfc = getattr(workspaces, '.cps_workflow_configuration')

        for ptype in self.newptypes:
            if 'cps_workspace_wf' in self.flextypes[ptype].keys():
                wwf = self.flextypes[ptype]['cps_workspace_wf']
            else:
                wwf = 'workspace_content_wf'
            self.log("  Add %s chain to portal type %s in %s of %s" % (
                wwf, ptype, '.cps_workflow_configuration', WORKSPACES_ID))
            wfc.manage_addChain(portal_type=ptype, chain=wwf)

        if not '.cps_workflow_configuration' in sections.objectIds():
            raise "DependanceError", 'no .cps_workflow_configuration in Section'
        else:
            wfc = getattr(sections, '.cps_workflow_configuration')

        for ptype in self.newptypes:
            self.log("  Add %s chain to portal type %s in %s of %s" % (
                'section_content_wf', ptype, '.cps_workflow_configuration',
                SECTIONS_ID))
            wfc.manage_addChain(portal_type=ptype,
                                chain='section_content_wf')

    def updatePortalTree(self):
        # register folderish document types in portal_tree
        self.log("Registering folderish document types in portal_tree")
        trtool = self.portal.portal_trees
        trtool[WORKSPACES_ID].manage_changeProperties(
            type_names=list(trtool[WORKSPACES_ID].type_names) 
                + ['FAQ', 'ImageGallery', 'Glossary'])
        trtool[WORKSPACES_ID].manage_rebuild()
        trtool[SECTIONS_ID].manage_changeProperties(
            type_names=list(trtool[SECTIONS_ID].type_names) 
                + ['FAQ', 'ImageGallery', 'Glossary'])
        trtool[SECTIONS_ID].manage_rebuild()


class CMFInstaller(CPSInstaller):
    def setupPortalTypes(self):
        # setup portal_types
        self.log("Verifying portal types")
        self.flextypes = self.portal.getDocumentTypes()
        self.newptypes = self.flextypes.keys()
        self.ttool = self.portal.portal_types

        #self.allowTypesInWorkspaces()
        self.registerTypes()
        #self.updatePortalTree()
        #self.updateWorkflowAssociations()


def install(self):
    installer = CPSInstaller(self)
    installer.install()
    return installer.logResult()

def cmfinstall(self):
    installer = CMFInstaller(self)
    installer.install()
    return installer.logResult()

