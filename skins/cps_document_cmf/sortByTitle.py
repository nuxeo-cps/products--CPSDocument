##parameters=proxydocs
# $Id$

def sort(a,b):
    return cmp(getattr(a, 'title', ''),getattr(b, 'title', ''))

if proxydocs:
    return proxydocs.sort(sort)
else:
    return []

