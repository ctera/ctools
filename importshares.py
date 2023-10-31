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

def import_shares(self, device_name_source, device_name_dest):
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
     
    except CTERAException as error:
        logging.error(error)

def import_shares_old(address_source, login_source, password_source, address_destination, login_destination, password_destination):
    try:
        config.http['SSL'] = 'Trust'
        filer_source = Gateway(address_source, 443, True)
        filer_destination = Gateway(address_destination, 443, True)
        filer_source.login(login_source, password_source)
        filer_destination.login(login_destination, password_destination)
        shares_source = filer_source.get('/config/fileservices/share')
        everyone = gateway_types.ShareAccessControlEntry(gateway_enum.PrincipalType.LG, 'Everyone', gateway_enum.FileAccessMode.RW)
        for share in shares_source:
            get_share=[share.name,share.directory[1:],share.access,share.comment]
            if share.name == 'public' or share.name == 'cloud' or share.name == 'backups':
                logging.info(str(get_share) + ' skipped')
            else:
                    filer_destination.shares.add(get_share[0],get_share[1],acl= [everyone],access=get_share[2],csc='disabled',dir_permissions=777,comment=get_share[3])
     
    except CTERAException as error:
        logging.error(error)