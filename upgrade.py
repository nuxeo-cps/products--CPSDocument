# Copyright 2005-2007 Nuxeo SAS <http://nuxeo.com>
# Author: Julien Anguenot <ja@nuxeo.com>
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

import logging
import re

import transaction
from Acquisition import aq_base, aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CPSUtil.text import upgrade_string_unicode
from Products.CPSUtil.file import ofsFileHandler
from Products.CPSUtil.image import imageGeometry

from Products.CPSSchemas.BasicFields import CPSStringField
from Products.CPSSchemas.BasicWidgets import CPSIntWidget
from Products.CPSSchemas.widgets.image import CPSImageWidget
from Products.CPSSchemas.widgets.image import CPSPhotoWidget
from Products.CPSSchemas.upgrade import upgrade_datamodel_unicode
from Products.CPSDocument.FlexibleTypeInformation import flexible_widget_split

import itertools

_marker = object()

def upgrade_334_335_allowct_sections(context):
    ttool = getToolByName(context, 'portal_types')
    section = ttool['Section']
    flextypes = context.getDocumentTypes()
    allowed_in = flextypes.keys()
    for ptype in allowed_in:
        sectionACT = list(section.allowed_content_types)
        if ptype not in  sectionACT:
            sectionACT.append(ptype)
            section.allowed_content_types = sectionACT
    return "CPSDocument updated: Sections allow content types"

def upgrade_335_336_fix_broken_flexible(context):
    """Fix broken flexible attachement fields

    The _objects attribute of docs with flexible content might be broken
    because of the use of the 'delattr' function instead of
    'manage_delObjects' when deleting flexible fields.

    This is related to ticket #889.
    """
    repository = getToolByName(context, 'portal_repository')
    fixed_fields = 0
    for doc in repository.values():
        if getattr(doc, '_objects', None) is None:
            continue
        new_objects = []
        for ob in doc._objects:
            if getattr(aq_base(doc), ob['id'], None) is None:
                fixed_fields += 1
            else:
                new_objects.append(ob)
        doc._objects = tuple(new_objects)
    return "CPSDocument updated: fixed %d broken flexible fields" % fixed_fields

def upgrade_336_337_anim_flash(context):
    """Upgrade all Flash Animations.

    The field 'preview' that contains the file is moved to 'flash_file'.
    """
    repository = getToolByName(context, 'portal_repository')
    fixed_files = 0
    for doc in repository.values():
        bdoc = aq_base(doc)
        if getattr(bdoc, 'portal_type', None) == 'Flash Animation':
            preview = getattr(bdoc, 'preview', _marker)
            flash_file = getattr(bdoc, 'flash_file', _marker)
            if preview is not _marker and flash_file is _marker:
                if preview == None:
                    delattr(bdoc, 'preview')
                    bdoc.flash_file = None
                else:
                    doc.manage_renameObject('preview', 'flash_file')
                fixed_files += 1
    return "CPSDocument updated: fixed %d flash anims" % fixed_files

def check_338_340_document_to_flex(context):
    ttool = getToolByName(context, 'portal_types')
    if 'Document' not in ttool.objectIds():
        # No Document type to upgrade
        return False
    doc_type = ttool['Document']
    from FlexibleTypeInformation import FlexibleTypeInformation
    if doc_type.meta_type != FlexibleTypeInformation.meta_type:
        # This is CPS 3.2, and Document is not even Flexible.
        # Can't upgrade
        return False
    if 'flexible_content' in doc_type.schemas:
        # Alredy upgraded:
        return False
    return True

def upgrade_338_340_textimage_widgets(portal):
    logger = logging.getLogger('Products.CPSDocument.upgrades.'
                               'textimage_widgets')
    layout_ids = ('flexible_content',)

    def do_one(doc, widget, layout, template_widget, template_layout):
        wid = widget.getId()
        tpl_id = flexible_widget_split(wid)[0]
        if tpl_id != 'textimage':
            return
        logger.debug("Upgrading widget %r", widget)
        state = widget.__dict__.copy()
        state.pop('widget_type', None)
        layout.delSubObject(wid)
        layout.add(TextImageWidget(wid))
        layout[wid].__dict__.update(state)
        return True

    do_on_flexible_widgets(do_one, portal, layout_ids)
    logger.warn("Finished upgrading textimage widgets for layouts %r",
                ','.join(layout_ids))
    transaction.commit()


def upgrade_338_340_document_to_flex(context):
    """Upgrade Document type instances to become flexible."""
    repository = getToolByName(context, 'portal_repository')
    ttool = getToolByName(context, 'portal_types')

    doc_type = ttool['Document']
    schemas = list(doc_type.schemas)
    if 'document' in schemas:
        schemas.remove('document')
    if 'flexible_content' not in schemas:
        schemas.append('flexible_content')
    doc_type.schemas = tuple(schemas)

    layouts = list(doc_type.layouts)
    if 'document' in layouts:
        layouts.remove('document')
    if 'flexible_content' not in layouts:
        layouts.append('flexible_content')
    doc_type.layouts = tuple(layouts)

    doc_type.flexible_layouts = ('flexible_content:flexible_content',)

    count = 0
    for doc in repository.iterValues():
        if doc.portal_type != 'Document':
            continue
        bdoc = aq_base(doc)

        schemas = getattr(bdoc, '.cps_schemas', None)
        content = getattr(bdoc, 'content', None)
        content_position = getattr(bdoc, 'content_position', None)
        content_format = getattr(bdoc, 'content_format', None)

        if (schemas is not None
            and content is None
            and content_position is None
            and content_format is None
            ):
            continue

        doc.flexibleAddWidget('flexible_content', 'textimage')
        doc.content_f0 = content
        doc.content_f1 = content_position
        doc.content_f2 = content_format

        for attr in 'content', 'content_position', 'content_format':
            delattr(doc, attr)

        count += 1

    return 'CPSDocument updated: %d Document instances became flexible' % count

def check_338_340_newsitem_to_flex(context):
    ttool = getToolByName(context, 'portal_types')
    if 'News Item' not in ttool.objectIds():
        # No Document type to upgrade
        return False
    doc_type = ttool['News Item']
    from FlexibleTypeInformation import FlexibleTypeInformation
    if doc_type.meta_type != FlexibleTypeInformation.meta_type:
        # News item is not even a CPSDocument. That happens with 3.3.0.
        return False
    schemas = list(doc_type.schemas)
    if 'news' in schemas:
        return True

    # Even if the doc_type is upgraded, we might need to upgrade documents
    catalog = getToolByName(context, 'portal_catalog')
    brains = catalog.searchResults(portal_type='News Item')
    # Let's just test the first one, so the checker doesn't get very slow.
    if len(brains) == 0:
        return False

    ob = brains[0].getObject()
    if getattr(ob, 'attachedFile', _marker) is _marker:
        return False

    return True

def upgrade_338_340_newsitem_to_flex(context):
    """Upgrade News Item type instances to become flexible."""
    repository = getToolByName(context, 'portal_repository')
    ttool = getToolByName(context, 'portal_types')

    doc_type = ttool['News Item']
    schemas = list(doc_type.schemas)
    if 'news' in schemas:
        schemas.remove('news')
        schemas.append('newsitem')
        doc_type.schemas = tuple(schemas)

    layouts = list(doc_type.layouts)
    if 'news' in layouts:
        layouts.remove('news')
        layouts.append('newsitem_start')
        layouts.append('newsitem_flexible')
        layouts.append('newsitem_end')
        doc_type.layouts = tuple(layouts)

    doc_type.flexible_layouts = ('newsitem_flexible:flexible_content',)

    pfilter = lambda o: getattr(o, 'portal_type', '') == 'News Item'
    docs = itertools.ifilter(pfilter, repository.values())
    count = 0
    for doc in docs:
        bdoc = aq_base(doc)

        schemas = getattr(bdoc, '.cps_schemas', None)
        attachedFile = getattr(bdoc, 'attachedFile', None)
        attachedFile_text = getattr(bdoc, 'attachedFile_text', None)
        attachedFile_html = getattr(bdoc, 'attachedFile_html', None)

        if (schemas is not None
            and attachedFile is None
            and attachedFile_text is None
            and attachedFile_html is None
            ):
            continue

        doc.flexibleAddWidget('newsitem_flexible', 'attachedFile')
        kw = {'attachedFile_f0': attachedFile,
              'attachedFile_f1': attachedFile_text,
              'attachedFile_f2': attachedFile_html,
              }
        doc.edit(**kw)

        for attr in 'attachedFile', 'attachedFile_text', 'attachedFile_html':
            if getattr(doc, attr, _marker) is not _marker:
                delattr(doc, attr)

        count += 1

    return 'CPSDocument updated: %d Document instances became flexible' % count

def upgrade_unicode(portal, resync_trees=True):
    """Upgrade all documents to unicode.

    Takes care of frozen revisions without version bumps
    CPS String Field content will be cast to unicode, whereas
    CPS Ascii String Field content will be cast to str
    """

    logger = logging.getLogger('Products.CPSDocument.upgrades.unicode')
    repotool = portal.portal_repository
    total = len(repotool)

    done = 0
    for doc in repotool.iterValues():
        if not upgrade_doc_unicode(doc):
            logger.error("Could not upgrade document revision %s", doc)
            continue
        done += 1
        if done % 100 == 0:
            logger.info("Upgraded %d/%d document revisions", done, total)
            transaction.commit()

    logger.warn("Finished unicode upgrade of the %d/%d documents.", done, total)

    if not resync_trees:
        return

    logger.info("Rebuilding Tree Caches")
    trees = portal.portal_trees.objectValues('CPS Tree Cache')
    for tree in trees:
        logger.info("Rebuilding %s", tree)
        tree.rebuild()
        transaction.commit()
    logger.warn("Finished rebuilding the Tree Caches")

def do_on_flexible_widgets(meth, portal, layout_ids):
    """Apply meth to for all flexible widgets of given layout_ids in the portal.

    Details for meth:
      typically defined inside the primary handler function to benefit from
      its local variables.

      signature:
        def meth(doc, widget, layout, template_widget, template_layout)
      where template_widget is the global widget this one refers to

      meaning of returned values:
        - True if has run successfully
        - False if some error has occurred
        - None if has not been applicable, and this is not an error

    This looper is supposed to understand both IndirectWidget cases and
    the older copy-pasted flexible widgets.
    """

    logger = logging.getLogger('Products.CPSDocument.upgrades.'
                               'do_on_flexible_widgets')
    repotool = portal.portal_repository
    total = len(repotool)

    ltool = portal.portal_layouts
    layouts = {}
    for lid in layout_ids:
        try:
            layouts[lid] = ltool[lid]
        except KeyError:
            logger.warn("Global layout %r not found", lid)

    done = 0
    for doc in repotool.iterValues():
        ret = do_on_flex_widgets_doc(meth, doc, layouts, logger)
        if ret is None: # means was not applicable, but ok
            continue

        if not ret:
            logger.error("Could not upgrade document revision %s", doc)
            continue

        done += 1
        if done % 100 == 0:
            logger.info("Upgraded %d/%d document revisions", done, total)
            transaction.commit()

    logger.warn("Finished resyncing flexible widgets for layouts %r "
                "of the %d/%d documents.", layout_ids, done, total)

    transaction.commit()

def do_on_flex_widgets_doc(meth, doc, layouts, logger):

    if not doc.hasObject('.cps_layouts'):
        return
    lcont = doc['.cps_layouts']
    loc_lids = lcont.objectIds()
    status = True
    for lid, glob in layouts.items():
        if not lid in loc_lids:
            continue

        loc = lcont[lid]

        for wid, w in loc.items():
            if wid in glob.keys():
                gw = glob[wid]
            else:
                split = flexible_widget_split(wid)
                try:
                    gw = glob[split[0]]
                except KeyError:
                    logger.warn("Could not find template widget for %s",
                                w.absolute_url_path())
                    status = False
                    continue

            ret = meth(doc, w, loc, gw, glob)
            if ret is None:
                status is None
            elif status is not None:
                status = status and ret

    return status


def resync_flexible_widgets(portal, wid_props=None):
    """Upgrade flexible widgets by recopying properties from the master ones.

    wid_props is a double dict
       (layout_id -> (template widget id -> property ids))
    """

    logger = logging.getLogger('Products.CPSDocument.upgrades.'
                               'resync_flexible_widgets')
    layout_ids = wid_props.keys()
    logger.info("Starting resync of flexible widgets for layouts %r \n"
                "detailed parameters: %r", layout_ids, wid_props)

    def do_one(doc, widget, layout, template_widget, template_layout):
        props = wid_props.get(layout.getId())
        for pid in props.get(template_widget.getWidgetId(), ()):
            widget.manage_changeProperties(
                **{pid: template_widget.getProperty(pid)})
        return True

    do_on_flexible_widgets(do_one, portal, layout_ids)
    logger.warn("Finished resyncing flexible widgets for layouts %r",
                ','.join(layout_ids))
    transaction.commit()

def upgrade_doc_unicode(doc):
        ptype = doc.portal_type

        logger = logging.getLogger('Products.CPSDocument.upgrades.doc_unicode')
        # Going through DataModel for uniformity (DublinCore etc)
        if doc.hasObject('.cps_schemas'):
            # we may have String fields to upgrade so that they validate None
            for sch in doc['.cps_schemas'].objectValues(['CPS Schema']):
                for ffield in sch.objectValues(['CPS File Field']):
                    suffix = ffield.suffix_text
                    if not suffix:
                        continue
                    try:
                        tfield = sch[ffield._getDependantFieldsBaseId()+suffix]
                    except KeyError, AtrributeError:
                        logger.warn("Could not find the text alternative field"
                                    "for %s", ffield.absolute_url_path())
                        continue

                    if not isinstance(tfield, CPSStringField):
                        logger.warn("Should have been a CPS String Field: %s",
                                    field.absolute_url_path())
                        continue
                    tfield.validate_none = True
                    logger.info("Upgraded text alternative field at %s",
                                tfield.absolute_url_path())

        try:
            dm = doc.getDataModel()
        except ValueError:
            # if due to lack of FTI, already logged
            return False

        return upgrade_datamodel_unicode(dm)

def upgrade_text_widgets_tidy(portal):
    """This should be played after running the profiles."""
    resync_flexible_widgets(portal, wid_props=dict(
        flexible_content=dict(content=('xhtml_sanitize_system',),
                              content_right=('xhtml_sanitize_system',))
        ))

def upgrade_image_gallery_unidim_thumbnails(portal):
    """This should be played after running the profiles."""
    logger = logging.getLogger(
        'Products.CPSDocument.upgrades.image_gallery_unidim_thumbnails')
    logger.info("Starting.")
    done = seen = 0

    def commit_log(counter):
        logger.info(
            "Went through %d docs, upgraded %d over %d image galleries",
            c+1, done, seen)
        transaction.commit()


    repotool = portal.portal_repository
    for c, doc in enumerate(repotool.iterValues()):
        if doc.portal_type != "ImageGallery":
            continue
        seen += 1
        try:
            doc_b = aq_base(doc)
            size = max(getattr(doc_b, 'preview_height', 0),
                       getattr(doc_b, 'preview_width', 0))
            if size: # otherwise there'll be field default value
                doc.thumbnail_size = size
            done += 1
        except ConflictError:
            raise
        except:
            logger.exception("Could not upgrade Image Gallery at %s",
                             doc.absolute_url_path())
        if c and not (c % 100):
            commit_log(c)
    commit_log(c)

# downstream welcome to add more
FLEXIBLE_LAYOUTS = ['flexible_content', 'newsitem_flexible']
FLEXIBLE_LAYOUTS_SIZE_WIDGETS = dict(flexible_content=('display_size',),
                                     newsitem_flexible=('display_size',))

def upgrade_flexible_widgets_indirect(portal):
    """Upgrade all flexible documents to use IndirectWidget."""
    from Products.CPSSchemas.widgets.indirect import IndirectWidget
    utool = portal.portal_url

    def do_one(doc, widget, layout, template_widget, template_layout):
        fields = widget.fields
        subwidgets = widget.getProperty('widget_ids', None)

        layout = aq_parent(aq_inner(widget))
        wid = widget.getWidgetId()
        layout.delSubObject(wid)
        layout.addSubObject(IndirectWidget(wid))
        indirect = layout[wid]

        rpath = utool.getRpath(template_widget)
        indirect.manage_changeProperties(base_widget_rpath=rpath)
        indirect.manage_addProperty('fields', fields, 'lines')
        if subwidgets is not None:
            indirect.manage_addProperty('widget_ids', subwidgets, 'lines')
        return True

    do_on_flexible_widgets(do_one, portal, FLEXIBLE_LAYOUTS)

def make_size_widget(layout, subwid, **kw):
    """Make a subwidget to control sizes and return it.

    Can be used either to upgrade flexible layouts or for the global ones.
    kw gets applied as properties on the widget.
    """
    layout.addSubObject(CPSIntWidget(subwid))
    size_widget = layout[subwid]
    kw.setdefault('label_edit', 'cpsdoc_image_display_size_largest_label_edit')
    kw.setdefault('help', 'cpsdoc_image_display_size_help')
    size_widget.manage_changeProperties(**kw)
    return size_widget

def upgrade_image_widget(doc, widget, layout, template_widget, template_layout):
    wid = widget.getWidgetId()

    # keeping interesting part of attrs
    state = widget.__dict__.copy()
    stprops = state.pop('_properties', ())
    if stprops:
        oldclsprops = frozenset(p['id'] for p in widget.__class__._properties)
        addprops = tuple(p for p in stprops if p['id'] not in oldclsprops)
    size = max(state.pop('display_width', 0), state.pop('display_height', 0))
    allow_resize = state.pop('allow_resize', widget.__class__.allow_resize)

    # instantiation and state init
    layout.delSubObject(wid)
    layout.addSubObject(CPSImageWidget(wid))
    widget = layout[wid]
    widget.__dict__.update(state)
    if stprops:
        widget._properties = CPSImageWidget._properties + addprops
    widget.size_spec = 'l%d' % size

    suffix = flexible_widget_split(wid)[1]

    if allow_resize:
        # user has had the opportunity to resize, we make a subwidget.
        # we try and have the same suffix as the main one, to stay
        # human-readers friendly
        fti = doc.getTypeInfo()
        _, schema = fti._getFlexibleLayoutAndSchemaFor(doc, layout.getId())

        base_id = 'display_size'
        if suffix:
            subwid = '_'.join((base_id, suffix))
        else:
            subwid = base_id
        # TODO: what if hundreds of flex widgets. Seen that in the wild
        c = ord('A')
        while subwid in layout.keys():
            subwid = '_'.join((base_id, chr(c), suffix))
            c += 1

        widget.widget_ids = (subwid,)
        size_widget = make_size_widget(layout, subwid)

        tpl_widget = CPSIntWidget('tpl') # for now, that's enough, this is
        # used for field inits, which are in this case ok at class level
        fti._createFieldsForFlexibleWidget(schema, size_widget, tpl_widget)

        dm = doc.getDataModel()
        img = dm[widget.fields[0]]
        if img is not None:
            subfid = size_widget.fields[0]
            dm[subfid] = max(*imageGeometry(ofsFileHandler(img)))
            dm._commitData()

def upgrade_photo_widget(doc, widget, layout, template_widget, template_layout):
    has_original = widget.canKeepOriginal()
    if has_original:
        fields = widget.fields
        original_fid = fields[3]
        dm = doc.getDataModel()
        original = dm[original_fid]

    upgrade_image_widget(doc, widget, layout, template_widget, template_layout)
    widget = layout[widget.getWidgetId()]
    widget.fields = fields[:3] + fields[4:]

    if has_original:
        if original is not None:
            original = original._file_obj
            # main field now the original
            dm = doc.getDataModel()
            dm[fields[0]] = original
            dm._commitData()

        # resized version not stored in a field
        fti = doc.getTypeInfo()
        _, schema = fti._getFlexibleLayoutAndSchemaFor(doc, layout.getId())
        schema.delSubObject(original_fid)

        # Zoom size did not exist before.
        # In any case the later switch to Indirect Widget will take over it
        widget.manage_changeProperties(zoom_size_spec='l800')

def upgrade_image_widgets(portal):
    logger = logging.getLogger('Products.CPSDocument.upgrade.image_widgets')

    for layout_id, subwids in FLEXIBLE_LAYOUTS_SIZE_WIDGETS.items():
        layout = portal.portal_layouts[layout_id]
        for subwid in subwids:
            make_size_widget(layout, subwid, fields=['?'])
            logger.info("Added widget %r to layout %r", subwid, layout)

    from Products.CPSSchemas.BasicWidgets import CPSImageWidget \
        as OldImageWidget
    from Products.CPSSchemas.ExtendedWidgets import CPSPhotoWidget \
        as OldPhotoWidget
    def do_one(doc, widget, layout, tpl_widget, tpl_layout):
        if widget.__class__ is OldImageWidget:
            upgrade_image_widget(doc, widget, layout, tpl_widget, tpl_layout)
        elif widget.__class__ is OldPhotoWidget:
            upgrade_photo_widget(doc, widget, layout, tpl_widget, tpl_layout)

    do_on_flexible_widgets(do_one, portal, FLEXIBLE_LAYOUTS)
