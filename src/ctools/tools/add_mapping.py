"""Add domain to advanced mapping on CTERA filers."""

import logging
from typing import Any, Optional

from cterasdk import common_types

from ..core.filer import get_filer, get_filers


def add_mapping(
    session: Any,
    domain: str,
    tenant: Optional[str] = None,
    device: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Add domain to advanced ID mapping on filers.

    Args:
        session: Authenticated GlobalAdmin session
        domain: Domain name to add
        tenant: Optional tenant name
        device: Optional device name (adds on single device if provided)
        all_tenants: If True and no device specified, run on all tenants
    """
    logging.info("Starting add mapping task.")

    try:
        if device:
            filer = get_filer(session, device, tenant)
            if filer:
                _add_mapping_to_filer(filer, domain)
        else:
            filers = get_filers(session, all_tenants, tenant)
            if filers:
                for filer in filers:
                    _add_mapping_to_filer(filer, domain)

        logging.info("Finished add mapping task.")
    except Exception as e:
        logging.warning("An error occurred: %s", e)


def _get_advanced_mapping(filer: Any) -> tuple:
    """
    Get current advanced ID mapping from filer.

    Returns:
        Tuple of (mappings list, highest_id)
    """
    highest_id = 0
    mappings = []

    mapping_dict = filer.directoryservice.get_advanced_mapping()
    for domain_name, mapping in mapping_dict.items():
        logging.debug("Domain: %s, Mapping: %s", domain_name, mapping)
        if mapping.maxID > highest_id:
            highest_id = mapping.maxID
        mappings.append(mapping)

    return mappings, highest_id


def _add_mapping_to_filer(filer: Any, domain: str) -> None:
    """Add domain mapping to a single filer."""
    try:
        # Get current mappings and highest ID
        mappings, highest_id = _get_advanced_mapping(filer)
        logging.info("Current mappings on %s: %d domains, highest ID: %d",
                     filer.name, len(mappings), highest_id)

        # Check if domain already exists
        existing_domains = [m.domainFlatName for m in mappings]
        if domain.upper() in [d.upper() for d in existing_domains]:
            logging.warning("Domain %s already has mapping on %s, skipping", domain, filer.name)
            return

        # Add new domain mapping with ID range of 200000
        new_mapping = common_types.ADDomainIDMapping(domain, highest_id + 1, highest_id + 200000)
        mappings.append(new_mapping)

        logging.info("Adding mapping for domain %s on %s (ID range: %d - %d)",
                     domain, filer.name, highest_id + 1, highest_id + 200000)

        # Set all mappings
        filer.directoryservice.set_advanced_mapping(mappings)
        logging.info("Successfully added domain mapping %s on %s", domain, filer.name)
    except Exception as e:
        logging.warning("Error adding mapping on %s: %s", filer.name, e)
