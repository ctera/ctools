#!/usr/bin/python
import sys
import csv
import urllib3
import logging

from pathlib import Path
from getpass import getpass
from cterasdk import GlobalAdmin, core_types, CTERAException, tojsonstr
from cterasdk.lib.filesystem import FileSystem

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ask(prompt):
    user_input = None
    while not user_input:
        user_input = input(prompt)
    return user_input

def create_folders(global_admin,filepath):
    try:
#        address = ask('Enter CTERA Portal address: ')
#        username = ask('Username: ')
#        password = getpass('Password: ')

#        global_admin = GlobalAdmin(address)
#        global_admin.login(username, password)
        with open(filepath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                try:
                    folder_group = row['folder_group']
                    cloud_drive_folder = row['cloud_drive_folder']
                    cloud_drive_folder_description = row['cloud_drive_folder_description']
                    user_owner = row['user_owner']
                    zone_name = row['zone']
                    zone_description = row['zone_description']
                    deduplication_method_type = row['deduplication_method']
                    idx = user_owner.rfind('\\')

                    owner = None
                    if idx > 0:
                        domain, user = user_owner.split('\\')
                        owner = core_types.UserAccount(user, domain)
                    else:
                        owner = core_types.UserAccount(user_owner)

                    try:
                        global_admin.cloudfs.mkfg(folder_group, owner, deduplication_method_type)
                    except CTERAException as error:
                        logging.getLogger().warn('Failed creating folder group. %s', {'name': folder_group, 'error': tojsonstr(error, False)})

                    try:
                        global_admin.cloudfs.mkdir(cloud_drive_folder, folder_group, owner, winacls=True, description=cloud_drive_folder_description)
                    except CTERAException as error:
                        logging.getLogger().warn('Failed creating cloud drive folder. %s', {'name': cloud_drive_folder, 'error': tojsonstr(error, False)})

                    try:
                        global_admin.zones.add(zone_name, description=zone_description)  # add zone
                    except CTERAException as error:
                        logging.getLogger().warn('Failed creating zone. %s', {'name': zone_name, 'error': tojsonstr(error, False)})

                    try:
                        cloudfs_folder_helper = portal_type.CloudFSFolderFindingHelper(cloud_drive_folder, owner)
                        logging.getLogger().info('Adding cloud folders to zone. %s', {'zone': zone_name, 'cloud_drive_folders': [cloud_drive_folder]})
                        global_admin.zones.add_folders(zone_name, [cloudfs_folder_helper])  # add folders
                    except CTERAException as error:
                        logging.getLogger().warn('Failed adding folders to zone. %s', {'zone': zone_name, 'error': tojsonstr(error, False)})
                except CTERAException as error:
                    print(error)
                    input()
        global_admin.logout()
    except KeyboardInterrupt:
        pass

def usage():
    print()
    print('Usage: ' + sys.argv[0] + ' ' + '<csv>')

if __name__ == "__main__":

    config.http['ssl'] = 'Trust'  # ignore certificate errors connecting to CTERA Portal
    config.Logging.get().setLevel(logging.INFO)  # enable debug: logging.DEBUG

    args = sys.argv
    if len(args) < 2:
        logging.getLogger().error('You did not specify an input file. Exiting.')
        usage()
        quit()

    if len(args) > 2:
        logging.getLogger().error('Too many arguments.')
        usage()
        quit()

    filesystem = FileSystem.instance()
    try:
        filepath = args[1]
        logging.getLogger().debug('Looking for input file. %s', {'filepath': filepath})
        info = FileSystem.get_local_file_info(filepath)  # look for config file
        logging.getLogger().debug('Found input file. %s', {'name': info['name'], 'size': info['size']})
    except CTERAException as error:
        logging.getLogger().error('Could not find input file.', {'filepath': filepath})
        usage()
        quit()

    try:
        logging.getLogger().info('Populating CloudFS Structure on CTERA Portal.')
        create_folders(filepath)
        logging.getLogger().info('Completed.')
    except CTERAException as error:
        logging.getLogger().fatal(error.message)
    except KeyboardInterrupt:
        logging.getLogger().fatal('Cancelled by user.')