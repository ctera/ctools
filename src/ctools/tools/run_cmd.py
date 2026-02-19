"""Run CLI commands on CTERA filers."""

import logging
from typing import Any, Optional

from cterasdk import CTERAException

from ..core.filer import get_filer, get_filers


def run_cmd(
    session: Any,
    command: str,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Run a CLI command on connected filers.

    Args:
        session: Authenticated GlobalAdmin session
        command: CLI command to execute
        tenant: Optional tenant name
        device: Optional device name (runs on single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info('Starting run_cmd task.')

    try:
        if device:
            # Single device mode
            filer = get_filer(session, device, tenant)
            if filer:
                _run_on_filer(filer, command)
        else:
            # Multi-filer mode
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _run_on_filer(filer, command)

            logging.info('Finished run_cmd task on all filers.')
    except Exception as e:
        logging.warning("An error occurred: %s", e)


def _run_on_filer(filer: Any, command: str) -> None:
    """Execute command on a single filer."""
    try:
        logging.info("Running command on: %s", filer.name)
        response = filer.cli.run_command(command)
        logging.info(response)
        logging.info("Finished command on: %s", filer.name)
    except CTERAException as error:
        logging.debug(error)
        logging.warning("Failed to run command on %s", filer.name)
    except AttributeError as error:
        logging.debug(error)
        logging.warning("Command execution error on %s", filer.name)
