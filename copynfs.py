import cterasdk
from filer import get_filer, get_filers
from cterasdk import Edge, edge_types, edge_enum
from login import global_admin_login

principal_dict = {"LocalGroup": edge_enum.PrincipalType.LG, "LocalUser": edge_enum.PrincipalType.LU, "DomainGroup": edge_enum.PrincipalType.DG, "DomainUser": edge_enum.PrincipalType.DU}
perm_dict = {"ReadWrite": edge_enum.FileAccessMode.RW, "ReadOnly": edge_enum.FileAccessMode.RO, "None": edge_enum.FileAccessMode.NA}


def copy_nfs_share(ga, share, dest):
  try:
    tenant = ga.users.session().user.tenant
    filer_dest = get_filer(ga, dest, tenant)

    client_list = []
    for client in share.trustedNFSClients:
      if client.accessLevel == "ReadWrite":
        client_list.append(edge_types.NFSv3AccessControlEntry(client.address, client.netmask, edge_enum.FileAccessMode.RW))
      elif client.accessLevel == "ReadOnly":
        client_list.append(edge_types.NFSv3AccessControlEntry(client.address, client.netmask, edge_enum.FileAccessMode.RO))

    acl_entries = []
    for acl in share.acl:
      print("Processing ACL entry: %s" % str(acl))

      name = None

      if acl.principal2._classname == "LocalUser":
        name = acl.principal2.ref.split("#")[-1]
        print("LocalUser: ", name)
      elif acl.principal2._classname == "DomainUser":
        name = acl.principal2.name
        print("DomainUser: ", name)
      elif acl.principal2._classname == "LocalGroup":
        name = acl.principal2.ref.split("#")[-1]
        print("LocalGroup: ", name)
      elif acl.principal2._classname == "DomainGroup":
        name = acl.principal2.name
        print("DomainGroup: ", name)
      else:
        print("Error processing ACL entry: ", acl)

      entry = edge_types.ShareAccessControlEntry(principal_dict[acl.principal2._classname], name, perm_dict[acl.permissions.allowedFileAccess])
      acl_entries.append(entry)
    
    filer_dest.shares.add(share.name, share.directory[1:], acl=None, access=share.access, dir_permissions=777, comment=share.comment, export_to_nfs=True, trusted_nfs_clients=client_list)

    print("Number of ACL Entries to add: %s" % len(acl_entries))
    for entry in acl_entries:
      try:
        filer_dest.shares.add_acl(share.name, [entry])
        print("Successfully added ACL entry %s to share %s" % (entry.name, share.name))
      except Exception as e:
        print("Failed to add ACL entry %s to share %s" % (entry.name, share.name))
        print("This could be due to the destination filer not having the same local users/groups as the source filer has in its permissions for the share")
        print(e)
        continue
    print("Successfully added ACL entries to share %s" % share.name)
  except Exception as e:
    print("Failed to copy share: %s" % share.name)
    print(e)

def get_nfs_shares(ga, source):
  tenant = ga.users.session().user.tenant
  filer = get_filer(ga, source, tenant)

  try:
    shares = filer.shares.get()

    nfs_shares = []

    for share in shares:
      if share.exportToNFS:
        nfs_shares.append(share)
    
    return nfs_shares
  except Exception as e:
    print("Failed to get shares from device: %s" % source)
    print(e)
    return None

def copy_nfs_shares(ga, source, dest):
  try:
    tenant = ga.users.session().user.tenant
    filer_source = get_filer(ga, source, tenant)
    filer_dest = get_filer(ga, dest, tenant)

    nfs_shares_source = get_nfs_shares(ga, source)

    for share in nfs_shares_source:
      try:
        #get the nfs clients from the source share
        source_nfs_clients = filer_source.shares.get(share.name).trustedNFSClients

        print(dir(source_nfs_clients[0]))

        print("nfs client accessLevel: %s" % source_nfs_clients[0].accessLevel)
        print("nfs client address: %s" % source_nfs_clients[0].address)
        print("nfs client netmask: %s" % source_nfs_clients[0].netmask)

        client_list = []
        for client in source_nfs_clients:
          if client.accessLevel == "ReadWrite":
            client_list.append(edge_types.NFSv3AccessControlEntry(client.address, client.netmask, edge_enum.FileAccessMode.RW))
          elif client.accessLevel == "ReadOnly":
            client_list.append(edge_types.NFSv3AccessControlEntry(client.address, client.netmask, edge_enum.FileAccessMode.RO))

        acl_entries = []
        for acl in share.acl:
          print("Processing ACL entry: %s" % str(acl))

          name = None

          if acl.principal2._classname == "LocalUser":
            name = acl.principal2.ref.split("#")[-1]
            print("LocalUser: ", name)
          elif acl.principal2._classname == "DomainUser":
            name = acl.principal2.name
            print("DomainUser: ", name)
          elif acl.principal2._classname == "LocalGroup":
            name = acl.principal2.ref.split("#")[-1]
            print("LocalGroup: ", name)
          elif acl.principal2._classname == "DomainGroup":
            name = acl.principal2.name
            print("DomainGroup: ", name)
          else:
            print("Error processing ACL entry: ", acl)
  
          entry = edge_types.ShareAccessControlEntry(principal_dict[acl.principal2._classname], name, perm_dict[acl.permissions.allowedFileAccess])
          acl_entries.append(entry)
        
        filer_dest.shares.add(share.name, share.directory[1:], acl=None, access=share.access, dir_permissions=777, comment=share.comment, export_to_nfs=True, trusted_nfs_clients=client_list)

        print("Number of ACL Entries to add: %s" % len(acl_entries))
        for entry in acl_entries:
          try:
            filer_dest.shares.add_acl(share.name, [entry])
            print("Successfully added ACL entry %s to share %s" % (entry.name, share.name))
          except Exception as e:
            print("Failed to add ACL entry %s to share %s" % (entry.name, share.name))
            print("This could be due to the destination filer not having the same local users/groups as the source filer has in its permissions for the share")
            print(e)
            continue
        print("Successfully added ACL entries to share %s" % share.name)
      except Exception as e:
        print("Failed to copy share: %s" % share.name)
        print(e)

  except Exception as e:
    print("Failed to copy shares from device: %s to device: %s" % (source, dest))
    print(e)


"""if __name__ == "__main__":
  ga = global_admin_login("192.168.22.197", "admin", "lap6056*", True)
  try:
    copy_nfs_shares(ga, "lakegw2", "labgw")
  except Exception as e:
    print(e)
  finally:
    ga.logout()"""