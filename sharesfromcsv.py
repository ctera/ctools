import csv
import logging

from cterasdk import Edge, edge_types, edge_enum, settings

def convert_acl_entries(acl_entries):
  """
  Given a list of ACLEntry objects (with attributes .principal_type, .name, .access),
  return a list of edge_types.ShareAccessControlEntry instances.
  """
  # 1. Map CSV-style principal_type strings → edge_enum.PrincipalType
  principal_map = {
    'LocalGroup':   edge_enum.PrincipalType.LG,
    'LocalUser':    edge_enum.PrincipalType.LU,
    'DomainGroup':  edge_enum.PrincipalType.DG,
    'DomainUser':   edge_enum.PrincipalType.DU,
  }

  # 2. Map CSV-style access strings → edge_enum.FileAccessMode
  access_map = {
    'ReadOnly':   edge_enum.FileAccessMode.RO,
    'ReadWrite':  edge_enum.FileAccessMode.RW,
  }

  result = []
  for entry in acl_entries:
    # Lookup principal type
    pt = principal_map.get(entry.principal_type)
    if pt is None:
      raise ValueError(f"Unknown principal_type: {entry.principal_type!r}")

    # Lookup access mode
    mode = access_map.get(entry.access)
    if mode is None:
      raise ValueError(f"Unknown access mode: {entry.access!r}")

    # Create and collect a ShareAccessControlEntry
    result.append(
      edge_types.ShareAccessControlEntry(pt, entry.name, mode)
    )

  return result

class ACLEntry:
    def __init__(self, principal_type, name, access):
        self.principal_type = principal_type
        self.name = name
        self.access = access

    def __repr__(self):
        return f"ACLEntry(principal_type={self.principal_type!r}, name={self.name!r}, access={self.access!r})"


class ShareEntry:
    def __init__(self, name, directory, access, acl):
        self.name = name
        self.directory = directory
        self.access = access
        self.acl = acl

    def __repr__(self):
        return (f"ShareEntry(name={self.name!r}, directory={self.directory!r}, "
                f"access={self.access!r}, acl={self.acl!r})")


def parse_csv(file_path):
  """
  Reads a CSV with columns: name, path, access, acl
  Returns a list of ShareEntry objects, where .acl is a list of ACLEntry.
  """
  entries = []

  with open(file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
      # 1. Extract and strip each top-level field
      share_name = row['name'].strip()
      directory = row['path'].strip()
      access_mode = row['access'].strip()
      acl_field = row['acl'].strip()

      # 2. Parse the ACL string into ACLEntry objects
      acl_list = []
      if acl_field:
        # Each ACL entry is separated by ';'
        for raw_entry in acl_field.split(';'):
          raw_entry = raw_entry.strip()
          if not raw_entry:
            continue

          # Expect exactly three parts: principal_type, principal_name, permission
          parts = [part.strip() for part in raw_entry.split(':')]
          if len(parts) != 3:
            # Skip or log an unexpected format
            continue

          principal_type, principal_name, permission = parts
          acl_list.append(ACLEntry(principal_type, principal_name, permission))

      # 3. Build the ShareEntry
      entries.append(ShareEntry(share_name, directory, access_mode, acl_list))

    return entries


def shares_from_csv(edge_address, edge_username, edge_password, csv_file):
  """
  Reads shares from a CSV file and adds them to the specified CTERA Edge device.
  
  :param edge_address: IP address of the CTERA Edge device
  :param edge_username: Username for the CTERA Edge device
  :param edge_password: Password for the CTERA Edge device
  :param csv_file: Path to the CSV file containing share definitions
  """
  share_entries = parse_csv(csv_file)

  settings.sessions.management.ssl = False
  with Edge(edge_address) as edge:
    edge.login(edge_username, edge_password)

    share_entries = parse_csv(csv_file)
    for share in share_entries:
      logging.info(f"Processing share: {share.name}")
      logging.info(f"  Directory: {share.directory}")
      logging.info(f"  Access: {share.access}")
      logging.info("  ACL:")
      for acl in share.acl:
        logging.info(f"    {acl.principal_type}: {acl.name} - {acl.access}")

      acl_list = convert_acl_entries(share.acl)
      try:
        edge.shares.add(share.name, share.directory, acl_list, access=share.access)
      except Exception as e:
        logging.error(f"Failed to add share {share.name}: {e}")
   


if __name__ == "__main__":
  settings.sessions.management.ssl = False
  with Edge('192.168.22.244') as edge:
    edge.login('admin', 'lap6056*')

    for share in share_entries:
      print(f"Processing share: {share.name}")
      print(f"  Directory: {share.directory}")
      print(f"  Access: {share.access}")
      print("  ACL:")
      for acl in share.acl:
        print(f"    {acl.principal_type}: {acl.name} - {acl.access}")
      

      acl_list = convert_acl_entries(share.acl)

      edge.shares.add(share.name, share.directory, acl_list, access=share.access)


