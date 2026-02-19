"""Resume cloud sync on CTERA filers."""

import logging
from typing import Any, Optional

from ..core.filer import get_filer, get_filers


def unsuspend_sync(
    session: Any,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Resume cloud sync on filers.

    Args:
        session: Authenticated GlobalAdmin session
        tenant: Optional tenant name
        device: Optional device name (resumes single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info("Starting unsuspend sync task.")

    try:
        if device:
            filer = get_filer(session, device, tenant)
            if filer:
                _unsuspend_filer(filer)
        else:
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _unsuspend_filer(filer)

            logging.info("Finished unsuspend sync task.")
    except Exception as e:
        logging.warning("An error occurred: %s", e)


def _unsuspend_filer(filer: Any) -> None:
    """Resume sync on a single filer."""
    try:
        filer.sync.unsuspend()
        logging.info("Resumed sync on %s", filer.name)
    except Exception as e:
        logging.warning("Error resuming sync on %s: %s", filer.name, e)
