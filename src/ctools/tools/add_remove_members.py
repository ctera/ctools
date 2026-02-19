"""Add/Remove members tool - Manage Administrators group membership on filers."""

import logging
from typing import Any, Optional

from cterasdk import CTERAException, edge_types, edge_enum, settings

from ..core.filer import get_filer, get_filers


def add_remove_members(
    session: Any,
    operation: str,
    user: Optional[str] = None,
    group: Optional[str] = None,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Add or remove domain users/groups to/from Administrators group on filers.

    Args:
        session: Authenticated GlobalAdmin session
        operation: "Add" or "Remove"
        user: Domain user to add/remove (format: domain\\user or just user)
        group: Domain group to add/remove (format: domain\\group or just group)
        tenant: Optional tenant name
        device: Optional device name
        all_tenants: If True, run on all tenants
    """
    logging.info("Starting add/remove members task.")
    logging.info("Operation: %s, User: %s, Group: %s", operation, user, group)

    if not user and not group:
        logging.error("No user or group specified")
        return

    settings.sessions.management.ssl = False
    error_string = ""

    try:
        # Get filers based on scope
        if device:
            filers = [get_filer(session, device, tenant)]
            filers = [f for f in filers if f is not None]
        elif all_tenants:
            filers = get_filers(session, all_tenants=True)
        elif tenant:
            filers = get_filers(session, False, tenant=tenant)
        else:
            logging.error("No device name, tenant name, or all_tenants flag specified")
            return

        if not filers:
            logging.error("No devices found")
            return

        for filer in filers:
            try:
                if operation == "Add":
                    _add_member(filer, user, group, error_string)
                elif operation == "Remove":
                    _remove_member(filer, user, group, error_string)
                else:
                    logging.error("Unknown operation: %s", operation)
                    return
            except Exception as e:
                error_string += f"Error on {filer.name}: {e}\n"
                logging.warning("Error processing filer %s: %s", filer.name, e)

        if error_string:
            logging.error("Errors occurred during operation:\n%s", error_string)

        logging.info("Finished add/remove members task.")

    except CTERAException as error:
        logging.error("CTERA error: %s", error)
        raise


def _add_member(filer: Any, user: Optional[str], group: Optional[str], error_string: str) -> None:
    """Add a user or group to Administrators on a filer."""
    if user:
        domain_user = edge_types.UserGroupEntry(edge_enum.PrincipalType.DU, user)
        try:
            filer.groups.add_members('Administrators', [domain_user])
            logging.info("Added user '%s' to Administrators on %s", user, filer.name)
        except Exception as e:
            error_string += f"Failed to add user on {filer.name}: {e}\n"
            logging.warning("Failed to add user on %s: %s", filer.name, e)

    if group:
        domain_group = edge_types.UserGroupEntry(edge_enum.PrincipalType.DG, group)
        try:
            filer.groups.add_members('Administrators', [domain_group])
            logging.info("Added group '%s' to Administrators on %s", group, filer.name)
        except Exception as e:
            error_string += f"Failed to add group on {filer.name}: {e}\n"
            logging.warning("Failed to add group on %s: %s", filer.name, e)


def _remove_member(filer: Any, user: Optional[str], group: Optional[str], error_string: str) -> None:
    """Remove a user or group from Administrators on a filer."""
    if user:
        domain_user = edge_types.UserGroupEntry(edge_enum.PrincipalType.DU, user)
        try:
            filer.groups.remove_members('Administrators', [domain_user])
            logging.info("Removed user '%s' from Administrators on %s", user, filer.name)
        except Exception as e:
            error_string += f"Failed to remove user on {filer.name}: {e}\n"
            logging.warning("Failed to remove user on %s: %s", filer.name, e)

    if group:
        domain_group = edge_types.UserGroupEntry(edge_enum.PrincipalType.DG, group)
        try:
            filer.groups.remove_members('Administrators', [domain_group])
            logging.info("Removed group '%s' from Administrators on %s", group, filer.name)
        except Exception as e:
            error_string += f"Failed to remove group on {filer.name}: {e}\n"
            logging.warning("Failed to remove group on %s: %s", filer.name, e)
