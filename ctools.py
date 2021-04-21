from login import login
from status import run_status
from unlock import unlock, start_ssh
from run_cmd import run_cmd
from suspend_sync import suspend_filer_sync
from unsuspend_sync import unsuspend_filer_sync
from cterasdk import *
from argparse import ArgumentParser
from getpass import getpass
import logging, sys

def set_logging(p_level=logging.INFO,log_file="log.txt"):
    """Set up logging to a given file name.
    
    Keyword arguments:
    p_level --  DEBUG, INFO, WARNING, ERROR, Critical. (default INFO)
    log_file -- file name for log file. (default "log.txt")
    """
    logging.root.handlers = []
    logging.basicConfig(
        level=p_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
   )

def parse_args():
    """Parse CLI Arguments.
    
    Required Arguments:
    See choices in FUNCTION_MAP
    Optionally, any or all Portal Global Admin creds can be provided.
    """
    parser = ArgumentParser(description='Manage CTERA Edge Filers')

    FUNCTION_MAP = {'suspend_sync' : suspend_filer_sync,
                    'unsuspend_sync' : unsuspend_filer_sync,
                    'get_status' : run_status,
                    'run_cmd' : run_cmd,
                    'enable_telnet' : unlock,
                    'enable_ssh' : start_ssh
                   }

    tasks = parser.add_argument_group('tasks', 'Possible tasks to run.')
    tasks.add_argument('task', choices=FUNCTION_MAP.keys())

    creds = parser.add_argument_group('credentials', 'Optional. Provide creds for scripting or re-running.')
    creds.add_argument('-a', '--address',help='Portal IP, hostname, or FQDN')
    creds.add_argument('-u', '--username',help='Username for portal administrator')
    creds.add_argument('-p', '--password',help='Password for portal administrator')

    args = parser.parse_args()
    if args.address is None:
        address = input("Portal (IP, Hostname or FQDN): ")
    else:
        address = args.address
    if args.username is None:
        username = input("Admin Username: ")
    else:
        username = args.username
    if args.password is None:
        password = getpass("Admin Password: ")
    else:
        password = args.password

    global_admin = login(address,username,password)
    selected_task = FUNCTION_MAP[args.task]
    selected_task(global_admin)
    return parser

if __name__ == "__main__":
    set_logging(logging.DEBUG)
    logging.info('Starting ctools')
    parse_args()
    sys.exit('Exiting ctools.')
