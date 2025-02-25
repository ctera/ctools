# python file to describe behaviors if the user wants to run ctools as a commandline
import sys, logging

from run_cmd import run_cmd

from cli_helpers.run_cmd_cli import run_cmd_cli
from cli_helpers.suspend_sync_cli import suspend_sync_cli
from cli_helpers.unsuspend_sync_cli import unsuspend_sync_cli
from cli_helpers.show_status_cli import show_status_cli
from cli_helpers.enable_ssh_cli import enable_ssh_cli
from cli_helpers.disable_ssh_cli import disable_ssh_cli
from cli_helpers.enable_telnet_cli import enable_telnet_cli
from cli_helpers.reset_password_cli import reset_password_cli
from cli_helpers.copy_shares_cli import copy_shares_cli
from cli_helpers.report_zones_cli import report_zones_cli
from cli_helpers.populate_shares_cli import populate_shares_cli
from cli_helpers.shares_report_cli import shares_report_cli
from cli_helpers.add_mapping_cli import add_mapping_cli

from cterasdk import GlobalAdmin, settings
from log_setter import set_logging

def cli(args):
    if args[1] == "--help":
        print("\nCTools is a GUI toolset to interact with your CTERA Environment\n")
        print("Usage: ./ctools.exe [tool] [parameters]\n")
        print("Tools:")
        print("  run_cmd                show_status")
        print("  suspend_sync           unsuspend_sync")
        print("  enable_ssh             disable_ssh")
        print("  enable_telnet          reset_password")
        print("  cloud_folders          delete_shares")
        print("  copy_shares            add_rem_members")
        print("  report_zones           populate_shares")
        print("  add_mapping            shares_report")
        print("  import_cert")
        print("\nFor help using these tools, you can use the --help flag after selecting the tool")
        print("Ex: \"./ctools.exe run_cmd --help\"\n")

        sys.exit(0)

    if args[1] == "run_cmd":
        run_cmd_cli(args)
    elif args[1] == "suspend_sync":
        suspend_sync_cli(args)
    elif args[1] == "unsuspend_sync":
        unsuspend_sync_cli(args)
    elif args[1] == "show_status":
        show_status_cli(args)
    elif args[1] == "enable_ssh":
        enable_ssh_cli(args)
    elif args[1] == "disable_ssh":
        disable_ssh_cli(args)
    elif args[1] == "enable_telnet":
        enable_telnet_cli(args)
    elif args[1] == "reset_password":
        reset_password_cli(args)
    elif args[1] == "cloud_folders":
        print("\nThis tool is not yet supported with the CLI\n")
    elif args[1] == "delete_shares":
        print("\nThis tool is not yet supported with the CLI\n")
    elif args[1] == "copy_shares":
        copy_shares_cli(args)
    elif args[1] == "add_rem_members":
        print("\nThis tool is not yet supported with the CLI\n")
    elif args[1] == "report_zones":
        report_zones_cli(args)
    elif args[1] == "populate_shares":
        populate_shares_cli(args)
    elif args[1] == "shares_report":
        shares_report_cli(args)
    elif args[1] == "add_mapping":
        add_mapping_cli(args)
    elif args[1] == "import_cert":
        print("\nThis tool is not yet supported with the CLI\n")

    else:
        print("\nInvalid tool selected. Please use the --help flag to see a list of available tools\n")