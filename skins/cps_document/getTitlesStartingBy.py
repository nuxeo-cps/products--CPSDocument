##parameters=proxydocs,strt=None,all=0
# $Id$

res = []

if strt:
    str1 = strt.lower()
    for proxy in proxydocs:
        if proxy.getContent()['title'].lower().startswith(strt):
            res.append(proxy)
elif all:
    res = proxydocs
#return empty list if no letter specified (and all is false) 
return res
