"""Generate shares report for CTERA filers."""

import csv
import logging
from typing import Any, Optional

from ..core.filer import get_filer, get_filers


def shares_report(
    session: Any,
    filename: str,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Generate shares report.

    Args:
        session: Authenticated GlobalAdmin session
        filename: Output CSV filename
        tenant: Optional tenant name
        device: Optional device name (reports single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info("Starting shares report task.")

    try:
        if device:
            filers = [get_filer(session, device, tenant)]
            filers = [f for f in filers if f]  # Filter None
        elif tenant:
            filers = get_filers(session, all_tenants=False, tenant=tenant)
        else:
            filers = get_filers(session, all_tenants=all_tenants)

        if not filers:
            logging.warning("No filers found")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Share Name', 'Share Path', 'Edge Filer Name', 'Edge Filer IP', 'ACL Permissions'])

            for filer in filers:
                _write_filer_shares(writer, filer)

        logging.info("Shares report saved to %s", filename)
    except Exception as e:
        logging.error("Error generating shares report: %s", e)

    logging.info("Finished shares report task.")


def _get_principal_name(acl_entry: Any) -> tuple:
    """Extract a readable name and type from an ACL principal."""
    principal = acl_entry.principal2
    classname = principal._classname

    if classname in ("LocalUser", "LocalGroup"):
        name = principal.ref.split("#")[-1]
    elif classname in ("DomainUser", "DomainGroup"):
        name = principal.name
    else:
        name = str(principal)

    return name, classname


def _format_acl(share: Any) -> str:
    """Format all ACL entries for a share into a single string."""
    if not hasattr(share, 'acl') or not share.acl:
        return ''

    entries = []
    for acl_entry in share.acl:
        try:
            name, principal_type = _get_principal_name(acl_entry)
            permission = acl_entry.permissions.allowedFileAccess
            entries.append(f"{principal_type}: {name} ({permission})")
        except Exception as e:
            logging.debug("Error reading ACL entry: %s", e)

    return "; ".join(entries)


def _write_filer_shares(writer: csv.writer, filer: Any) -> None:
    """Write shares for a single filer."""
    try:
        shares = filer.shares.get()
        ip_address = _get_filer_ip(filer)

        for share in shares:
            logging.info("Writing %s stats to file", share.name)
            acl_str = _format_acl(share)
            writer.writerow([
                share.name,
                getattr(share, 'directory', 'N/A'),
                filer.name,
                ip_address,
                acl_str
            ])
    except Exception as e:
        logging.warning("Error getting shares for %s: %s", filer.name, e)


def _get_filer_ip(filer: Any) -> str:
    """Get filer IP address."""
    try:
        return filer.network.ipconfig().ip.address
    except Exception:
        return 'N/A'
