import sys
import logging

from log_setter import set_logging
from cterasdk import settings, GlobalAdmin
from worm_settings import get_worm_settings, display_worm_settings, set_worm_grace_period, parse_target_date, calculate_days_until_date


def worm_settings_cli(args):
    if len(args) < 3:
        print("\nManage WORM (Write Once Read Many) settings for folders in CTERA Portal\n")
        print("Usage:")
        print("  Get Settings:")
        print("    ./ctools.exe worm_settings get [address] [username] [password] [folder_id] [verbose]\n")
        print("  Set Grace Period by Value:")
        print("    ./ctools.exe worm_settings set [address] [username] [password] [folder_id] [amount] [type] [verbose]\n")
        print("  Set Grace Period by Date:")
        print("    ./ctools.exe worm_settings set [address] [username] [password] [folder_id] [date] Days [verbose]\n")
        print("Parameters:")
        print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
        print("  username: The global admin username of the CTERA Portal")
        print("  password: The global admin password of the CTERA Portal")
        print("  folder_id: The folder ID - Ex: 31")
        print("  amount: Grace period amount - Ex: 7")
        print("  type: Grace period type - Days, Hours, or Minutes")
        print("  date: Target date - Ex: '26 Aug 2026' or '2026-08-26'")
        print("  verbose: Enable debug logging - True or False\n")
        print("Examples:")
        print("  ./ctools.exe worm_settings get 192.168.80.200 admin password1! 31 False")
        print("  ./ctools.exe worm_settings set 192.168.80.200 admin password1! 31 7 Days False")
        print("  ./ctools.exe worm_settings set 192.168.80.200 admin password1! 31 '26 Aug 2026' Days True\n")

        sys.exit(0)

    else:
        operation = args[2]

        if operation not in ['get', 'set']:
            print("\nError: Operation must be 'get' or 'set'\n")
            sys.exit(1)

        if len(args) < 7:
            print("\nError: Not enough arguments provided\n")
            sys.exit(1)

        address = args[3]
        username = args[4]
        password = args[5]
        folder_id = args[6]

        # Parse verbose flag (default to False if not provided)
        verbose = False
        if operation == 'get' and len(args) >= 8:
            verbose = args[7] == "True"
        elif operation == 'set' and len(args) >= 10:
            verbose = args[9] == "True"

        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        # Validate folder ID
        try:
            folder_id_int = int(folder_id)
        except ValueError:
            print("\nError: Folder ID must be a valid integer\n")
            sys.exit(1)

        settings.sessions.management.ssl = False

        with GlobalAdmin(address) as ga:
            try:
                ga.login(username, password)
                logging.info("Login successful!")

                if operation == 'get':
                    # Get WORM settings
                    logging.info("Retrieving WORM settings for folder ID: %s", folder_id_int)
                    folder_obj = get_worm_settings(ga, folder_id_int)

                    if folder_obj:
                        display_worm_settings(folder_obj, folder_id_int)
                        logging.info("WORM settings retrieved successfully!")
                    else:
                        logging.error("Failed to retrieve folder settings")
                        sys.exit(1)

                elif operation == 'set':
                    if len(args) < 9:
                        print("\nError: Set operation requires amount/date and type\n")
                        sys.exit(1)

                    value_or_date = args[7]
                    period_type = args[8]

                    # Try to parse as date first
                    try:
                        target_date = parse_target_date(value_or_date)
                        amount = calculate_days_until_date(target_date)
                        period_type = 'Days'
                        logging.info("Target date: %s", target_date.strftime('%d %b %Y'))
                        logging.info("Calculated days from today: %s", amount)
                    except ValueError:
                        # Not a date, treat as numeric amount
                        try:
                            amount = int(value_or_date)
                        except ValueError:
                            logging.error("Grace period value must be a valid integer or date")
                            sys.exit(1)

                    # Validate period type
                    if period_type not in ['Days', 'Hours', 'Minutes']:
                        logging.error("Period type must be Days, Hours, or Minutes")
                        sys.exit(1)

                    # Set WORM grace period
                    success = set_worm_grace_period(ga, folder_id_int, amount, period_type)

                    if not success:
                        logging.error("Failed to update WORM grace period")
                        sys.exit(1)

                    # Retrieve and display updated settings
                    logging.info("Retrieving updated WORM settings...")
                    folder_obj = get_worm_settings(ga, folder_id_int)
                    if folder_obj:
                        display_worm_settings(folder_obj, folder_id_int)

                ga.logout()
                logging.info("Logged out successfully")

            except Exception as e:
                logging.error("An error occurred: %s", str(e))
                sys.exit(1)

        sys.exit(0)
