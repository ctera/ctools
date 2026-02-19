"""Create shares from CSV - Create shares with ACL entries on a CTERA filer."""

import csv
import logging
from collections import OrderedDict
from typing import Any, Optional

from cterasdk import edge_types, edge_enum, CTERAException

from ..core.filer import get_filer

# Mapping from CSV type strings to cterasdk principal type enums
PRINCIPAL_TYPE_MAP = {
    "DomainUser": edge_enum.PrincipalType.DU,
    "DomainGroup": edge_enum.PrincipalType.DG,
    "LocalUser": edge_enum.PrincipalType.LU,
    "LocalGroup": edge_enum.PrincipalType.LG,
}

# Mapping from CSV permission strings to cterasdk file access mode enums
PERMISSION_MAP = {
    "RW": edge_enum.FileAccessMode.RW,
    "RO": edge_enum.FileAccessMode.RO,
    "NA": edge_enum.FileAccessMode.NA,
}


def _parse_acl_string(acl_string: str, row_num: int) -> list:
    """
    Parse the acl column string into a list of ACL row dicts.

    Format: "type:name:permission" entries separated by semicolons.
    Example: "DomainGroup:CTERA\\Domain Admins:RW;LocalUser:admin:RO"
    """
    acl_rows = []
    if not acl_string:
        return acl_rows

    for entry in acl_string.split(';'):
        entry = entry.strip()
        if not entry:
            continue

        parts = entry.split(':')
        if len(parts) != 3:
            logging.warning(
                "Row %d: Invalid ACL entry '%s'. Expected format 'type:name:permission'. Skipping.",
                row_num, entry
            )
            continue

        acl_type, acl_name, acl_permission = [p.strip() for p in parts]

        if acl_type not in PRINCIPAL_TYPE_MAP:
            logging.warning(
                "Row %d: Invalid type '%s'. Must be one of: %s. Skipping ACL entry.",
                row_num, acl_type, ', '.join(PRINCIPAL_TYPE_MAP.keys())
            )
            continue

        acl_permission_upper = acl_permission.upper()
        if acl_permission_upper not in PERMISSION_MAP:
            logging.warning(
                "Row %d: Invalid permission '%s'. Must be one of: %s. Skipping ACL entry.",
                row_num, acl_permission, ', '.join(PERMISSION_MAP.keys())
            )
            continue

        acl_rows.append({
            "type": acl_type,
            "name": acl_name,
            "permission": acl_permission_upper,
        })

    return acl_rows


def _parse_csv(filepath: str) -> OrderedDict:
    """
    Parse the CSV file. One row per share.

    CSV columns: share_name, path, comment, acl
    The acl column contains semicolon-separated entries in the format:
      type:name:permission;type:name:permission;...

    Returns an OrderedDict where:
      key = share_name
      value = dict with keys: path, comment, acl_rows
    """
    shares = OrderedDict()

    with open(filepath, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        required_columns = {'share_name', 'path'}
        if not required_columns.issubset(set(csv_reader.fieldnames or [])):
            missing = required_columns - set(csv_reader.fieldnames or [])
            raise ValueError(f"CSV missing required columns: {', '.join(missing)}")

        for row_num, row in enumerate(csv_reader, start=2):
            share_name = row.get('share_name', '').strip()
            path = row.get('path', '').strip()
            comment = row.get('comment', '').strip()
            acl_string = row.get('acl', '').strip()

            if not share_name:
                logging.warning("Row %d: Missing share_name, skipping row", row_num)
                continue

            if not path:
                logging.warning("Row %d: Missing path for share '%s', skipping row", row_num, share_name)
                continue

            if share_name in shares:
                logging.warning("Row %d: Duplicate share_name '%s', skipping row", row_num, share_name)
                continue

            acl_rows = _parse_acl_string(acl_string, row_num)

            shares[share_name] = {
                "path": path,
                "comment": comment,
                "acl_rows": acl_rows,
            }

    return shares


def _build_acl_entry(acl_row: dict) -> edge_types.ShareAccessControlEntry:
    """Build a single ShareAccessControlEntry from a parsed ACL row."""
    return edge_types.ShareAccessControlEntry(
        PRINCIPAL_TYPE_MAP[acl_row["type"]],
        acl_row["name"],
        PERMISSION_MAP[acl_row["permission"]],
    )


def create_shares_from_csv(
    session: Any,
    device: str,
    filepath: str,
    tenant: Optional[str] = None,
    exclude_everyone_rw: bool = False,
) -> None:
    """
    Create shares with ACL entries on a filer from a CSV file.

    Args:
        session: Authenticated GlobalAdmin session
        device: Name of the target filer device
        filepath: Path to CSV file with share definitions
        tenant: Optional tenant name
        exclude_everyone_rw: If False (default), auto-add Everyone RW to each share.
                             If True, do not add Everyone RW automatically.
    """
    logging.info("Starting create shares from CSV task.")

    # Parse CSV
    logging.info("Reading CSV file: %s", filepath)
    shares = _parse_csv(filepath)

    if not shares:
        logging.warning("No shares found in CSV file.")
        return

    logging.info("Found %d share(s) to create.", len(shares))

    # Get the filer device
    logging.info("Connecting to device: %s", device)
    filer = get_filer(session, device, tenant)
    if not filer:
        raise Exception(f"Device not found: {device}")

    # Process each share
    created_count = 0
    failed_count = 0

    for share_name, share_data in shares.items():
        path = share_data["path"]
        comment = share_data["comment"]
        acl_rows = share_data["acl_rows"]

        logging.info("Creating share: %s (path: %s)", share_name, path)

        # Create the share without ACL first
        try:
            filer.shares.add(
                share_name,
                path,
                acl=None,
                access=edge_enum.Acl.WindowsNT,
                dir_permissions=777,
                comment=comment or None,
            )
            logging.info("Successfully created share: %s", share_name)
            created_count += 1
        except CTERAException as e:
            logging.error("Failed to create share '%s': %s", share_name, e)
            failed_count += 1
            continue
        except Exception as e:
            logging.error("Unexpected error creating share '%s': %s", share_name, e)
            failed_count += 1
            continue

        # Add Everyone RW unless excluded
        if not exclude_everyone_rw:
            # Check if Everyone is already in the CSV ACL entries
            has_everyone = any(
                r["type"] == "LocalGroup" and r["name"].lower() == "everyone"
                for r in acl_rows
            )
            if not has_everyone:
                try:
                    everyone_entry = edge_types.ShareAccessControlEntry(
                        edge_enum.PrincipalType.LG, "Everyone", edge_enum.FileAccessMode.RW
                    )
                    filer.shares.add_acl(share_name, [everyone_entry])
                    logging.info("Added default ACL: Everyone RW to share %s", share_name)
                except Exception as e:
                    logging.warning("Failed to add Everyone RW to share %s: %s", share_name, e)
        else:
            logging.info("Excluding default Everyone RW for share: %s", share_name)

        # Add ACL entries one at a time
        if acl_rows:
            logging.info("Adding %d ACL entry/entries to share: %s", len(acl_rows), share_name)

            for acl_row in acl_rows:
                try:
                    entry = _build_acl_entry(acl_row)
                    filer.shares.add_acl(share_name, [entry])
                    logging.info(
                        "Added ACL: %s %s (%s) to share %s",
                        acl_row["type"], acl_row["name"],
                        acl_row["permission"], share_name
                    )
                except Exception as e:
                    logging.warning(
                        "Failed to add ACL entry %s %s to share %s: %s",
                        acl_row["type"], acl_row["name"], share_name, e
                    )
                    logging.warning(
                        "This could be due to the filer not having the user/group configured."
                    )
        else:
            logging.info("No ACL entries for share: %s", share_name)

    logging.info(
        "Finished create shares from CSV task. Created: %d, Failed: %d",
        created_count, failed_count
    )
