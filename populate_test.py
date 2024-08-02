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

def run_populate(address, username, password, device_name, domain):
  try:
    settings.sessions.management.ssl = False
    global_admin = global_admin_login(address, username, password, True)
    folders = get_cloud_folders(global_admin)

    filer = get_filer(global_admin, device_name)

    create_shares_from_folders_list(global_admin, folders, filer, domain)
  except CTERAException as ce:
    logging.error(ce)
    logging.error("Failed creating share task.")
  finally:
    global_admin.logout()

def create_shares_from_folders_list(self, folders, edge_filer, domain):
    """Create shares from a list of cloud folders."""
    local_users = self.users.list_local_users(include = ['name', 'firstName', 'lastName'])
    local_users_dict = {user.name: user for user in local_users}

    domain_users = self.users.list_domain_users(domain, include=['name', 'firstName', 'lastName'])
    domain_users_dict = {user.name: user for user in domain_users}

    for folder in folders:
      if folder.name != "My Files":
        print("Attempting to create share for folder: " + str(folder.name))

        match = local_users_dict.get(folder.owner.split('/')[-1], None)

        if match is None:
          print("User not found in local users. Attempting to get user from domain users dict.")
          match = domain_users_dict.get(folder.owner.split('/')[-2], None)
        
        if match is not None:
          path = "cloud/users/" + match.firstName + " " + match.lastName + "/" + folder.name
          print("Folder owner is found and the path has been set. Now adding the share.")
          edge_filer.shares.add(str(folder.name), path)
        else:
          print("Folder owner not found. Share will not be created.")
          continue
