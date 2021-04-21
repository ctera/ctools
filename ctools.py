from menu import menu
from status import run_status
from unlock import unlock, start_ssh
from run_cmd import run_cmd
from suspend_sync import suspend_filer_sync
from unsuspend_sync import unsuspend_filer_sync
from cterasdk import *
from argparse import ArgumentParser
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

parser = ArgumentParser(description='Manage CTERA Edge Filers')
parser.add_argument('-m', '--menu',
                    dest='action',action='store_const',
                    const=menu,
                    help='Show a menu of options to run')
parser.add_argument('-rs','--get_status',
                    dest='action',action='store_const',
                    const=run_status,
                    help='Get and save status of all Filers')
parser.add_argument('-et','--enable_telnet',
                    dest='action',action='store_const',
                    const=unlock,
                    help='Enable telnet on a Filer')
parser.add_argument('-es','--enable_ssh',
                    dest='action',action='store_const',
                    const=start_ssh,
                    help='Enable ssh on a Filer')
parser.add_argument('-ss','--suspend_sync',
                    dest='action', action='store_const',
                    const=suspend_filer_sync,
                    help='Suspend Sync on a given Filer')
parser.add_argument('-us','--unsuspend_sync',
                    dest='action', action='store_const',
                    const=unsuspend_filer_sync,
                    help='Unsuspend Sync on a given Filer')

if __name__ == "__main__":
    args = parser.parse_args()
    set_logging(logging.DEBUG)
    if args.action is None:
        self = None
        menu(self)
        sys.exit('Exiting ctools.')
    logging.info('Starting ctools')
    args.action(args)
    sys.exit('Exiting ctools.')
