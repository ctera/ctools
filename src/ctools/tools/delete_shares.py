"""Delete shares tool - Delete shares based on substring match."""

import csv
import logging
from typing import Any, List, Tuple

from cterasdk import CTERAException

from ..core.filer import get_filers


def find_shares_to_delete(session: Any, substring: str) -> List[Tuple[Any, List[Any]]]:
    """
    Find all shares matching a substring across all filers.

    Args:
        session: Authenticated GlobalAdmin session
        substring: Substring to match in share names

    Returns:
        List of tuples (filer, [shares]) containing matching shares
    """
    logging.info("Searching for shares containing: %s", substring)

    results = []
    filers = get_filers(session, all_tenants=True)

    if not filers:
        logging.warning("No filers found")
        return results

    for filer in filers:
        try:
            shares = filer.api.get('/config/fileservices/share')
            matching_shares = []

            for share in shares:
                if isinstance(share.name, str) and substring in share.name:
                    matching_shares.append(share)
                    logging.info("Found matching share: %s on %s", share.name, filer.name)

            if matching_shares:
                results.append((filer, matching_shares))

        except Exception as e:
            logging.warning("Error getting shares from %s: %s", filer.name, e)

    logging.info("Found %d filers with matching shares", len(results))
    return results


def delete_shares(
    session: Any,
    substring: str,
    output_file: str = "deleted_shares.csv"
) -> List[Tuple[str, str, str]]:
    """
    Delete shares matching a substring (returns list for confirmation).

    Args:
        session: Authenticated GlobalAdmin session
        substring: Substring to match in share names
        output_file: CSV file to log deletions

    Returns:
        List of tuples (filer_name, share_name, status) for each deletion
    """
    logging.info("Starting delete shares task.")
    logging.info("Searching for shares containing: %s", substring)

    results = []
    filers = get_filers(session, all_tenants=True)

    if not filers:
        logging.warning("No filers found")
        return results

    # Create/check CSV file for logging
    try:
        with open(output_file, 'a+', newline='', encoding='utf-8') as f:
            f.seek(0)
            writer = csv.writer(f)
            if f.read() == '':
                writer.writerow(['FilerName', 'ShareName', 'Status'])
    except Exception as e:
        logging.warning("Could not initialize output file: %s", e)

    for filer in filers:
        try:
            shares = filer.api.get('/config/fileservices/share')

            for share in shares:
                if isinstance(share.name, str) and substring in share.name:
                    try:
                        filer.shares.delete(share.name)
                        logging.info("Deleted share %s from %s", share.name, filer.name)
                        status = 'Deleted'
                    except CTERAException as error:
                        logging.warning("Failed to delete share %s from %s: %s", share.name, filer.name, error)
                        status = 'NotDeleted'

                    results.append((filer.name, share.name, status))

                    # Log to CSV
                    try:
                        with open(output_file, 'a', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow([filer.name, share.name, status])
                    except Exception as e:
                        logging.warning("Could not write to output file: %s", e)

        except Exception as e:
            logging.warning("Error processing filer %s: %s", filer.name, e)

    logging.info("Finished delete shares task. Processed %d shares.", len(results))
    return results
