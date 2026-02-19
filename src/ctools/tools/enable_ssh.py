"""Enable SSH on CTERA filers."""

import logging
from typing import Any, Optional

from ..core.filer import get_filer, get_filers


def enable_ssh(
    session: Any,
    public_key: str,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Enable SSH on filers.

    Args:
        session: Authenticated GlobalAdmin session
        public_key: SSH public key to authorize
        tenant: Optional tenant name
        device: Optional device name (enables on single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info("Starting enable SSH task.")

    try:
        if device:
            filer = get_filer(session, device, tenant)
            if filer:
                _enable_ssh_on_filer(filer, public_key)
        else:
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _enable_ssh_on_filer(filer, public_key)

            logging.info("Finished enable SSH task.")
    except Exception as e:
        logging.warning("An error occurred: %s", e)


def _enable_ssh_on_filer(filer: Any, public_key: str) -> None:
    """Enable SSH on a single filer."""
    try:
        filer.ssh.enable(public_key)
        logging.info("Enabled SSH on %s", filer.name)
    except Exception as e:
        logging.warning("Error enabling SSH on %s: %s", filer.name, e)
