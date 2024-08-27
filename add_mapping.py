from login import global_admin_login
from filer import get_filers, get_filer
from cterasdk import settings

import logging

from cterasdk import common_types

def get_adv_mapping(edge):
    highest_id = 0
    mappings = []
    for domain, mapping in edge.directoryservice.get_advanced_mapping().items():
      print(f"Domain: {domain}")
      print(f"Mapping: {mapping}")
      if mapping.maxID > highest_id:
          highest_id = mapping.maxID
      mappings.append(mapping)

    return mappings, highest_id
  
def add_mapping(address, username, password, domain, device_name=None, tenant=None):
  try:
    settings.sessions.management.ssl = False
    ga = global_admin_login(address, username, password, True)
    if device_name:
      filers=[get_filer(ga, device_name, tenant)]
    elif tenant:
      filers = get_filers(ga, tenant=tenant, all_tenants=False)
    else:
      filers = get_filers(ga, all_tenants=True)

    for edge in filers:
      mappings, highest_id = get_adv_mapping(edge)

      mappings.append(common_types.ADDomainIDMapping(domain, highest_id + 1, highest_id + 200000))

      for mapping in mappings:
          print(f"Mapping: {mapping}")

      logging.info(f"Attempting to add mapping for domain {domain} to {edge.name}")
      edge.directoryservice.set_advanced_mapping(mappings)
      logging.info(f"Added mapping for domain {domain} to {edge.name}")
  except Exception as e:
    logging.error(f"Error: {e}")
  finally:
     ga.logout()
    
