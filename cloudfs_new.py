import csv
import logging

from cterasdk import GlobalAdmin, core_types, CTERAException, tojsonstr


def create_folders(global_admin, filepath):

    try:
        with open(filepath, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                try:
                    folder_group = row['folder_group']
                    cloud_drive_folder = row['cloud_drive_folder']
                    cloud_drive_folder_description = row['cloud_drive_folder_description']
                    user_owner = row['user_owner']
                    zone = row['zone']
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
                        global_admin.cloudfs.groups.add(folder_group, owner, deduplication_method_type)
                    except CTERAException as e:
                        logging.error('Failed creating folder group: %s', tojsonstr(e, False))
                    
                    try:
                        global_admin.cloudfs.drives.add(cloud_drive_folder, folder_group, owner, description=cloud_drive_folder_description)
                    except CTERAException as e:
                        logging.error('Failed creating cloud drive folder: %s', tojsonstr(e, False))

                    try:
                        global_admin.cloudfs.zones.add(zone, description=zone_description)
                    except CTERAException as e:
                        logging.error('Failed creating zone: %s', tojsonstr(e, False))
                    
                    try:
                        folder_to_add = core_types.CloudFSFolderFindingHelper(cloud_drive_folder, owner)
                        global_admin.cloudfs.zones.add_folders(zone, [folder_to_add])
                    except CTERAException as e:
                        logging.error('Failed adding folders to zone: %s', tojsonstr(e, False))
                    
                    logging.info('Successfully created folder group, cloud drive folder, and zone for: %s', cloud_drive_folder)
                except CTERAException as e:
                    print(e)
                    continue

                
    except FileNotFoundError as e:
        print(f"File {e} not found.")

