"""Disable SSH on CTERA filers."""

import logging
from typing import Any, Optional

from ..core.filer import get_filer, get_filers


def disable_ssh(
    session: Any,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Disable SSH on filers.

    Args:
        session: Authenticated GlobalAdmin session
        tenant: Optional tenant name
        device: Optional device name (disables on single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info("Starting disable SSH task.")

    try:
        if device:
            filer = get_filer(session, device, tenant)
            if filer:
                _disable_ssh_on_filer(filer)
        else:
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _disable_ssh_on_filer(filer)

            logging.info("Finished disable SSH task.")
    except Exception as e:
        logging.warning("An error occurred: %s", e)


def _disable_ssh_on_filer(filer: Any) -> None:
    """Disable SSH on a single filer."""
    try:
        filer.ssh.disable()
        logging.info("Disabled SSH on %s", filer.name)
    except Exception as e:
        logging.warning("Error disabling SSH on %s: %s", filer.name, e)
