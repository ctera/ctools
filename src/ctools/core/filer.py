"""Filer utilities for CTERA operations."""

import logging
import re
from typing import Optional, List, Any

from cterasdk import CTERAException


def safe_cli_command(filer: Any, command: str) -> str:
    """
    Execute CLI command and ensure result is a string.
    Handles SDK 7.11+ changes where CLI output format may differ.

    Args:
        filer: Filer object
        command: CLI command to execute

    Returns:
        String output or 'Not Applicable' on failure
    """
    try:
        result = filer.cli.run_command(command)

        if isinstance(result, str):
            return result

        if hasattr(result, 'value'):
            return str(result.value)
        if hasattr(result, 'text'):
            return str(result.text)
        if hasattr(result, '__str__'):
            return str(result)

        return str(result) if result is not None else 'Not Applicable'
    except AttributeError:
        return 'Not Applicable'
    except Exception as e:
        logging.debug("CLI command failed: %s, error: %s", command, e)
        return 'Not Applicable'


def get_portal_name(filer: Any) -> str:
    """
    Extract clean portal/tenant name from filer object.
    Handles SDK 7.11+ where filer.portal returns object reference paths.

    Args:
        filer: Filer object

    Returns:
        Clean tenant/portal name string
    """
    try:
        portal = filer.portal

        if isinstance(portal, str):
            if '/' in portal:
                # Handle format like "objs/9//TeamPortal/portal"
                match = re.search(r'/([^/]+)/portal$', portal)
                if match:
                    return match.group(1)

                # Get named parts, excluding 'objs', 'portal', and numeric IDs
                parts = [p for p in portal.split('/') if p and p != 'objs' and p != 'portal']
                named_parts = [p for p in parts if not p.isdigit()]
                if named_parts:
                    return named_parts[-1]

            return portal

        if hasattr(portal, 'name'):
            return portal.name
        if hasattr(portal, 'tenant'):
            return portal.tenant

        return str(portal)
    except Exception as e:
        logging.debug("Failed to get portal name: %s", e)
        return 'Unknown'


def get_current_tenant(portal_session: Any) -> Optional[str]:
    """
    Get current tenant from session, handling different SDK versions.

    Args:
        portal_session: Portal session object (GlobalAdmin)

    Returns:
        Current tenant name or None if unable to determine
    """
    session = portal_session.users.session()

    # Try current_tenant() method first (7.11+)
    if hasattr(session, 'current_tenant') and callable(getattr(session, 'current_tenant', None)):
        try:
            return session.current_tenant()
        except Exception:
            pass

    # Try 7.11+ structure - tenant property
    if hasattr(session, 'tenant'):
        return session.tenant

    # Fall back to older structure
    if hasattr(session, 'user') and hasattr(session.user, 'tenant'):
        return session.user.tenant

    # Try other common patterns
    if hasattr(session, 'currentTenant'):
        return session.currentTenant

    logging.warning("Could not determine tenant. Session attrs: %s", dir(session))
    return None


def get_filer(portal_session: Any, device: str, tenant: Optional[str] = None) -> Optional[Any]:
    """
    Get a specific filer device.

    Args:
        portal_session: Portal session object
        device: Device name
        tenant: Optional tenant name

    Returns:
        Filer object or None if not found
    """
    try:
        return portal_session.devices.device(device, tenant)
    except CTERAException as error:
        logging.debug(error)
        logging.error("Device not found: %s", device)
        return None


def get_filers(
    portal_session: Any,
    all_tenants: bool = False,
    tenant: Optional[str] = None
) -> Optional[List[Any]]:
    """
    Get all connected filers from the portal.

    Args:
        portal_session: Portal session object
        all_tenants: If True, get filers from all tenants
        tenant: Specific tenant name (ignored if all_tenants is True)

    Returns:
        List of connected filer objects or None on error
    """
    try:
        connected_filers = []
        include_fields = [
            'deviceConnectionStatus.connected',
            'deviceReportedStatus.config.hostname'
        ]

        if all_tenants:
            portal_session.portals.browse_global_admin()
            current = get_current_tenant(portal_session)
            logging.info("Getting all Filers (current tenant: %s)", current)

            for portal_tenant in portal_session.portals.tenants():
                portal_session.portals.browse(portal_tenant.name)
                tenant_filers = portal_session.devices.filers(include=include_fields)
                connected_filers.extend([
                    f for f in tenant_filers
                    if f.deviceConnectionStatus.connected
                ])
        elif tenant:
            logging.info("Getting Filers connected to %s", tenant)
            portal_session.portals.browse(tenant)
            tenant_filers = portal_session.devices.filers(include=include_fields)
            connected_filers.extend([
                f for f in tenant_filers
                if f.deviceConnectionStatus.connected
            ])
        else:
            current_tenant = get_current_tenant(portal_session)
            logging.info("Getting Filers connected to %s", current_tenant)
            tenant_filers = portal_session.devices.filers(include=include_fields)
            connected_filers.extend([
                f for f in tenant_filers
                if f.deviceConnectionStatus.connected
            ])

        return connected_filers
    except CTERAException as error:
        logging.debug(error)
        logging.error("Error getting Filers.")
        return None
