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

from Products.CPSInstaller.CPSInstaller import CPSInstaller, CMFInstaller

SECTIONS_ID = 'sections'
WORKSPACES_ID = 'workspaces'
CPS_SKINS = { 'cps_document': 'Products/CPSDocument/skins/cps_document',
              'cps_document_images':
              'Products/CPSDocument/skins/cps_document_images'}
CMF_SKINS = { 'cps_document': 'Products/CPSDocument/skins/cps_document_cmf',
              'cps_utils_cmf': 'Products/CPSDocument/skins/cps_utils_cmf',
              'cps_document_images':
              'Products/CPSDocument/skins/cps_document_images'}


class DocInstaller(CPSInstaller):
    product_name = 'CPSDocument'

    def install(self):
        self.log("Starting CPSDocument install")
        self.verifySkins(CPS_SKINS)
        # This installer calls skins later, so we need to reset the skins now.
        self.resetSkinCache()
        self.installCPSSchemas()
        self.installDocumentSchemas()
        self.setupPortalTypes()
        self.checkLinkBackwardCompatibility()
        self.updateWorkflowAssociations()
        self.setupTranslations()
        self.finalize()
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
        self.verifyFlexibleTypes(self.flextypes)
        types = self.newptypes[:]
        types.remove('Section')
        self.allowContentTypes(types, 'Workspace')
        self.updatePortalTree()

    def updateWorkflowAssociations(self):
        # check workflow association
        ws_chain = {}
        se_chain = {}
        for ptype in self.newptypes:
            ws_chain[ptype] = 'workspace_content_wf'
            se_chain[ptype] = 'section_content_wf'
        for ptype in self.newptypes:
            wf = self.flextypes[ptype].get('cps_workspace_wf',
                                           'workspace_content_wf')
            ws_chain[ptype] = wf
            wf = self.flextypes[ptype].get('cps_section_wf',
                                           'section_content_wf')
            se_chain[ptype] = wf
        self.verifyLocalWorkflowChains(self.portal[WORKSPACES_ID], ws_chain)
        self.verifyLocalWorkflowChains(self.portal[SECTIONS_ID], se_chain)

    def updatePortalTree(self):
        # register folderish document types in portal_tree
        self.log("Registering folderish document types in portal_tree")
        self.verifyTreeCacheTypes(WORKSPACES_ID,
                                  ['FAQ', 'ImageGallery', 'Glossary', 'Book', 'Chapter'])
        self.verifyTreeCacheTypes(SECTIONS_ID,
                                  ['FAQ', 'ImageGallery', 'Glossary', 'Book', 'Chapter'])

    def checkLinkBackwardCompatibility(self):
        # now Link document use Metadata Relation to store href
        # previous definition use a deprecated href attribute
        self.log("Checking Backward Compatibility for Link Document")
        do_check = 0
        try:
            if 'link' in self.portal.portal_types['Link'].schemas and \
                   self.portal.portal_schemas['link']['href']:
                do_check = 1
        except AttributeError:
            pass

        if not do_check:
            self.log("  not needed.")
            return

        query = {}
        root = self.portal.portal_url.getPortalPath()
        query['path'] = root + '/portal_repository/'
        query['portal_type'] = ['Link']
        self.log("  Searching for %s" % str(query))
        for brain in self.portal.portal_catalog(**query):
            ob = brain.getObject()
            if hasattr(ob, 'href'):
                href = getattr(ob, 'href')
                if href and not getattr(ob, 'Relation', None):
                    setattr(ob, 'Relation', href)
                    self.log("  Setting Relation = href for doc %s" % \
                                ob.getId())

    def installDocumentSchemas(self):
        self.verifyWidgets(self.portal.getDocumentWidgets())
        self.verifySchemas(self.portal.getDocumentSchemas())
        self.verifyLayouts(self.portal.getDocumentLayouts())
        self.verifyVocabularies(self.portal.getDocumentVocabularies())

class CMFInstaller(DocInstaller):
    product_name = 'CPSDocument'

    def install(self):
        self.log("Starting CPSDocument install")
        self.verifySkins(CMF_SKINS)
        # This installer calls skins later, so we need to reset the skins now.
        self.resetSkinCache()
        self.setupLocalizer()
        self.installCPSSchemas()
        self.installDocumentSchemas()
        self.setupPortalTypes()
        self.checkLinkBackwardCompatibility()
        self.setupTranslations()
        self.finalize()
        self.log("End of specific CPSDocument install")

    def setupPortalTypes(self):
        # setup portal_types
        self.log("Verifying portal types")
        self.flextypes = self.portal.getDocumentTypes()

        # Rely on CPSDefault
        del self.flextypes['Section']
        del self.flextypes['Workspace']
        self.newptypes = self.flextypes.keys()
        self.ttool = self.portal.portal_types
        self.verifyFlexibleTypes(self.flextypes)

    def installDocumentSchemas(self):
        self.verifyWidgets(self.portal.getDocumentWidgets())
        self.verifySchemas(self.portal.getDocumentSchemas())
        self.verifyLayouts(self.portal.getDocumentLayouts())
        self.verifyVocabularies(self.portal.getDocumentVocabularies())

    def setupLocalizer(self):
        # Localizer
        if not self.portalHas('Localizer'):
            self.log(" Adding Localizer ")
            languages = ('en',)
            self.portal.manage_addProduct['Localizer'].manage_addLocalizer(
                title='',
                languages=languages)
        self.verifyMessageCatalog('default','Default messages')

        # translation_service
        if not self.portalHas('translation_service'):
            self.portal.manage_addProduct['TranslationService'].\
                addPlacefulTranslationService(id='translation_service')
            self.log("  translation_service tool added")
            translation_service = self.portal.translation_service
            translation_service.manage_setDomainInfo(path_0='Localizer/default')
            self.log("   default domain set to Localizer/default")


###########################################################
###########################################################

def cpsinstall(self):
    installer = DocInstaller(self)
    installer.install()
    return installer.logResult()

def cmfinstall(self):
    installer = CMFInstaller(self)
    installer.install()
    return installer.logResult()

def install(self):
    """Dispatch to the good installer
    CMF / CPS
    """
    is_cps3 = 0
    try:
        from Products.CPSDefault.Portal import CPSDefaultSite
        is_cps3 = 1
    except ImportError:
        pass

    if is_cps3:
        return cpsinstall(self)
    else:
        return cmfinstall(self)
