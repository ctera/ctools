"""Modern CLI for CTools using argparse."""

import argparse
import logging
import sys

from cterasdk import GlobalAdmin, settings

from ..core.logging import setup_logging
from ..core.auth import global_admin_login, enable_device_sso


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to a subparser."""
    parser.add_argument("address", help="Portal IP, hostname, or FQDN")
    parser.add_argument("username", help="Global admin username")
    parser.add_argument("password", help="Global admin password")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging"
    )


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="ctools",
        description="CTools - A toolset for CTERA environments"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 4.1.1"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # show_status command
    status_parser = subparsers.add_parser(
        "show_status",
        help="Generate status report for all filers"
    )
    add_common_args(status_parser)
    status_parser.add_argument("filename", help="Output CSV filename")
    status_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # run_cmd command
    runcmd_parser = subparsers.add_parser(
        "run_cmd",
        help="Run CLI command on devices"
    )
    add_common_args(runcmd_parser)
    runcmd_parser.add_argument("cmd", help="CLI command to execute")
    runcmd_parser.add_argument("--tenant", help="Tenant name")
    runcmd_parser.add_argument("--device", help="Device name")
    runcmd_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # suspend_sync command
    suspend_parser = subparsers.add_parser(
        "suspend_sync",
        help="Suspend cloud sync on devices"
    )
    add_common_args(suspend_parser)
    suspend_parser.add_argument("--tenant", help="Tenant name")
    suspend_parser.add_argument("--device", help="Device name")
    suspend_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # unsuspend_sync command
    unsuspend_parser = subparsers.add_parser(
        "unsuspend_sync",
        help="Resume cloud sync on devices"
    )
    add_common_args(unsuspend_parser)
    unsuspend_parser.add_argument("--tenant", help="Tenant name")
    unsuspend_parser.add_argument("--device", help="Device name")
    unsuspend_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # enable_ssh command
    ssh_enable_parser = subparsers.add_parser(
        "enable_ssh",
        help="Enable SSH on devices"
    )
    add_common_args(ssh_enable_parser)
    ssh_enable_parser.add_argument("--tenant", help="Tenant name")
    ssh_enable_parser.add_argument("--device", help="Device name")
    ssh_enable_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # disable_ssh command
    ssh_disable_parser = subparsers.add_parser(
        "disable_ssh",
        help="Disable SSH on devices"
    )
    add_common_args(ssh_disable_parser)
    ssh_disable_parser.add_argument("--tenant", help="Tenant name")
    ssh_disable_parser.add_argument("--device", help="Device name")
    ssh_disable_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # enable_telnet command
    telnet_parser = subparsers.add_parser(
        "enable_telnet",
        help="Enable telnet on devices"
    )
    add_common_args(telnet_parser)
    telnet_parser.add_argument("--tenant", help="Tenant name")
    telnet_parser.add_argument("--device", help="Device name")
    telnet_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # reset_password command
    reset_parser = subparsers.add_parser(
        "reset_password",
        help="Reset device admin password"
    )
    add_common_args(reset_parser)
    reset_parser.add_argument("new_password", help="New password to set")
    reset_parser.add_argument("--tenant", help="Tenant name")
    reset_parser.add_argument("--device", help="Device name")
    reset_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # report_zones command
    zones_parser = subparsers.add_parser(
        "report_zones",
        help="Generate zones report"
    )
    add_common_args(zones_parser)
    zones_parser.add_argument("filename", help="Output CSV filename")
    zones_parser.add_argument("--tenant", help="Tenant name")
    zones_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # shares_report command
    shares_parser = subparsers.add_parser(
        "shares_report",
        help="Generate shares report"
    )
    add_common_args(shares_parser)
    shares_parser.add_argument("filename", help="Output CSV filename")
    shares_parser.add_argument("--tenant", help="Tenant name")
    shares_parser.add_argument("--device", help="Device name")
    shares_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # copy_shares command
    copy_parser = subparsers.add_parser(
        "copy_shares",
        help="Copy shares between devices"
    )
    add_common_args(copy_parser)
    copy_parser.add_argument("source_device", help="Source device name")
    copy_parser.add_argument("target_device", help="Target device name")
    copy_parser.add_argument("--tenant", help="Tenant name")

    # populate_shares command
    populate_parser = subparsers.add_parser(
        "populate_shares",
        help="Populate shares from CSV"
    )
    add_common_args(populate_parser)
    populate_parser.add_argument("csv_file", help="CSV file with share definitions")
    populate_parser.add_argument("--tenant", help="Tenant name")

    # add_mapping command
    mapping_parser = subparsers.add_parser(
        "add_mapping",
        help="Add domain to advanced mapping"
    )
    add_common_args(mapping_parser)
    mapping_parser.add_argument("domain", help="Domain name")
    mapping_parser.add_argument("--tenant", help="Tenant name")
    mapping_parser.add_argument("--device", help="Device name")
    mapping_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    # worm_settings command
    worm_parser = subparsers.add_parser(
        "worm_settings",
        help="Configure WORM settings"
    )
    add_common_args(worm_parser)
    worm_parser.add_argument("--tenant", help="Tenant name")
    worm_parser.add_argument("--device", help="Device name")
    worm_parser.add_argument(
        "--all-tenants",
        action="store_true",
        help="Run on all tenants"
    )

    return parser


def run_with_session(args, handler_func, **kwargs):
    """
    Set up session and run a handler function.

    Args:
        args: Parsed arguments
        handler_func: Function to call with (session, **kwargs)
        **kwargs: Additional arguments to pass to handler
    """
    setup_logging(
        logging.DEBUG if args.verbose else logging.INFO,
        'debug-log.txt' if args.verbose else 'info-log.txt'
    )

    settings.sessions.management.ssl = False

    try:
        with GlobalAdmin(args.address) as admin:
            admin.login(args.username, args.password)
            enable_device_sso(admin)
            admin.logout()

        with GlobalAdmin(args.address) as admin:
            admin.login(args.username, args.password)
            try:
                handler_func(admin, **kwargs)
            finally:
                admin.logout()
    except Exception as e:
        logging.error("Operation failed: %s", e)
        sys.exit(1)


def cli_main(argv=None):
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Import handlers lazily to avoid circular imports
    if args.command == "show_status":
        from ..tools.status import run_status
        run_with_session(
            args, run_status,
            filename=args.filename,
            all_tenants=args.all_tenants
        )

    elif args.command == "run_cmd":
        from ..tools.run_cmd import run_cmd
        run_with_session(
            args, run_cmd,
            command=args.cmd,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "suspend_sync":
        from ..tools.suspend_sync import suspend_sync
        run_with_session(
            args, suspend_sync,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "unsuspend_sync":
        from ..tools.unsuspend_sync import unsuspend_sync
        run_with_session(
            args, unsuspend_sync,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "enable_ssh":
        from ..tools.enable_ssh import enable_ssh
        run_with_session(
            args, enable_ssh,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "disable_ssh":
        from ..tools.disable_ssh import disable_ssh
        run_with_session(
            args, disable_ssh,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "enable_telnet":
        from ..tools.enable_telnet import enable_telnet
        run_with_session(
            args, enable_telnet,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "reset_password":
        from ..tools.reset_password import reset_password
        run_with_session(
            args, reset_password,
            new_password=args.new_password,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "report_zones":
        from ..tools.report_zones import report_zones
        run_with_session(
            args, report_zones,
            filename=args.filename,
            tenant=args.tenant,
            all_tenants=args.all_tenants
        )

    elif args.command == "shares_report":
        from ..tools.shares_report import shares_report
        run_with_session(
            args, shares_report,
            filename=args.filename,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "copy_shares":
        from ..tools.copy_shares import copy_shares
        run_with_session(
            args, copy_shares,
            source_device=args.source_device,
            target_device=args.target_device,
            tenant=args.tenant
        )

    elif args.command == "populate_shares":
        from ..tools.populate_shares import populate_shares
        run_with_session(
            args, populate_shares,
            csv_file=args.csv_file,
            tenant=args.tenant
        )

    elif args.command == "add_mapping":
        from ..tools.add_mapping import add_mapping
        run_with_session(
            args, add_mapping,
            domain=args.domain,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    elif args.command == "worm_settings":
        from ..tools.worm_settings import worm_settings
        run_with_session(
            args, worm_settings,
            tenant=args.tenant,
            device=args.device,
            all_tenants=args.all_tenants
        )

    else:
        print(f"Command '{args.command}' is not yet implemented.")
        sys.exit(1)
