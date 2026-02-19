"""Populate cloud folders as shares on a device."""

import logging
from typing import Any, Optional, Dict

from ..core.filer import get_filer


def _get_cloud_folders(session: Any) -> list:
    """Get all cloud folders from the portal."""
    try:
        # cloudfs.drives.all() returns a QueryIterator, convert to list
        result = list(session.cloudfs.drives.all())
        logging.info("Found %d cloud folders", len(result))
        return result
    except Exception as e:
        logging.error("Failed to get cloud folders: %s", e)
        return []


def _build_user_dicts(session: Any, domain: Optional[str] = None) -> tuple:
    """
    Build dictionaries of local and domain users.

    Returns:
        Tuple of (local_users_dict, domain_users_dict)
    """
    local_users_dict: Dict[str, Any] = {}
    domain_users_dict: Dict[str, Any] = {}

    # Get local users
    try:
        local_users = session.users.list_local_users(include=['name', 'firstName', 'lastName'])
        local_users_dict = {user.name: user for user in local_users}
        logging.info("Found %d local users", len(local_users_dict))
    except Exception as e:
        logging.error("Failed to get local users: %s", e)
        return local_users_dict, domain_users_dict

    # Get domain users if domain is specified
    if domain:
        try:
            domain_users = session.users.list_domain_users(domain, include=['name', 'firstName', 'lastName'])
            domain_users_dict = {user.name: user for user in domain_users}
            logging.info("Found %d domain users in %s", len(domain_users_dict), domain)
        except Exception as e:
            logging.error("Failed to get domain users from %s: %s", domain, e)

    return local_users_dict, domain_users_dict


def populate_shares(
    session: Any,
    device: str,
    domain: Optional[str] = None
) -> None:
    """
    Populate cloud folders as shares on a device.

    This function gets cloud folders from the portal and creates shares
    for them on the specified Edge device. It matches cloud folder owners
    to local/domain users to determine the correct share path.

    Args:
        session: Authenticated GlobalAdmin session
        device: Device name to populate shares on
        domain: Domain name (only needed if domain users are cloud folder owners)
    """
    logging.info("Starting populate shares task.")

    try:
        # Get cloud folders from the GlobalAdmin session (not from the filer)
        logging.info("Getting cloud folders from portal")
        folders = _get_cloud_folders(session)

        if not folders:
            logging.warning("No cloud folders found")
            logging.info("Finished populate shares task.")
            return

        # Get the filer device
        filer = get_filer(session, device)
        if not filer:
            logging.error("Device not found: %s", device)
            return

        # Build user lookup dictionaries
        local_users_dict, domain_users_dict = _build_user_dicts(session, domain)

        if not local_users_dict and not domain_users_dict:
            logging.error("No users found. Cannot create shares.")
            return

        # Create shares for each cloud folder
        for folder in folders:
            if folder is None:
                continue

            # Skip "My Files" folder
            if folder.name == "My Files":
                logging.debug("Skipping 'My Files' folder")
                continue

            logging.info("Processing cloud folder: %s", folder.name)

            # Try to find the folder owner in local users first
            # folder.owner format is typically like "users/username" or similar
            owner_name = folder.owner.split('/')[-1] if folder.owner else None

            if not owner_name:
                logging.warning("Folder %s has no owner. Skipping.", folder.name)
                continue

            # Try local users first
            match = local_users_dict.get(owner_name)

            # If not found in local users and domain is specified, try domain users
            if match is None and domain:
                logging.debug("User not found in local users. Checking domain users.")
                # Domain user format might be different - try the second-to-last part
                domain_owner_name = folder.owner.split('/')[-2] if '/' in folder.owner else owner_name
                match = domain_users_dict.get(domain_owner_name)

            if match is not None:
                # Build the share path: cloud/users/FirstName LastName/FolderName
                user_display_name = f"{match.firstName} {match.lastName}"
                share_path = f"cloud/users/{user_display_name}/{folder.name}"

                logging.info("Found folder owner: %s", user_display_name)
                logging.info("Creating share with path: %s", share_path)

                try:
                    filer.shares.add(str(folder.name), share_path)
                    logging.info("Successfully created share: %s", folder.name)
                except Exception as e:
                    logging.warning("Failed to create share %s: %s", folder.name, e)
            else:
                logging.warning(
                    "Owner '%s' for folder '%s' not found in local or domain users. Share will not be created.",
                    owner_name, folder.name
                )

        logging.info("Finished populate shares task.")
    except Exception as e:
        logging.error("Error in populate shares task: %s", e)
