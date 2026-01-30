import logging
from datetime import datetime, date
from cterasdk import CTERAException, Object


def parse_target_date(date_string):
    """
    Parse date string in multiple formats and return a date object

    Supported formats:
    - "20 Feb 2026" / "20 February 2026" (DD MMM YYYY)
    - "20/02/2026" (DD/MM/YYYY)
    - "02/20/2026" (MM/DD/YYYY)
    - "2026-02-20" (YYYY-MM-DD)
    - "20-02-2026" (DD-MM-YYYY)

    Args:
        date_string: String representation of the date

    Returns:
        datetime.date object

    Raises:
        ValueError: If the date string cannot be parsed in any supported format
    """
    date_formats = [
        # DD MMM YYYY or DD MMMM YYYY (e.g., "20 Feb 2026" or "20 February 2026")
        '%d %b %Y',
        '%d %B %Y',
        # DD/MM/YYYY (e.g., "20/02/2026")
        '%d/%m/%Y',
        # MM/DD/YYYY (e.g., "02/20/2026")
        '%m/%d/%Y',
        # YYYY-MM-DD (e.g., "2026-02-20")
        '%Y-%m-%d',
        # DD-MM-YYYY (e.g., "20-02-2026")
        '%d-%m-%Y',
    ]

    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_string.strip(), fmt).date()
            return parsed_date
        except ValueError:
            continue

    # If none of the formats worked, raise an error
    raise ValueError(
        f"Unable to parse date '{date_string}'. Supported formats: "
        "'20 Feb 2026', '20/02/2026', '02/20/2026', '2026-02-20', '20-02-2026'"
    )


def calculate_days_until_date(target_date):
    """
    Calculate the number of days from today to the target date

    Args:
        target_date: datetime.date object representing the target date

    Returns:
        Integer number of days from today to target date

    Raises:
        ValueError: If the target date is in the past
    """
    today = date.today()
    days_delta = (target_date - today).days

    if days_delta < 0:
        raise ValueError(
            f"Target date {target_date.strftime('%d %b %Y')} is in the past. "
            "Please specify a future date."
        )

    return days_delta


def get_worm_settings(admin, folder_id):
    """
    Retrieve WORM settings for a folder using cterasdk API

    Args:
        admin: GlobalAdmin instance (already logged in)
        folder_id: The folder ID to query

    Returns:
        The folder object with WORM settings, or None if not found
    """
    try:
        # Use admin.api.get() to retrieve the folder object
        folder_obj = admin.api.get(f'objs/{folder_id}')
        return folder_obj
    except CTERAException as e:
        logging.error("Failed to retrieve folder settings: %s", str(e))
        return None
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
        return None


def display_worm_settings(folder_obj, folder_id):
    """
    Display WORM settings from the folder object

    Args:
        folder_obj: The folder object returned from the API
        folder_id: The folder ID (for display purposes)
    """
    logging.info("Folder ID: %s", folder_id)

    # Check if folder object exists
    if folder_obj is None:
        logging.error("Folder object is None")
        return

    # Check if WORM settings exist
    if not hasattr(folder_obj, 'wormSettings') or folder_obj.wormSettings is None:
        logging.info("No WORM settings found for this folder")
        return

    worm_settings = folder_obj.wormSettings

    # Check if WORM is enabled
    if hasattr(worm_settings, 'worm'):
        logging.info("WORM Enabled: %s", worm_settings.worm)
    else:
        logging.info("WORM Enabled: Not specified")

    # Display grace period if it exists
    if hasattr(worm_settings, 'gracePeriod') and worm_settings.gracePeriod is not None:
        grace_period = worm_settings.gracePeriod
        logging.info("WORM Grace Period Settings:")

        if hasattr(grace_period, 'amount'):
            logging.info("  Amount: %s", grace_period.amount)
        else:
            logging.info("  Amount: Not specified")

        if hasattr(grace_period, 'type'):
            logging.info("  Type: %s", grace_period.type)
        else:
            logging.info("  Type: Not specified")
    else:
        logging.info("No grace period settings found")

    # Display full WORM settings object for debugging
    logging.info("Full WORM Settings Object: %s", worm_settings)

    # Try to display as dictionary if possible
    if hasattr(worm_settings, '__dict__'):
        logging.info("WORM Settings Details:")
        for key, value in worm_settings.__dict__.items():
            logging.info("  %s: %s", key, value)


def set_worm_grace_period(admin, folder_id, amount, period_type):
    """
    Set WORM grace period for a folder using cterasdk API

    Args:
        admin: GlobalAdmin instance (already logged in)
        folder_id: The folder ID to update
        amount: The amount (number) for the grace period
        period_type: The type of period ('Days', 'Hours', or 'Minutes')

    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the current folder object
        logging.info("Retrieving current folder settings for folder ID: %s", folder_id)
        folder_obj = admin.api.get(f'objs/{folder_id}')

        # Check if folder object exists
        if folder_obj is None:
            logging.error("Failed to retrieve folder object")
            return False

        # Check if WORM settings exist
        if not hasattr(folder_obj, 'wormSettings') or folder_obj.wormSettings is None:
            logging.error("This folder does not have WORM settings configured")
            return False

        worm_settings = folder_obj.wormSettings

        # Check if gracePeriod exists, if not create it
        if not hasattr(worm_settings, 'gracePeriod') or worm_settings.gracePeriod is None:
            # Create a new WormPeriod object
            grace_period = Object()
            grace_period._classname = 'WormPeriod'
            grace_period.amount = amount
            grace_period.type = period_type
            worm_settings.gracePeriod = grace_period
        else:
            # Update existing grace period
            worm_settings.gracePeriod.amount = amount
            worm_settings.gracePeriod.type = period_type

        # Save the updated folder object back to the server
        logging.info("Updating WORM grace period to %s %s", amount, period_type)
        admin.api.put(f'objs/{folder_id}', folder_obj)

        logging.info("WORM grace period updated successfully!")
        logging.info("Folder ID: %s", folder_id)
        logging.info("Grace Period: %s %s", amount, period_type)

        return True

    except CTERAException as e:
        logging.error("Failed to update WORM grace period: %s", str(e))
        return False
    except Exception as e:
        logging.error("Unexpected error: %s", str(e))
        return False
