"""Authentication utilities for CTERA Portal."""

import logging
import sys
from io import StringIO
from typing import Optional

import urllib3
from cterasdk import GlobalAdmin, CTERAException, settings


def global_admin_login(
    address: str,
    username: str,
    password: str,
    ignore_cert: bool = False
) -> Optional[GlobalAdmin]:
    """
    Log into CTERA Portal and return GlobalAdmin session.

    Args:
        address: Portal IP, hostname, or FQDN
        username: Global admin username
        password: Global admin password
        ignore_cert: If True, ignore SSL certificate warnings

    Returns:
        GlobalAdmin session object, or None if login fails
    """
    if ignore_cert:
        settings.sessions.management.ssl = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # If prompted for untrusted cert, answer no
    sys.stdin = StringIO('n')

    try:
        logging.info("Logging into %s", address)
        global_admin = GlobalAdmin(address)
        global_admin.login(username, password)
        logging.debug("Successfully logged in to %s", address)
        return global_admin
    except CTERAException as error:
        logging.error(
            "Login failed. Verify credentials and certificate settings. Error: %s",
            error
        )
        return None


def enable_device_sso(admin: GlobalAdmin) -> bool:
    """
    Enable Single Sign On to devices for read-write admins.

    Args:
        admin: Authenticated GlobalAdmin session

    Returns:
        True if successful, False otherwise
    """
    try:
        admin.portals.browse_global_admin()
        admin.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')
        return True
    except Exception as e:
        logging.warning("Failed to enable device SSO: %s", e)
        return False
