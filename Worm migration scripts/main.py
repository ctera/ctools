#!/usr/bin/env python3
"""
main.py - Get and Set WORM settings for a folder using cterasdk

This script retrieves and updates WORM (Write Once Read Many) settings
for a specified folder in CTERA Portal using the cterasdk Python library.

Usage:
    python main.py get --folder-id <id> [--portal <address>] [--username <user>] [--password <pass>]
    python main.py set --folder-id <id> --days <n> [--portal <address>] [--username <user>] [--password <pass>]
    python main.py set --folder-id <id> --hours <n> [--portal <address>] [--username <user>] [--password <pass>]
    python main.py set --folder-id <id> --minutes <n> [--portal <address>] [--username <user>] [--password <pass>]
    python main.py set --folder-id <id> --date <date> [--portal <address>] [--username <user>] [--password <pass>]

Examples:
    python main.py get --folder-id 31
    python main.py set --folder-id 31 --days 7
    python main.py set --folder-id 31 --hours 12
    python main.py set --folder-id 31 --minutes 30
    python main.py set --folder-id 31 --date "20 Feb 2026"
"""

import argparse
import sys
from datetime import datetime, date
import cterasdk.settings
from cterasdk import GlobalAdmin, Object
from cterasdk.exceptions import CTERAException


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
        # This is equivalent to GET /admin/api/objs/{folder_id}
        folder_obj = admin.api.get(f'objs/{folder_id}')
        return folder_obj
    except CTERAException as e:
        print(f"[ERROR] Failed to retrieve folder settings: {str(e)}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return None


def display_worm_settings(folder_obj, folder_id):
    """
    Display WORM settings from the folder object
    
    Args:
        folder_obj: The folder object returned from the API
        folder_id: The folder ID (for display purposes)
    """
    print(f"\n[INFO] Folder ID: {folder_id}")
    
    # Check if folder object exists
    if folder_obj is None:
        print("[ERROR] Folder object is None")
        return
    
    # Check if WORM settings exist
    if not hasattr(folder_obj, 'wormSettings') or folder_obj.wormSettings is None:
        print("[INFO] No WORM settings found for this folder")
        return
    
    worm_settings = folder_obj.wormSettings
    
    # Check if WORM is enabled
    if hasattr(worm_settings, 'worm'):
        print(f"[INFO] WORM Enabled: {worm_settings.worm}")
    else:
        print("[INFO] WORM Enabled: Not specified")
    
    # Display grace period if it exists
    if hasattr(worm_settings, 'gracePeriod') and worm_settings.gracePeriod is not None:
        grace_period = worm_settings.gracePeriod
        print("\n[INFO] WORM Grace Period Settings:")
        
        if hasattr(grace_period, 'amount'):
            print(f"  Amount: {grace_period.amount}")
        else:
            print("  Amount: Not specified")
            
        if hasattr(grace_period, 'type'):
            print(f"  Type: {grace_period.type}")
        else:
            print("  Type: Not specified")
    else:
        print("[INFO] No grace period settings found")
    
    # Display full WORM settings object for debugging (if needed)
    print("\n[INFO] Full WORM Settings Object:")
    print(f"  {worm_settings}")
    
    # Try to display as dictionary if possible
    if hasattr(worm_settings, '__dict__'):
        print("\n[INFO] WORM Settings Details:")
        for key, value in worm_settings.__dict__.items():
            print(f"  {key}: {value}")


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
        print(f"[INFO] Retrieving current folder settings for folder ID: {folder_id}...")
        folder_obj = admin.api.get(f'objs/{folder_id}')
        
        # Check if folder object exists
        if folder_obj is None:
            print("[ERROR] Failed to retrieve folder object")
            return False
        
        # Check if WORM settings exist
        if not hasattr(folder_obj, 'wormSettings') or folder_obj.wormSettings is None:
            print("[ERROR] This folder does not have WORM settings configured")
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
        print(f"[INFO] Updating WORM grace period to {amount} {period_type}...")
        admin.api.put(f'objs/{folder_id}', folder_obj)
        
        print(f"[SUCCESS] WORM grace period updated successfully!")
        print(f"[INFO] Folder ID: {folder_id}")
        print(f"[INFO] Grace Period: {amount} {period_type}")
        
        return True
        
    except CTERAException as e:
        print(f"[ERROR] Failed to update WORM grace period: {str(e)}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return False


def main():
    """Main function to handle command line arguments and execute WORM settings operations"""
    parser = argparse.ArgumentParser(
        description='Get and Set WORM settings for a folder in CTERA Portal using cterasdk',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s get --folder-id 31
  %(prog)s set --folder-id 31 --days 7
  %(prog)s set --folder-id 31 --hours 12
  %(prog)s set --folder-id 31 --minutes 30
  %(prog)s set --folder-id 31 --date "20 Feb 2026"
  %(prog)s get --folder-id 31 --portal 192.168.27.67 --username admin --password Sooraj@123
        """
    )
    
    # Add subparsers for get and set commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute', required=True)
    
    # Parser for 'get' command
    get_parser = subparsers.add_parser('get', help='Get WORM settings for a folder')
    get_parser.add_argument(
        '--folder-id',
        type=int,
        required=True,
        help='The folder ID to query for WORM settings'
    )
    
    # Parser for 'set' command
    set_parser = subparsers.add_parser('set', help='Set WORM grace period for a folder')
    set_parser.add_argument(
        '--folder-id',
        type=int,
        required=True,
        help='The folder ID to update'
    )
    
    # Mutually exclusive group for time period options
    period_group = set_parser.add_mutually_exclusive_group(required=True)
    period_group.add_argument(
        '--days',
        type=int,
        help='Set grace period in days'
    )
    period_group.add_argument(
        '--hours',
        type=int,
        help='Set grace period in hours'
    )
    period_group.add_argument(
        '--minutes',
        type=int,
        help='Set grace period in minutes'
    )
    period_group.add_argument(
        '--date',
        type=str,
        help="Set grace period based on target date (e.g., '20 Feb 2026'). Calculates days from today to the target date."
    )
    
    # Common arguments for both commands
    for subparser in [get_parser, set_parser]:
        subparser.add_argument(
            '--portal',
            type=str,
            default='192.168.27.67',
            help='CTERA Portal address (default: 192.168.27.67)'
        )
        subparser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Username for CTERA Portal login (default: admin)'
        )
        subparser.add_argument(
            '--password',
            type=str,
            default='Sooraj@123',
            help='Password for CTERA Portal login (default: Sooraj@123)'
        )
    
    args = parser.parse_args()
    
    # Configure SSL settings (disable for self-signed certificates)
    cterasdk.settings.core.syn.settings.connector.ssl = False
    
    try:
        # Create GlobalAdmin instance and login
        with GlobalAdmin(args.portal) as admin:
            print(f"[INFO] Logging in to CTERA Portal at {args.portal}...")
            admin.login(args.username, args.password)
            print("[SUCCESS] Login successful!")
            
            if args.command == 'get':
                # Retrieve WORM settings
                print(f"[INFO] Retrieving WORM settings for folder ID: {args.folder_id}...")
                folder_obj = get_worm_settings(admin, args.folder_id)
                
                if folder_obj:
                    display_worm_settings(folder_obj, args.folder_id)
                    print("\n[SUCCESS] WORM settings retrieved successfully!")
                else:
                    print("\n[ERROR] Failed to retrieve folder settings")
                    sys.exit(1)
                    
            elif args.command == 'set':
                # Determine the period type and amount
                if args.days is not None:
                    amount = args.days
                    period_type = 'Days'
                elif args.hours is not None:
                    amount = args.hours
                    period_type = 'Hours'
                elif args.minutes is not None:
                    amount = args.minutes
                    period_type = 'Minutes'
                elif args.date is not None:
                    # Parse the target date and calculate days
                    try:
                        target_date = parse_target_date(args.date)
                        amount = calculate_days_until_date(target_date)
                        period_type = 'Days'
                        print(f"[INFO] Target date: {target_date.strftime('%d %b %Y')}")
                        print(f"[INFO] Calculated days from today: {amount}")
                    except ValueError as e:
                        print(f"[ERROR] {str(e)}")
                        sys.exit(1)
                else:
                    print("[ERROR] No time period specified")
                    sys.exit(1)
                
                # Set WORM grace period
                success = set_worm_grace_period(admin, args.folder_id, amount, period_type)
                
                if not success:
                    print("\n[ERROR] Failed to update WORM grace period")
                    sys.exit(1)
                
                # Retrieve and display updated settings
                print("\n[INFO] Retrieving updated WORM settings...")
                folder_obj = get_worm_settings(admin, args.folder_id)
                if folder_obj:
                    display_worm_settings(folder_obj, args.folder_id)
            
            admin.logout()
            print("[INFO] Logged out successfully")
            
    except CTERAException as e:
        print(f"[ERROR] CTERA API error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
