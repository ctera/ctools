import cterasdk
from filer import get_filer, get_filers
from copynfs import copy_nfs_share
from cterasdk import Edge, edge_types, edge_enum
import logging

import cterasdk.settings

principal_dict = {"LocalGroup": edge_enum.PrincipalType.LG, "LocalUser": edge_enum.PrincipalType.LU, "DomainGroup": edge_enum.PrincipalType.DG, "DomainUser": edge_enum.PrincipalType.DU}
perm_dict = {"ReadWrite": edge_enum.FileAccessMode.RW, "ReadOnly": edge_enum.FileAccessMode.RO, "None": edge_enum.FileAccessMode.NA}


def copyshares(source, source_username, source_pass, dest, dest_username, dest_pass):
  cterasdk.settings.sessions.management.ssl = False

  filer_source = Edge(source)
  filer_source.login(source_username, source_pass)
  filer_destination = Edge(dest)
  filer_destination.login(dest_username, dest_pass)
  try:
    shares_source = filer_source.shares.get()

    logging.info("Copying shares from device <%s> to device <%s>" % (source, dest))
    logging.info("Number of shares found: %s" % len(shares_source))
  except Exception as e:
    logging.error("Failed to get shares from device: %s" % source)
    logging.error(e)
    return
  
  try:
    default = "Unknown"
    for share in shares_source:
      logging.info("Share details:")
      logging.info("Name: %s" % str(share.name or default))
      logging.info("Directory: %s" % str(share.directory or default))
      logging.info("Access: %s" % str(share.access or default))
      logging.info("Comment: %s" % str(share.comment or default))
      logging.info("---")
  except Exception as e:
    logging.error("Failed to print share details")
    logging.error(e)
    return
  
  try:
    for share in shares_source:
      logging.info("Processing share: %s" % str(share.name))
      if share.name == 'public' or share.name == 'cloud' or share.name == 'backups':
        logging.info("%s skipped" % str(share.name))
        continue
      elif share.exportToNFS:
        logging.info("Copying NFS share: %s" % str(share.name))
        copy_nfs_share(share, filer_destination)
        continue
      try:
        acl_entries = []
        for acl in share.acl:
          logging.debug("Processing ACL entry: %s" % str(acl))

          name = None

          if acl.principal2._classname == "LocalUser":
            name = acl.principal2.ref.split("#")[-1]
            logging.debug("LocalUser: " + str(name))
          elif acl.principal2._classname == "DomainUser":
            name = acl.principal2.name
            logging.debug("DomainUser: " + str(name))
          elif acl.principal2._classname == "LocalGroup":
            name = acl.principal2.ref.split("#")[-1]
            logging.debug("LocalGroup: " + str(name))
          elif acl.principal2._classname == "DomainGroup":
            name = acl.principal2.name
            logging.debug("DomainGroup: ", str(name))
          else:
            logging.error("Error processing ACL entry: ", acl)
  
          entry = edge_types.ShareAccessControlEntry(principal_dict[acl.principal2._classname], name, perm_dict[acl.permissions.allowedFileAccess])
          acl_entries.append(entry)

        logging.info("Adding share %s to filer <%s>" % (share.name, dest))
        try:
            share_access = share.access if share.access is not None else []
            share_comment = share.comment if share.comment is not None else ""
            share_directory = share.directory[1:] if share.directory else ""

            logging.info("Share Name: %s" % share.name)
            logging.info("Share Directory: %s" % share_directory)
            logging.info("Share Access: %s" % share_access)
            logging.info("Share Comment: %s" % share_comment)

            filer_destination.shares.add(
                share.name, 
                share_directory, 
                acl=None, 
                access=share_access, 
                dir_permissions=777, 
                comment=share_comment
            )
            logging.info("Successfully added share %s to filer <%s>" % (share.name, dest))

            logging.info("Number of ACL Entries to add: %s" % len(acl_entries))
            for entry in acl_entries:
                try:
                    filer_destination.shares.add_acl(share.name, [entry])
                    logging.info("Successfully added ACL entry %s to share %s" % (entry.name, share.name))
                except Exception as e:
                    logging.error("Failed to add ACL entry %s to share %s" % (entry.name, share.name))
                    logging.error("This could be due to the destination filer not having the same local users/groups.")
                    logging.error(e)
        except Exception as e:
            logging.error("Failed to add share %s to filer <%s>" % (share.name, dest))
            logging.error(e)
            continue
      except Exception as e:
        logging.error("Failed to process ACL entries")
        logging.error(e)
        continue
  except Exception as e:
    logging.error("Failed to process shares")
    logging.error(e)
    return
  
  finally:
    filer_source.logout()
    filer_destination.logout()


