##parameters=user, value
# $Id$
"""this script is called by the the Contributors write expression
check if current user is in contributors if not add him"""
uname = user.getId()
duser = context.portal_metadirectories['members'].getEntry(uname)
if duser:
    uname = duser.get('fullname', uname)
if not value:
    ret = [uname,]
elif uname in value:
    ret = value
else:
    ret = list(value) + [uname]

return ret
