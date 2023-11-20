from cterasdk import *
from filer import get_filer, get_filers
import os
import time
import sys
import sqlite3
import urllib3
import logging
urllib3.disable_warnings()
sys.path.append(os.getcwd())

def import_shares_old(self, device_name_source, device_name_dest):
    try:
        tenant = self.users.session().user.tenant
        filer_source = get_filer(self, device_name_source, tenant)
        filer_destination = get_filer(self, device_name_dest, tenant)
        shares_source = filer_source.get('/config/fileservices/share')
        everyone = gateway_types.ShareAccessControlEntry(gateway_enum.PrincipalType.LG, 'Everyone', gateway_enum.FileAccessMode.RW)
        for share in shares_source:
            get_share=[share.name,share.directory[1:],share.access,share.comment]
            if share.name == 'public' or share.name == 'cloud' or share.name == 'backups':
                logging.info(str(get_share) + ' skipped')
            else:
                    filer_destination.shares.add(get_share[0],get_share[1],acl= [everyone],access=get_share[2],dir_permissions=777,comment=get_share[3])
     
    except Exception as error:
        logging.error(error)

def import_shares(self, device_name_source, device_name_dest):
    try:
        tenant = self.users.session().user.tenant
        filer_source = get_filer(self, device_name_source, tenant)
        filer_destination = get_filer(self, device_name_dest, tenant)
        shares_source = filer_source.get('/config/fileservices/share')
        for share in shares_source:
            print("Share details:")
            print("Name:", getattr(share, 'name', 'Unknown'))
            print("Directory:", getattr(share, 'directory', 'Unknown'))
            print("Access:", getattr(share, 'access', 'Unknown'))
            print("Comment:", getattr(share, 'comment', 'Unknown'))
            print("---")
        everyone = gateway_types.ShareAccessControlEntry(gateway_enum.PrincipalType.LG, 'Everyone', gateway_enum.FileAccessMode.RW)
        for share in shares_source:
            get_share=[share.name,share.directory[1:],share.access,share.comment]
            print("Processing share:", share.name)
            if share.name == 'public' or share.name == 'cloud' or share.name == 'backups':
                logging.info(str(get_share) + ' skipped')
            else:
                try:
                   print("Adding share with values: Name: {}, Directory: {}, ACL: {}, Access: {}, Dir_permissions: {}, Comment: {}".format(get_share[0], get_share[1], [everyone], get_share[2], 777, get_share[3]))
                   print("ACL Entry: Principal Type: {}, Name: {}, Permission: {}".format(everyone.principal_type, everyone.name, everyone.perm))
                   filer_destination.shares.add(get_share[0],get_share[1],acl=[everyone],access=get_share[2],dir_permissions=777,comment=get_share[3])
                   print("Successfully processed share:", share.name)
                except Exception as error:
                    logging.error("Error adding share: %s. Error: %s" % (get_share[0], error))
 
    except Exception as error:
        logging.error("Error adding share: %s. Error: %s" % (get_share[0], error))