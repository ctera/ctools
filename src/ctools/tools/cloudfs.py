"""CloudFS tool - Create folder groups, cloud drive folders, and zones from CSV."""

import csv
import logging
from typing import Any

from cterasdk import core_types, CTERAException, tojsonstr


def create_folders(session: Any, filepath: str) -> None:
    """
    Create cloud folder groups, cloud drive folders, and zones from a CSV file.

    Args:
        session: Authenticated GlobalAdmin session
        filepath: Path to CSV file with folder definitions

    CSV columns expected:
        - folder_group: Name of the folder group
        - cloud_drive_folder: Name of the cloud drive folder
        - cloud_drive_folder_description: Description for the folder
        - user_owner: Owner in format 'domain\\user' or just 'user'
        - zone: Zone name
        - zone_description: Description for the zone
        - deduplication_method: Deduplication method type
    """
    logging.info("Starting CloudFS create folders task.")

    try:
        with open(filepath, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')

            for row in csv_reader:
                try:
                    folder_group = row['folder_group']
                    cloud_drive_folder = row['cloud_drive_folder']
                    cloud_drive_folder_description = row.get('cloud_drive_folder_description', '')
                    user_owner = row['user_owner']
                    zone = row['zone']
                    zone_description = row.get('zone_description', '')
                    deduplication_method_type = row.get('deduplication_method', 'None')

                    # Parse owner (domain\user or just user)
                    idx = user_owner.rfind('\\')
                    if idx > 0:
                        domain, user = user_owner.split('\\')
                        owner = core_types.UserAccount(user, domain)
                    else:
                        owner = core_types.UserAccount(user_owner)

                    # Create folder group
                    try:
                        session.cloudfs.groups.add(folder_group, owner, deduplication_method_type)
                        logging.info("Created folder group: %s", folder_group)
                    except CTERAException as e:
                        logging.error('Failed creating folder group %s: %s', folder_group, tojsonstr(e, False))

                    # Create cloud drive folder
                    try:
                        session.cloudfs.drives.add(
                            cloud_drive_folder,
                            folder_group,
                            owner,
                            description=cloud_drive_folder_description
                        )
                        logging.info("Created cloud drive folder: %s", cloud_drive_folder)
                    except CTERAException as e:
                        logging.error('Failed creating cloud drive folder %s: %s', cloud_drive_folder, tojsonstr(e, False))

                    # Create zone
                    try:
                        session.cloudfs.zones.add(zone, description=zone_description)
                        logging.info("Created zone: %s", zone)
                    except CTERAException as e:
                        logging.error('Failed creating zone %s: %s', zone, tojsonstr(e, False))

                    # Add folder to zone
                    try:
                        folder_to_add = core_types.CloudFSFolderFindingHelper(cloud_drive_folder, owner)
                        session.cloudfs.zones.add_folders(zone, [folder_to_add])
                        logging.info("Added folder %s to zone %s", cloud_drive_folder, zone)
                    except CTERAException as e:
                        logging.error('Failed adding folder to zone: %s', tojsonstr(e, False))

                    logging.info(
                        'Successfully processed: folder group=%s, cloud folder=%s, zone=%s',
                        folder_group, cloud_drive_folder, zone
                    )

                except CTERAException as e:
                    logging.error("Error processing row: %s", e)
                    continue
                except KeyError as e:
                    logging.error("Missing required column in CSV: %s", e)
                    continue

        logging.info("Finished CloudFS create folders task.")

    except FileNotFoundError:
        logging.error("CSV file not found: %s", filepath)
        raise
    except Exception as e:
        logging.error("Error in CloudFS task: %s", e)
        raise
