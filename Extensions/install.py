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
from zLOG import LOG, INFO, DEBUG

SECTIONS_ID = 'sections'
WORKSPACES_ID = 'workspaces'

class Installer:
    def __init__(self, context):
        self._log = []
        self.context = context
        self.portal = context.portal_url.getPortalObject()


    def install(self):
        self.log("Starting CPSDocument install")
        self.setupSkins()
        self.installCPSSchemas()
        self.setupPortalTypes()
        self.setupTranslations()
        self.log("End of specific CPSDocument install")

    #
    # Logging
    #
    def log(self, bla, zlog=1):
        self._log.append(bla)
        if (bla and zlog):
            LOG('CPSDocument install:', INFO, bla)

    def logOK(self):
        self.log(" Already correctly installed")

    def logResult(self):
        return '<html><head><title>CPSDocument Update</title></head>' \
            '<body><pre>'+ '\n'.join(self._log) + '</pre></body></html>'


    #
    # These methods do the actual work
    #
    # TODO: this is almost completely generic code, it should move to 
    # a superclass
    def setupSkins(self):
        # skins
        skins = ('cps_document',)
        paths = {
            'cps_document': 'Products/CPSDocument/skins/cps_document',
        }
        skin_installed = 0
        for skin in skins:
            path = paths[skin]
            path = path.replace('/', os.sep)
            self.log(" FS Directory View '%s'" % skin)
            if skin in self.portal.portal_skins.objectIds():
                dv = self.portal.portal_skins[skin]
                oldpath = dv.getDirPath()
                if oldpath == path:
                    self.logok()
                else:
                    self.log("  Correctly installed, correcting path")
                    dv.manage_properties(dirpath=path)
            else:
                skin_installed = 1
                self.portal.portal_skins.manage_addProduct['CMFCore'].manage_addDirectoryView(filepath=path, id=skin)
                self.log("  Creating skin")
        if skin_installed:
            allskins = self.portal.portal_skins.getSkinPaths()
            for skin_name, skin_path in allskins:
                if skin_name != 'Basic':
                    continue
                path = [x.strip() for x in skin_path.split(',')]
                path = [x for x in path if x not in skins] # strip all
                if path and path[0] == 'custom':
                    path = path[:1] + list(skins) + path[1:]
                else:
                    path = list(skins) + path
                npath = ', '.join(path)
                self.portal.portal_skins.addSkinSelection(skin_name, npath)
                self.log(" Fixup of skin %s" % skin_name)
            self.log(" Resetting skin cache")
            self.portal._v_skindata = None
            self.portal.setupCurrentSkin()

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
        if display_in_cmf_calendar:
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

    # TODO: this method is completely generic and should go to a superclass
    def setupTranslations(self):
        """Import .po files"""

        mcat = self.portal['Localizer']['default']
        self.log(" Checking available languages")
        podir = os.path.join('Products', 'CPSDocument')
        popath = getPath(podir, 'i18n')
        if popath is None:
            self.log(" !!! Unable to find .po dir")
        else:
            self.log("  Checking installable languages")
            langs = []
            avail_langs = mcat.get_languages()
            self.log("    Available languages: %s" % str(avail_langs))
            for file in os.listdir(popath):
                if file.endswith('.po'):
                    m = match('^.*([a-z][a-z])\.po$', file)
                    if m is None:
                        self.log('    Skipping bad file %s' % file)
                        continue
                    lang = m.group(1)
                    if lang in avail_langs:
                        lang_po_path = os.path.join(popath, file)
                        lang_file = open(lang_po_path)
                        self.log("    Importing %s into '%s' locale" % (file, lang))
                        mcat.manage_import(lang, lang_file)
                    else:
                        self.log('    Skipping not installed locale for file %s' % file)

class CMFInstaller(Installer):
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
    installer = Installer(self)
    installer.install()
    return installer.logResult()

def cmfinstall(self):
    installer = Installer(self)
    installer.install()
    return installer.logResult()

