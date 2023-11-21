from cterasdk import *

from login import global_admin_login

portal_address = "192.168.80.201"
portal_username = "admin"
portal_password = "lap6056*"
ignore_cert = True

global_admin = global_admin_login(portal_address, portal_username, portal_password, ignore_cert)

#result = global_admin.cli.run_command('show /settings')

admin_portal = global_admin.portals.browse_global_admin()

allowSSO = bool(global_admin.get('/rolesSettings/readWriteAdminSettings/allowSSO'))

print("Current sso setting: " + str(allowSSO))

if not allowSSO:
    global_admin.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')
else:
    print("This was already true")

allowSSO = bool(global_admin.get('/rolesSettings/readWriteAdminSettings/allowSSO'))

print("If it was false this should be true: " + str(allowSSO))

"""test_set = global_admin.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'False')

print(test_set)

result = global_admin.get('/rolesSettings/readWriteAdminSettings/allowSSO')

print(result)

test_set = global_admin.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')

print(test_set)

result = global_admin.get('/rolesSettings/readWriteAdminSettings/allowSSO')

print(result)"""


