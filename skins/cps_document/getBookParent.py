##parameters=
# function to retrieve the book parent of a chapter/page.
#
# The page can be in a book, or in a chapter of a book,
# or, who knows in the future, in a deeper hierarchy in a book

def getParent(object):
    if object.portal_type not in ('Book'):
        return getParent(object.aq_parent)
    else:
        return object


parent = context.aq_inner
returned = parent

returned = getParent(parent)

return returned
