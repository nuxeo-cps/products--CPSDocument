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

def install(self):

    _log = []
    def pr(bla, zlog=1, _log=_log):
        if bla == 'flush':
            return '<html><head><title>CPSDocument Update</title></head><body><pre>'+ \
                   '\n'.join(_log) + \
                   '</pre></body></html>'

        _log.append(bla)
        if (bla and zlog):
            LOG('CPSDocument install:', INFO, bla)

    def prok(pr=pr):
        pr(" Already correctly installed")

    pr("Starting CPSDocument install")

    portal = self.portal_url.getPortalObject()

    def portalhas(id, portal=portal):
        return id in portal.objectIds()


    # skins
    skins = ('cps_document',)
    paths = {
        'cps_document': 'Products/CPSDocument/skins/cps_document',
    }
    skin_installed = 0
    for skin in skins:
        path = paths[skin]
        path = path.replace('/', os.sep)
        pr(" FS Directory View '%s'" % skin)
        if skin in portal.portal_skins.objectIds():
            dv = portal.portal_skins[skin]
            oldpath = dv.getDirPath()
            if oldpath == path:
                prok()
            else:
                pr("  Correctly installed, correcting path")
                dv.manage_properties(dirpath=path)
        else:
            skin_installed = 1
            portal.portal_skins.manage_addProduct['CMFCore'].manage_addDirectoryView(filepath=path, id=skin)
            pr("  Creating skin")
    if skin_installed:
        allskins = portal.portal_skins.getSkinPaths()
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
            portal.portal_skins.addSkinSelection(skin_name, npath)
            pr(" Fixup of skin %s" % skin_name)
        pr(" Resetting skin cache")
        portal._v_skindata = None
        portal.setupCurrentSkin()

    # call cpsschemas install
    from Products.CPSSchemas.Extensions.install import install as \
         cpschemas_install
    res = cpschemas_install(self)
    pr(res)

    # setup portal_type
    pr("Verifying portal types")
    flextypes = self.getDocumentTypes()
    newptypes = flextypes.keys()
    ttool = portal.portal_types
    if 'Workspace' in ttool.objectIds():
        workspaceACT = list(ttool['Workspace'].allowed_content_types)
    else:
        raise "DependanceError", 'Workspace'
    for ptype in newptypes:
        if ptype not in  workspaceACT:
            workspaceACT.append(ptype)

    allowed_content_type = {
                            'Workspace' : workspaceACT,
                            }

    ttool['Workspace'].allowed_content_types = allowed_content_type['Workspace']

    ptypes_installed = ttool.objectIds()
    display_in_cmf_calendar = []
    for ptype, data in flextypes.items():
        pr("  Type '%s'" % ptype)
        if ptype in ptypes_installed:
            ttool.manage_delObjects([ptype])
            pr("   Deleted")
        ti = ttool.addFlexibleTypeInformation(id=ptype)
        if data.get('display_in_cmf_calendar'):
            display_in_cmf_calendar.append(ptype)
            del data['display_in_cmf_calendar']
        ti.manage_changeProperties(**data)
        pr("   Installation")

    # register ptypes to portal_calendar
    if len(display_in_cmf_calendar):
        portal.portal_calendar.calendar_types = display_in_cmf_calendar

    # check site and workspaces proxies
    sections_id = 'sections'
    workspaces_id = 'workspaces'

    # register folderish document types in portal_tree
    pr("Registering folderish document types in portal_tree")
    trtool = portal.portal_trees
    trtool[workspaces_id].manage_changeProperties(
        type_names=list(trtool[workspaces_id].type_names) + ['FAQ',]
        )
    trtool[sections_id].manage_rebuild()
    trtool[sections_id].manage_changeProperties(
        type_names=list(trtool[sections_id].type_names) + ['FAQ',]
        )
    trtool[sections_id].manage_rebuild()

    # check workflow association
    pr("Verifying local workflow association")
    if not '.cps_workflow_configuration' in portal[workspaces_id].objectIds():
        raise "DependanceError", 'no .cps_workflow_configuration in Workspace'
    else:
        wfc = getattr(portal[workspaces_id], '.cps_workflow_configuration')

    for ptype in newptypes:
        if 'cps_workspace_wf' in flextypes[ptype].keys():
            wwf = flextypes[ptype]['cps_workspace_wf']
        else:
            wwf = 'workspace_content_wf'
        pr("  Add %s chain to portal type %s in %s of %s" %(wwf,
             ptype, '.cps_workflow_configuration', workspaces_id))
        wfc.manage_addChain(portal_type=ptype, chain=wwf)

    if not '.cps_workflow_configuration' in portal[sections_id].objectIds():
        raise "DependanceError", 'no .cps_workflow_configuration in Section'
    else:
        wfc = getattr(portal[sections_id], '.cps_workflow_configuration')

    for ptype in newptypes:
        pr("  Add %s chain to portal type %s in %s of %s" %('section_content_wf',
             ptype, '.cps_workflow_configuration', sections_id))
        wfc.manage_addChain(portal_type=ptype,
                            chain='section_content_wf')

    # importing .po files
    mcat = portal['Localizer']['default']
    pr(" Checking available languages")
    podir = os.path.join('Products', 'CPSDocument')
    popath = getPath(podir, 'i18n')
    if popath is None:
        pr(" !!! Unable to find .po dir")
    else:
        pr("  Checking installable languages")
        langs = []
        avail_langs = mcat.get_languages()
        pr("    Available languages: %s" % str(avail_langs))
        for file in os.listdir(popath):
            if file.endswith('.po'):
                m = match('^.*([a-z][a-z])\.po$', file)
                if m is None:
                    pr( '    Skipping bad file %s' % file)
                    continue
                lang = m.group(1)
                if lang in avail_langs:
                    lang_po_path = os.path.join(popath, file)
                    lang_file = open(lang_po_path)
                    pr("    Importing %s into '%s' locale" % (file, lang))
                    mcat.manage_import(lang, lang_file)
                else:
                    pr( '    Skipping not installed locale for file %s' % file)


    pr("End of specific CPSDocument install")
    return pr('flush')
