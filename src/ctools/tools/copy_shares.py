"""Copy shares between CTERA filers."""

import logging

from cterasdk import Edge, settings, edge_types, edge_enum


# Mapping from principal class names to enum types
PRINCIPAL_DICT = {
    "LocalGroup": edge_enum.PrincipalType.LG,
    "LocalUser": edge_enum.PrincipalType.LU,
    "DomainGroup": edge_enum.PrincipalType.DG,
    "DomainUser": edge_enum.PrincipalType.DU
}

# Mapping from permission strings to enum types
PERM_DICT = {
    "ReadWrite": edge_enum.FileAccessMode.RW,
    "ReadOnly": edge_enum.FileAccessMode.RO,
    "None": edge_enum.FileAccessMode.NA
}

# Shares to skip during copy
SKIP_SHARES = {'public', 'cloud', 'backups'}


def _copy_nfs_share(share, dest_filer) -> None:
    """Copy an NFS-exported share to destination filer."""
    try:
        # Build NFS client list
        client_list = []
        for client in share.trustedNFSClients:
            if client.accessLevel == "ReadWrite":
                client_list.append(edge_types.NFSv3AccessControlEntry(
                    client.address, client.netmask, edge_enum.FileAccessMode.RW
                ))
            elif client.accessLevel == "ReadOnly":
                client_list.append(edge_types.NFSv3AccessControlEntry(
                    client.address, client.netmask, edge_enum.FileAccessMode.RO
                ))

        # Build ACL entries
        acl_entries = _build_acl_entries(share)

        # Get share properties with defaults
        share_directory = share.directory[1:] if share.directory else ""
        share_access = share.access if share.access is not None else []
        share_comment = share.comment if share.comment is not None else ""

        # Create the share with NFS settings
        dest_filer.shares.add(
            share.name,
            share_directory,
            acl=None,
            access=share_access,
            dir_permissions=777,
            comment=share_comment,
            export_to_nfs=True,
            trusted_nfs_clients=client_list
        )

        # Add ACL entries one at a time
        _add_acl_entries(dest_filer, share.name, acl_entries)

        logging.info("Successfully copied NFS share: %s", share.name)
    except Exception as e:
        logging.warning("Error copying NFS share %s: %s", share.name, e)


def _build_acl_entries(share) -> list:
    """Build ACL entries from share."""
    acl_entries = []

    if not hasattr(share, 'acl') or share.acl is None:
        return acl_entries

    for acl in share.acl:
        try:
            logging.debug("Processing ACL entry: %s", acl)

            name = None
            classname = acl.principal2._classname

            if classname == "LocalUser":
                name = acl.principal2.ref.split("#")[-1]
                logging.debug("LocalUser: %s", name)
            elif classname == "DomainUser":
                name = acl.principal2.name
                logging.debug("DomainUser: %s", name)
            elif classname == "LocalGroup":
                name = acl.principal2.ref.split("#")[-1]
                logging.debug("LocalGroup: %s", name)
            elif classname == "DomainGroup":
                name = acl.principal2.name
                logging.debug("DomainGroup: %s", name)
            else:
                logging.error("Unknown principal type: %s", classname)
                continue

            entry = edge_types.ShareAccessControlEntry(
                PRINCIPAL_DICT[classname],
                name,
                PERM_DICT[acl.permissions.allowedFileAccess]
            )
            acl_entries.append(entry)
        except Exception as e:
            logging.debug("Error processing ACL entry: %s", e)

    return acl_entries


def _add_acl_entries(dest_filer, share_name: str, acl_entries: list) -> None:
    """Add ACL entries to a share one at a time."""
    logging.info("Number of ACL entries to add: %d", len(acl_entries))

    for entry in acl_entries:
        try:
            dest_filer.shares.add_acl(share_name, [entry])
            logging.info("Successfully added ACL entry %s to share %s", entry.name, share_name)
        except Exception as e:
            logging.warning("Failed to add ACL entry %s to share %s", entry.name, share_name)
            logging.warning("This could be due to the destination filer not having the same local users/groups.")
            logging.debug("Error: %s", e)


def copy_shares(
    source_ip: str,
    source_username: str,
    source_password: str,
    dest_ip: str,
    dest_username: str,
    dest_password: str
) -> None:
    """
    Copy shares from source device to destination device.

    Args:
        source_ip: Source device IP address or hostname
        source_username: Source device admin username
        source_password: Source device admin password
        dest_ip: Destination device IP address or hostname
        dest_username: Destination device admin username
        dest_password: Destination device admin password
    """
    logging.info("Starting copy shares task.")

    settings.sessions.management.ssl = False

    source = None
    dest = None

    try:
        # Connect to source device
        logging.info("Connecting to source device: %s", source_ip)
        source = Edge(source_ip)
        source.login(source_username, source_password)

        # Connect to destination device
        logging.info("Connecting to destination device: %s", dest_ip)
        dest = Edge(dest_ip)
        dest.login(dest_username, dest_password)

        # Get shares from source
        source_shares = source.shares.get()
        logging.info("Found %d shares on source device", len(source_shares))

        for share in source_shares:
            logging.info("Processing share: %s", share.name)

            # Skip system shares
            if share.name in SKIP_SHARES:
                logging.info("Skipping system share: %s", share.name)
                continue

            # Handle NFS shares separately
            if getattr(share, 'exportToNFS', False):
                logging.info("Copying NFS share: %s", share.name)
                _copy_nfs_share(share, dest)
                continue

            try:
                # Build ACL entries
                acl_entries = _build_acl_entries(share)

                # Get share properties with defaults
                share_directory = share.directory[1:] if share.directory else ""
                share_access = share.access if share.access is not None else []
                share_comment = share.comment if share.comment is not None else ""

                logging.info("Share Name: %s", share.name)
                logging.info("Share Directory: %s", share_directory)
                logging.debug("Share Access: %s", share_access)
                logging.debug("Share Comment: %s", share_comment)

                # Create the share (without ACL first, then add ACLs individually)
                dest.shares.add(
                    share.name,
                    share_directory,
                    acl=None,
                    access=share_access,
                    dir_permissions=777,
                    comment=share_comment
                )
                logging.info("Successfully added share %s to destination", share.name)

                # Add ACL entries one at a time
                _add_acl_entries(dest, share.name, acl_entries)

            except Exception as e:
                logging.warning("Error copying share %s: %s", share.name, e)

        logging.info("Finished copy shares task.")
    except Exception as e:
        logging.error("Error in copy shares task: %s", e)
        raise
    finally:
        # Logout from devices
        if source:
            try:
                source.logout()
            except:
                pass
        if dest:
            try:
                dest.logout()
            except:
                pass
