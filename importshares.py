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
from cterasdk import edge_types, edge_enum

principal_dict = {"LocalGroup": edge_enum.PrincipalType.LG, "LocalUser": edge_enum.PrincipalType.LU, "DomainGroup": edge_enum.PrincipalType.DG, "DomainUser": edge_enum.PrincipalType.DU}
perm_dict = {"ReadWrite": edge_enum.FileAccessMode.RW, "ReadOnly": edge_enum.FileAccessMode.RO, "None": edge_enum.FileAccessMode.NA}

def import_shares(self, device_name_source, device_name_dest):
    logging.info("Importing shares from device: %s to device: %s" % (device_name_source, device_name_dest))
    try:
        tenant = self.users.session().user.tenant
        filer_source = get_filer(self, device_name_source, tenant)
        filer_destination = get_filer(self, device_name_dest, tenant)
        shares_source = filer_source.shares.get()
        for share in shares_source:
            logging.info("Share details:")
            logging.info("Name:", share.name)
            logging.info("Directory:", share.directory)
            logging.info("Access:", share.access)
            logging.info("Comment:", share.comment)
            logging.info("---")
        
        everyone = edge_types.ShareAccessControlEntry(edge_enum.PrincipalType.LG, 'Everyone', edge_enum.FileAccessMode.RW)
        for share in shares_source:
            logging.info("Processing share:", str(share.name))
            if share.name == 'public' or share.name == 'cloud' or share.name == 'backups':
                logging.info(str(share.name) + ' skipped')
            else:
                try:
                    acl_entries = []
                    for acl in share.acl:
                        logging.debug("Processing ACL entry: ", acl)

                        name = None

                        if acl.principal2._classname == "LocalUser":
                            name = acl.principal2.ref.split("#")[-1]
                            logging.debug("LocalUser: ", name)
                        elif acl.principal2._classname == "DomainUser":
                            name = acl.principal2.name
                            logging.debug("DomainUser: ", name)
                        elif acl.principal2._classname == "LocalGroup":
                            name = acl.principal2.ref.split("#")[-1]
                            logging.debug("LocalGroup: ", name)
                        elif acl.principal2._classname == "DomainGroup":
                            name = acl.principal2.name
                            logging.debug("DomainGroup: ", name)
                        else:
                            logging.error("Error processing ACL entry: ", acl)

                        entry = edge_types.ShareAccessControlEntry(principal_dict[acl.principal2._classname], name, perm_dict[acl.permissions.allowedFileAccess])
                        acl_entries.append(entry)


                    logging.info("Adding share with values: Name: {}, Directory: {}, ACL: {}, Access: {}, Dir_permissions: {}, Comment: {}".format(share.name, share.directory[1:], acl_entries, share.access, 777, share.comment))
                    logging.info("ACL Entry: Principal Type: {}, Name: {}, Permission: {}".format(everyone.principal_type, everyone.name, everyone.perm))
                    filer_destination.shares.add(share.name, share.directory[1:], acl_entries, access=share.access, dir_permissions=777, comment=share.comment)
                    logging.info("Successfully processed share:", share.name)
                except Exception as error:
                    logging.error("Error adding share: %s. Error: %s" % (share.name, error))
 
    except Exception as error:
        logging.error("Error adding share. Error:", error)