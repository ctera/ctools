"""Suspend cloud sync on CTERA filers."""

import logging
from typing import Any, Optional

from ..core.filer import get_filer, get_filers


def suspend_sync(
    session: Any,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Suspend cloud sync on filers.

    Args:
        session: Authenticated GlobalAdmin session
        tenant: Optional tenant name
        device: Optional device name (suspends single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info("Starting suspend sync task.")

    try:
        if device:
            filer = get_filer(session, device, tenant)
            if filer:
                _suspend_filer(filer)
        else:
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _suspend_filer(filer)

            logging.info("Finished suspend sync task.")
    except Exception as e:
        logging.warning("An error occurred: %s", e)


def _suspend_filer(filer: Any) -> None:
    """Suspend sync on a single filer."""
    try:
        filer.sync.suspend(wait=True)
        logging.info("Suspended sync on %s", filer.name)
    except Exception as e:
        logging.warning("Error suspending sync on %s: %s", filer.name, e)
