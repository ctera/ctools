import cterasdk
from filer import get_filer, get_filers
from cterasdk import Edge, edge_types, edge_enum
from login import global_admin_login

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
    
    filer_dest.shares.add(share.name, share.directory[1:], export_to_nfs=True, trusted_nfs_clients=client_list)
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
        
        filer_dest.shares.add(share.name, share.directory[1:], export_to_nfs=True, trusted_nfs_clients=client_list)
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