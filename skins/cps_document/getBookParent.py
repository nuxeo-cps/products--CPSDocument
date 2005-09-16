##parameters=
# $Id:$
"""
Retrieve the book parent of a chapter/page.

The page can be in a book, or in a chapter of a book,
or, who knows in the future, in a deeper hierarchy in a book
"""

def getParent(object):
    try:
        if object.portal_type not in ('Book',):
            return getParent(object.aq_inner.aq_parent)
        else:
            return object
    except AttributeError:
        return object

return getParent(context.aq_inner)
