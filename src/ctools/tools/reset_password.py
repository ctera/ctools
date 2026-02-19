"""Reset password on CTERA filers."""

import logging
from typing import Any, Optional

from cterasdk import CTERAException

from ..core.filer import get_filer, get_filers


def reset_password(
    session: Any,
    new_password: str,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False,
    username: str = "admin"
) -> None:
    """
    Reset local user password on filers.

    Args:
        session: Authenticated GlobalAdmin session
        new_password: New password to set
        tenant: Optional tenant name
        device: Optional device name (resets single device if provided)
        all_tenants: If True and no device specified, run on all tenants
        username: Local username to reset (default: admin)
    """
    logging.info("Starting reset_password task.")

    try:
        if device:
            filer = get_filer(session, device, tenant)
            if filer:
                _reset_filer_password(filer, username, new_password)
        else:
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _reset_filer_password(filer, username, new_password)

            logging.info("Finished reset_password task.")
    except CTERAException as error:
        logging.debug(error)
        logging.error(
            "Failed reset_password task. Ensure password is 8+ characters "
            "with at least one letter, digit, and special character."
        )


def _reset_filer_password(filer: Any, username: str, password: str) -> None:
    """Reset password on a single filer."""
    try:
        filer.users.modify(username, password)
        logging.info("Password set for %s on %s", username, filer.name)
    except Exception as e:
        logging.warning("Error resetting password on %s: %s", filer.name, e)
