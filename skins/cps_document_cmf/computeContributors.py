##parameters=user, value
# $Id$
"""this script is called by the the Contributors write expression
check if current user is in contributors if not add him"""
uname = user.getId()

return uname
try:
    duser = context.portal_directories['members'].getEntry(uname, default=None)
except AttributeError:
    duser
if duser:
    uname = duser.get('fullname', uname)
if not value:
    ret = [uname,]
elif uname in value:
    ret = value
else:
    ret = list(value) + [uname]

return ret
