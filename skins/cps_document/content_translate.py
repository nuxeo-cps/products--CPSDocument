##parameters=lang, dest=None, REQUEST=None

proxy = context

if not hasattr(proxy, 'addLanguageToProxy'):
    if REQUEST is None:
        raise ValueError("Not a proxy")
    psm = 'psm_translation_not_supported'
    url = proxy.absolute_url()

localizer = context.Localizer
if not lang in localizer.get_supported_languages():
    if REQUEST is None:
        raise ValueError("Language '%s' not supported" % lang)
    psm = 'psm_translation_lang_not_supported'
    url = proxy.absolute_url()

if dest:
    # copy document for translating it.
    wftool = context.portal_workflow
    new_id = wftool.findNewId(dest, proxy.getId())
    wftool.doActionFor(proxy, 'translate', dest_container=dest,
                       initial_transition='checkout_translation_in',
                       language_map={lang: proxy.getLanguage()})
    psm = 'psm_translation_copied'
    url = '%s/%s/%s' % (context.portal_url(), dest, new_id)
else:
    # translate in place
    proxy.addLanguageToProxy(lang, from_lang=proxy.getLanguage())
    psm = 'psm_translation_added'
    url = proxy.absolute_url()

if REQUEST is not None:
    REQUEST.RESPONSE.redirect('%s/?portal_status_message=%s' % (url, psm))
