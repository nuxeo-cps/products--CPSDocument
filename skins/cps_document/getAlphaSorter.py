##parameters=proxydocs
# $Id $

def sort(a,b):
    return cmp(a.getContent()['title'],b.getContent()['title'])

if proxydocs:
    return proxydocs.sort(sort)
else:
    return []

