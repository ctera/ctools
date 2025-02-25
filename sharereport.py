from filer import get_filers
from login import global_admin_login

import logging

def share_report(ga, filename, tenant=None):
  """Get share report for a device"""

  if len(tenant) == 0:
    print("Getting all filers on all tenants")
    filers = get_filers(ga, all_tenants=True)
  else:
    print(f"Getting all filers on tenant {tenant}")
    filers = get_filers(ga, all_tenants=False, tenant=tenant)

  if filers is None:
    return None
  
  with open(filename, 'w') as f:
    f.write('Share Name, Share Path, Edge Filer Name, Edge Filer IP\n')
    for filer in filers:
      shares = filer.shares.get()
      for share in shares:
        logging.info(f'Writing {share.name} stats to file')
        f.write(f'{share.name}, {share.directory}, {filer.name}, {filer.network.ipconfig().ip.address}\n')


def share_report_test(ga, tenant=None):
  """Test share report function"""
  filers = get_filers(ga, tenant)

  if filers is None:
    return None
  
  for filer in filers:
    shares = filer.shares.get()
    
    print('Share Name, Edge Filer Name, Edge Filer IP')

    for share in shares:
      print(f'{share.name}, {filer.name}, {filer.network.ipconfig().ip.address}')

if __name__ == '__main__':
  ga = global_admin_login("portal.ctera.me", "admin", "lap6056*")

  try:
    share_report(ga)
  except Exception as e:
    print(e)
  finally:
    ga.logout()