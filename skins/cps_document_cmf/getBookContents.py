##parameters=
# recursive call of getFoldercCntents

def getContainerContent(object, liste, level, nb):
    
    if object.portal_type not in ('Chapter', 'Book'):
        liste.append((level, nb, object))
    else:
        items = object.getFolderContents()
        liste.append((level, None, object))
        level = level + 1
        for i in range(len(items)):
            item = items[i]
            list = getContainerContent(item, liste, level, i)



level = 0
returned = []
items = context.getFolderContents()
for i in range(len(items)):
    item = items[i]
    getContainerContent(item, returned, level, i)


return returned
