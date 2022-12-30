import logging
from getpass import getpass

from gooey import Gooey, GooeyParser

from login import global_admin_login
from status import run_status
from unlock import enable_telnet, start_ssh, disable_ssh
from run_cmd import run_cmd
from suspend_sync import suspend_filer_sync
from unsuspend_sync import unsuspend_filer_sync
from reset_password import reset_filer_password
from cloudfs import ask,create_folders,usage
from smb_audit import convert_size, extract_epoch, convert_time, show_ftr_details, summarize_audit, parse_audit, search_audit, smb_audit
from pandas.api.types import CategoricalDtype
import re

version = "2.1b"
name = "CTools "

def set_logging(p_level=logging.INFO, log_file="info-log.txt"):
    """
    Set up logging to a given file name.
    Doesn't require CTERASDK_LOG_FILE to be set.

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


@Gooey(advanced=True, navigation='SIDEBAR', program_name=name + version, use_cmd_args=True,
       default_size=(800, 750),
       menu=[{
            'name': 'File',
            'items': [{
                    'type': 'Link',
                    'menuTitle': 'Visit Our Site',
                    'url': 'https://www.ctera.com/'
                    }]},
             {'name': 'Help',
              'items': [{
                    'type': 'Link',
                    'menuTitle': 'CTERA Support',
                    'url': 'https://support.ctera.com/'
                   }, {
                    'type': 'Link',
                    'menuTitle': 'Open a CTools Issue',
                    'url': 'https://github.com/ctera/ctools/issues'}, {
                    'type': 'AboutDialog',
                    'menuTitle': 'About',
                    'name': 'CTools',
                    'description': 'A toolbox of tasks to check and manage CTERA Edge Filers.',
                    'version': version,
                    'copyright': '2023',
                    'website': 'https://github.com/ctera/ctools/',
                    'license': 'TBD'
                    },]}])
def main():
    """
    Create dictionary mapping task names to functions.
    Add parent parser(s) for re-use in task sub parsers.
    Add a subparser to present options based on chosen task.
    """
    FUNCTION_MAP = {'get_status': run_status,
                    'run_cmd': run_cmd,
                    'enable_telnet': enable_telnet,
                    'enable_ssh': start_ssh,
                    'disable_ssh': disable_ssh,
                    'suspend_sync': suspend_filer_sync,
                    'unsuspend_sync': unsuspend_filer_sync,
                    'reset_password': reset_filer_password,
                    'cloudfs': create_folders,
                    'smb_audit': smb_audit,
                    }
    parser = GooeyParser(description='Manage CTERA Edge Filers')
    parser.add_argument('--ignore-gooey', help='Run in CLI mode')
    # Parent Parser for tasks requiring portal logins.
    portal_parent_parser = GooeyParser(add_help=False)
    portal_parent_parser.add_argument('address', help='Portal IP, hostname, or FQDN')
    portal_parent_parser.add_argument('username', help='Username for portal administrator')
    # This makes password required.
    # Good for a GUI, not good for a CLI where it must be entered be in plain text.
    # To allow a secret prompt on CLI, enter ? for the password argument.
    portal_parent_parser.add_argument('password', widget='PasswordField', help='Password. Enter ? to prompt in CLI')

    # Optionally enable verbose/debug logging.
    # If not specified/checked, default to INFO level.
    portal_parent_parser.add_argument('-v', '--verbose', help='Add verbose logging', action='store_true')
    portal_parent_parser.add_argument('-i', '--ignore_cert', help='Ignore cert warnings', action='store_true')

    # Create a subparser
    subs = parser.add_subparsers(help='Task choices.', dest='task')

    # Filer Status sub parser
    status_help = "Record current status of connected Filers."
    status_parser = subs.add_parser('get_status', parents=[portal_parent_parser], help=status_help)
    status_parser.add_argument('filename', type=str, help='output filename')
    status_parser.add_argument('-a', '--all', action='store_true', help='All Filers, All Tenants')

    # Run device command sub parser
    cmd_help = "Run a comand on one or more connected Filers."
    all_help = "Run a command globally, on all Filers, on all Tenants."
    device_help = "Device name to run command against. Overrides --all flag."

    cmd_parser = subs.add_parser('run_cmd', parents=[portal_parent_parser], help=cmd_help)
    cmd_parser.add_argument('command', type=str, help=cmd_help)
    cmd_parser.add_argument('-a', '--all', action='store_true', help=all_help)
    cmd_parser.add_argument('-d', '--device', help=device_help)

    # Enable Telnet sub parser
    enable_telnet_help = "Enable SSH on a Filer."
    enable_telnet_parser = subs.add_parser('enable_telnet', parents=[portal_parent_parser], help=enable_telnet_help)
    enable_telnet_parser.add_argument('device_name', help='Device Name')
    enable_telnet_parser.add_argument('tenant_name', help='Tenant Name')
    enable_telnet_parser.add_argument('-c', '--code', help='Required code to enable telnet')

    # Enable SSH sub parser
    enable_ssh_help = "Enable SSH on a Filer."
    enable_ssh_parser = subs.add_parser('enable_ssh', parents=[portal_parent_parser], help=enable_ssh_help)
    enable_ssh_parser.add_argument('device_name', help='Device Name')
    enable_ssh_parser.add_argument('tenant_name', help='Tenant Name')
    enable_ssh_parser.add_argument('-p', '--pubkey', help='Provide an SSH Public Key')

    # Disable SSH sub parser
    disable_ssh_help = "Disable SSH on a Filer."
    disable_ssh_parser = subs.add_parser('disable_ssh', parents=[portal_parent_parser], help=disable_ssh_help)
    disable_ssh_parser.add_argument('device_name', help='Device Name')
    disable_ssh_parser.add_argument('tenant_name', help='Tenant Name')

    # Suspend sync sub parser
    suspend_sync_help = "Suspend sync on a given Filer"
    suspend_sync_parser = subs.add_parser('suspend_sync', parents=[portal_parent_parser], help=suspend_sync_help)
    suspend_sync_parser.add_argument('device_name', help='Device Name')
    suspend_sync_parser.add_argument('tenant_name', help='Tenant Name')

    # Suspend sync sub parser
    unsuspend_sync_help = "Unsuspend sync on a given Filer"
    unsuspend_sync_parser = subs.add_parser('unsuspend_sync', parents=[portal_parent_parser], help=unsuspend_sync_help)
    unsuspend_sync_parser.add_argument('device_name', help='Device Name')
    unsuspend_sync_parser.add_argument('tenant_name', help='Tenant Name')

    # Reset Filer sub parser
    reset_pw_help_text = "Reset a user password on a Filer"
    new_pw_help_text = 'New Filer Password. Enter ? to prompt in CLI'
    reset_password_parser = subs.add_parser('reset_password', parents=[portal_parent_parser], help=reset_pw_help_text)
    reset_password_parser.add_argument('device_name', help='Device Name')
    reset_password_parser.add_argument('tenant_name', help='Tenant Name')
    reset_password_parser.add_argument('user_name', help='User Name')
    reset_password_parser.add_argument('filer_password', widget='PasswordField', help=new_pw_help_text)

    # cloudfs sub parser
    cloudfs_help = "Create zones, folder groups, cloud folders"
    cloudfs_parser = subs.add_parser('cloudfs', parents=[portal_parent_parser], help=cloudfs_help)
    cloudfs_parser.add_argument('csv_file', widget='FileChooser', help='csv file') 

    # SMB Audit subparsers
    smb_audit_help_text = "Parse, summarize, and search Samba audit logs from CTEA devices."
    smb_audit_parser = subs.add_parser('smb_audit', help=smb_audit_help_text)
    smb_audit_parser.add_argument('-f', '--function', action='store', dest='function', widget='Dropdown', choices=['Parse', 'Summarize', 'Search'], required=True, default='Parse', type=str, help='Source log directory contianing ONLY audit log files (Format: share/folder1/folder2/folderN')
    smb_audit_parser.add_argument('-sd', '--source-directory', action='store', dest='source_directory', widget='DirChooser', type=str, help='Source log directory contianing ONLY audit log files (Format: share/folder1/folder2/folderN')
    smb_audit_parser.add_argument('-of', '--output-file', action='store', dest='output_file', type=str, help='Label for output files')
    #smb_audit_parser.add_argument('-c', '--csv', action='store_true', dest='make_csv', default=False, help='Output a CSV file in addition to other options')    
    smb_audit_parser.add_argument('-if', '--input-file', action='store', dest='ftr_file', type=str, widget="FileChooser", help='Name of the input file(Format: customer_location.ftr)')
    smb_audit_parser.add_argument('-ti', '--time-interval', action='store', dest='time_interval', type=str, widget="Dropdown", choices=['5min', '10min', '15min', '20min', '30min', '60min'], required=True, default='30min', help='Time interval used for summary computations')     
    smb_audit_parser.add_argument('-ss', '--search-string', action='store', dest='search_string', type=str, help='String to search for in the specified field.')
    smb_audit_parser.add_argument('-sf', '--search-field', action='store', dest='search_field', type=str, widget="Dropdown", choices=['path', 'share', 'user'], default='path', help='Field to be searched from the audit logs: path, user, result, share.')  
    smb_audit_parser.add_argument('--debug', action='store_true', dest='is_debug', default=False, help='Enables debug output of arguments')
    smb_audit_parser.add_argument('-v', '--verbose', help='Add verbose logging', action='store_true')
    
    #Create dictionary of Samba operation types
    smb_operations = ["op=ACEChanged", "op=ACLAdded", "op=ACLDeleted", "op=AclDenied", "op=chown",
                    "op=create", "op=createDenied", "op=delete", "op=deleteDenied", "op=move",
                    "op=open", "op=OpenDenied", "op=setattrib", "op=setdacl", "op=write"]
    smb_operation_type = CategoricalDtype(categories=smb_operations)    
    smb_ops_group = smb_audit_parser.add_argument_group('Show SMB Operations')
    for op in smb_operations:
        op_string = re.sub('op=', '', op)
        op_command = "--" + op_string
        smb_ops_group.add_argument(op_command, action='store_false', default=True, widget='CheckBox', help=op_string )

    
    # Parse arguments and run commands of chosen task
    args = parser.parse_args()
    if args.verbose:
        set_logging(logging.DEBUG, 'debug-log.txt')
    else:
        set_logging()

        
    # Uncomment to log the arguments. Will reveal a GUI password in plain text.
    # logging.debug(args)
    logging.info('Starting ctools')
    # For CLI, if required password arg is a ?, prompt for password
    if args.task != 'smb_audit':
        if args.password == '?':
            args.password = getpass(prompt='Password: ')
        # Create a global_admin object and login.
    # In the future, if we add device login tasks, we'll need to change this.
    if args.task != 'smb_audit':  #added this since smb_audit does not require portal login
        global_admin = global_admin_login(args.address, args.username, args.password, args.ignore_cert)
    # Set the chosen task.
    selected_task = FUNCTION_MAP[args.task]
    # Run selected task with required sub arguments.
    if args.task == 'get_status':
        selected_task(global_admin, args.filename, args.all)
    elif args.task == 'run_cmd':
        selected_task(global_admin, args.command, args.all, args.device)
    elif args.task == 'enable_telnet':
        selected_task(global_admin, args.device_name, args.tenant_name, args.code)
    elif args.task == 'enable_ssh':
        selected_task(global_admin, args.device_name, args.tenant_name, args.pubkey)
    elif args.task == 'disable_ssh':
        selected_task(global_admin, args.device_name, args.tenant_name)
    elif args.task == 'suspend_sync':
        selected_task(global_admin, args.device_name, args.tenant_name)
    elif args.task == 'unsuspend_sync':
        selected_task(global_admin, args.device_name, args.tenant_name)
    elif args.task == 'reset_password':
        selected_task(global_admin, args.device_name, args.tenant_name, args.user_name, args.filer_password)
    elif args.task == 'cloudfs':
        selected_task(global_admin, args.csv_file)
    elif args.task == 'smb_audit':
        selected_task(args)
    else:
        logging.error('No task found or selected.')
    if args.task != 'smb_audit':  #added this since smb_audit does not require portal login
        global_admin.logout()
    logging.info('Exiting ctools')


if __name__ == "__main__":
    main()

