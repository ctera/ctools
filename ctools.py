from login import login
from status import run_status
from unlock import enable_telnet, start_ssh, disable_ssh
from run_cmd import run_cmd
from suspend_sync import suspend_filer_sync
from unsuspend_sync import unsuspend_filer_sync
from gooey import Gooey, GooeyParser
from cterasdk import *
from argparse import ArgumentParser
from getpass import getpass
import logging, sys

""" If any args are present, run in CLI mode"""
if len(sys.argv) >= 2:
    if not '--ignore-gooey' in sys.argv:
        sys.argv.append('--ignore-gooey')


def set_logging(p_level=logging.INFO,log_file="info-log.txt"):
    """Set up logging to a given file name.
    Doesn't require CTERASDK_LOG_FILE to be set.
    
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
            logging.StreamHandler()])

@Gooey(advanced=True, navigation='TABBED', program_name="CTools",
        default_size=(600,600),
	menu=[{
	    'name': 'File',
	    'items': [{
		    'type': 'AboutDialog',
		    'menuTitle': 'About',
		    'name': 'CTools',
		    'description': 'A toolbox of sorts to check and manage CTERA Edge Filers and more coming soon.',
		    'version': 'v2.0a',
		    'copyright': '2021',
		    'website': 'https://github.com/ctera/ctools/tree/todd/gooey',
		    'license': 'TBD'
                    }, {
		    'type': 'Link',
		    'menuTitle': 'Visit Our Site',
                    'url': 'https://www.ctera.com/'
                    }]
	    },{
	    'name': 'Help',
	    'items': [{
		'type': 'Link',
		'menuTitle': 'Open an Issue',
		'url': 'https://github.com/ctera/ctools/issues'
	    }]
	}])

def main():
    """
    Create dictionary mapping task names to functions.
    Add parent parser(s) for re-use in task sub parsers.
    Add a subparser to present options based on chosen task.
    """
    FUNCTION_MAP = {'get_status' : run_status,
                    'run_cmd'   : run_cmd,
                    'enable_telnet' : enable_telnet,
                    'enable_ssh' : start_ssh,
                    'disable_ssh' : disable_ssh,
                    'suspend_sync' : suspend_filer_sync,
                    'unsuspend_sync' : unsuspend_filer_sync,
                   }
    parser = GooeyParser(description='Manage CTERA Edge Filers')
    # Parent Parser for tasks requiring portal logins.
    portal_parent_parser = GooeyParser(add_help=False)
    portal_parent_parser.add_argument('address',help='Portal IP, hostname, or FQDN')
    portal_parent_parser.add_argument('username',
                                help='Username for portal administrator')
    # This makes password required.
    # Good for a GUI, not good for a CLI where it must be entered be in plain text.
    # To allow a secret prompt on CLI, enter ? for the password argument.
    portal_parent_parser.add_argument('password',
                                help='Password. Enter ? to prompt in CLI',
                                widget='PasswordField')

    # Optionally enable verbose/debug logging.
    # If not specified/checked, default to INFO level.
    portal_parent_parser.add_argument('-v', '--verbose', help='Add verbose logging',
                                      action='store_true')

    # Create a subparser
    subs = parser.add_subparsers(help='Task choices.', dest='task')

    # Filer Status sub parser
    status_help = "Record current status of all connected Filers. Use --all to browse all Tenants"
    status_parser = subs.add_parser('get_status',
                                    parents = [portal_parent_parser],
                                    help=status_help)
    status_parser.add_argument('filename',type=str, help='output filename')
    status_parser.add_argument('-a', '--all',action='store_true',
                               help='All Filers, All Tenants')

    # Run device command sub parser
    cmd_help = "Run a comand on each connected Filer."
    cmd_parser = subs.add_parser('run_cmd',
                                parents = [portal_parent_parser],
                                help=cmd_help)
    cmd_parser.add_argument('command', type=str, help=cmd_help)

    # Enable Telnet sub parser
    enable_telnet_help = "Enable SSH on a Filer."
    enable_telnet_parser = subs.add_parser('enable_telnet',
                                parents = [portal_parent_parser],
                                help=enable_telnet_help)
    enable_telnet_parser.add_argument('device_name', help='Device Name')
    enable_telnet_parser.add_argument('tenant_name', help='Tenant Name')
    enable_telnet_parser.add_argument('-c','--code',
                                help='Required code to enable telnet')

    # Enable SSH sub parser
    enable_ssh_help = "Enable SSH on a Filer."
    enable_ssh_parser = subs.add_parser('enable_ssh',
                                parents = [portal_parent_parser],
                                help=enable_ssh_help)
    enable_ssh_parser.add_argument('device_name', help='Device Name')
    enable_ssh_parser.add_argument('tenant_name', help='Tenant Name')
    enable_ssh_parser.add_argument('-p','--pubkey',
                                    help='Provide an SSH Public Key')

    # Disable SSH sub parser
    disable_ssh_help = "Disable SSH on a Filer."
    disable_ssh_parser = subs.add_parser('disable_ssh',
                                parents = [portal_parent_parser],
                                help=disable_ssh_help)
    disable_ssh_parser.add_argument('device_name', help='Device Name')
    disable_ssh_parser.add_argument('tenant_name', help='Tenant Name')

    # Suspend sync sub parser
    suspend_sync_help = "Suspend sync on a given Filer"
    suspend_sync_parser = subs.add_parser('suspend_sync',
                                parents = [portal_parent_parser],
                                help=suspend_sync_help)
    suspend_sync_parser.add_argument('device_name', help='Device Name')
    suspend_sync_parser.add_argument('tenant_name', help='Tenant Name')

    # Suspend sync sub parser
    unsuspend_sync_help = "Unsuspend sync on a given Filer"
    unsuspend_sync_parser = subs.add_parser('unsuspend_sync',
                                parents = [portal_parent_parser],
                                help=unsuspend_sync_help)
    unsuspend_sync_parser.add_argument('device_name', help='Device Name')
    unsuspend_sync_parser.add_argument('tenant_name', help='Tenant Name')

    # Parse arguments and run commands of chosen task
    args = parser.parse_args()
    if args.verbose:
        set_logging(logging.DEBUG,'debug-log.txt')
    else:
        set_logging()
    # Uncomment to log the arguments. Will reveal a GUI password in plain text.
    #logging.debug(args)
    logging.info('Starting ctools')
    # For CLI, if required password arg is a ?, prompt for password
    if args.password == '?':
        args.password = getpass(prompt='Password: ')
    # Create a global_admin object and login.
    # In the future, if we add device login tasks, we'll need to change this.
    global_admin = login(args.address,args.username,args.password)
    ### Set the chosen task.
    selected_task = FUNCTION_MAP[args.task]
    # Run selected task with required sub arguments.
    if args.task == 'get_status':
        selected_task(global_admin,args.filename,args.all)
    elif args.task == 'run_cmd':
        selected_task(global_admin,args.command)
    elif args.task == 'enable_telnet':
        selected_task(global_admin,args.device_name,args.tenant_name,args.code)
    elif args.task == 'enable_ssh':
        selected_task(global_admin,args.device_name,args.tenant_name,args.pubkey)
    elif args.task == 'disable_ssh':
        selected_task(global_admin,args.device_name,args.tenant_name)
    elif args.task == 'suspend_sync':
        selected_task(global_admin,args.device_name,args.tenant_name)
    elif args.task == 'unsuspend_sync':
        selected_task(global_admin,args.device_name,args.tenant_name)
    else:
        logging.error('No task found or selected.')

if __name__ == "__main__":
    main()
