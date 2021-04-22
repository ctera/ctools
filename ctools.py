from login import login
from status import run_status
from unlock import unlock, start_ssh, disable_ssh
from run_cmd import run_cmd
from suspend_sync import suspend_filer_sync
from unsuspend_sync import unsuspend_filer_sync
from gooey import Gooey, GooeyParser
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

@Gooey(advanced=True)
def parse_args():
    """Parse CLI Arguments.
    
    Required Arguments:
    See choices in FUNCTION_MAP
    Optionally, any or all Portal Global Admin creds can be provided.
    """
    parser = GooeyParser(description='Manage CTERA Edge Filers')
    FUNCTION_MAP = {'get_status' : run_status}
    parser.add_argument('task', choices=FUNCTION_MAP.keys(),widget='FilterableDropdown')
    parser.add_argument('address',help='Portal IP, hostname, or FQDN')
    parser.add_argument('username',help='Username for portal administrator')
    parser.add_argument('password',help='Password for portal administrator', widget='PasswordField')
    args = parser.parse_args()
    logging.info('Starting ctools')
    global_admin = login(args.address,args.username,args.password)
    selected_task = FUNCTION_MAP[args.task]
    selected_task(global_admin)
    return parser

if __name__ == "__main__":
    set_logging(logging.DEBUG,'debug.log')
    parse_args()
