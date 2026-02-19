"""Enable telnet on CTERA filers."""

import hashlib
import logging
from typing import Any, Optional

from ..core.filer import get_filer, get_filers


def enable_telnet(
    session: Any,
    code: str,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Enable telnet on filers.

    Args:
        session: Authenticated GlobalAdmin session
        code: Authorization code for telnet access
        tenant: Optional tenant name
        device: Optional device name (enables on single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info("Starting enable telnet task.")

    try:
        if device:
            filer = get_filer(session, device, tenant)
            if filer:
                _enable_telnet_on_filer(filer, code)
        else:
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _enable_telnet_on_filer(filer, code)

            logging.info("Finished enable telnet task.")
    except Exception as e:
        logging.warning("An error occurred: %s", e)


def _enable_telnet_on_filer(filer: Any, code: str) -> None:
    """Enable telnet on a single filer."""
    try:
        filer.telnet.enable(code)
        logging.info("Enabled telnet on %s", filer.name)
    except Exception as e:
        logging.warning("Error enabling telnet on %s: %s", filer.name, e)
