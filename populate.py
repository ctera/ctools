from cterasdk import *
from cterasdk import settings
from filer import get_filer, get_filers

import urllib3
urllib3.disable_warnings()

import logging

from login import global_admin_login

def get_cloud_folders(self):
  """Get all cloud folders on a tenant."""
  try:
    result = self.cloudfs.drives.all()
    logging.info("Finished get_cloud_folders task.")

    return result
  except CTERAException as ce:
    logging.error(ce)
    logging.error("Failed get_cloud_folders task.")
      
  return None

def create_shares_from_folders_list(self, folders, edge_filer):
  """Create shares from a list of cloud folders."""
  try:
    for folder in folders:
      if folder.name != 'My Files':
        logging.info("Creating share for folder: " + folder.name)

        try:
          users = self.users.list_local_users(include = ['name', 'email', 'firstName', 'lastName'])
          match = None
          for user in users:
            if user.name == folder.owner.split('/')[-1]:
              match = user
              break
          
          if match is not None:
            path = "cloud/users/"+ match.firstName + " " + match.lastName + "/" + folder.name
            edge_filer.shares.add(folder.name, path)
        except CTERAException as ce:
          logging.error(ce)
          logging.error("Failed creating share for folder: " + folder.name)

      
  except CTERAException as ce:
    logging.error(ce)
    logging.error("Failed create_shares_from_folders_list task.")

def run_populate(address, username, password, device_name):
  try:
    settings.sessions.management.ssl = False
    global_admin = global_admin_login(address, username, password, True)
    folders = get_cloud_folders(global_admin)

    filer = get_filer(global_admin, device_name)

    create_shares_from_folders_list(global_admin, folders, filer)
  except CTERAException as ce:
    logging.error(ce)
    logging.error("Failed creating share task.")
  finally:
    global_admin.logout()


"""if __name__ == "__main__":
  run_populate("192.168.22.197", "admin", "lap6056*", "labgw")"""