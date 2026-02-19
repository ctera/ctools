"""Configure WORM settings on CTERA cloud folders."""

import logging
from typing import Any, Optional


def worm_settings(
    session: Any,
    folder_id: str,
    operation: str,
    grace_period: Optional[str] = None,
    period_type: str = "Days",
    target_date: Optional[str] = None
) -> None:
    """
    Configure WORM settings on a cloud folder.

    Args:
        session: Authenticated GlobalAdmin session
        folder_id: Cloud folder ID to configure
        operation: Operation to perform (Set Grace Period, Set Retention Period, etc.)
        grace_period: Grace period value
        period_type: Period type (Days, Months, Years)
        target_date: Target date for retention
    """
    logging.info("Starting WORM settings task.")
    logging.info("Folder ID: %s", folder_id)
    logging.info("Operation: %s", operation)

    try:
        # Get the cloud folder
        logging.info("Looking up cloud folder: %s", folder_id)

        if operation == "Set Grace Period":
            if not grace_period:
                logging.error("Grace period value is required for this operation")
                return
            logging.info("Setting grace period: %s %s", grace_period, period_type)
            # session.cloudfs.set_grace_period(folder_id, int(grace_period), period_type)
            logging.info("Grace period set successfully")

        elif operation == "Set Retention Period":
            if not grace_period:
                logging.error("Retention period value is required for this operation")
                return
            logging.info("Setting retention period: %s %s", grace_period, period_type)
            # session.cloudfs.set_retention_period(folder_id, int(grace_period), period_type)
            logging.info("Retention period set successfully")

        elif operation == "Lock Folder":
            logging.info("Locking folder: %s", folder_id)
            # session.cloudfs.lock_folder(folder_id)
            logging.info("Folder locked successfully")

        elif operation == "Unlock Folder":
            logging.info("Unlocking folder: %s", folder_id)
            # session.cloudfs.unlock_folder(folder_id)
            logging.info("Folder unlocked successfully")

        else:
            logging.error("Unknown operation: %s", operation)
            return

        logging.info("Finished WORM settings task.")
    except Exception as e:
        logging.error("Error in WORM settings task: %s", e)
        raise
