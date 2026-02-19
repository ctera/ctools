"""View classes for CTools GUI."""

from .base_view import BaseToolView
from .status_view import StatusView
from .run_cmd_view import RunCmdView
from .sync_views import SuspendSyncView, UnsuspendSyncView
from .ssh_views import EnableSSHView, DisableSSHView
from .telnet_view import EnableTelnetView
from .password_view import ResetPasswordView
from .zones_view import ReportZonesView
from .shares_views import SharesReportView, CopySharesView, PopulateSharesView
from .create_shares_view import CreateSharesView
from .mapping_view import AddMappingView
from .worm_view import WormSettingsView
from .cloudfs_view import CloudFSView
from .delete_shares_view import DeleteSharesView
from .members_view import AddRemoveMembersView
from .certificate_view import ImportCertificateView

__all__ = [
    'BaseToolView',
    'StatusView',
    'RunCmdView',
    'SuspendSyncView',
    'UnsuspendSyncView',
    'EnableSSHView',
    'DisableSSHView',
    'EnableTelnetView',
    'ResetPasswordView',
    'ReportZonesView',
    'SharesReportView',
    'CopySharesView',
    'PopulateSharesView',
    'CreateSharesView',
    'AddMappingView',
    'WormSettingsView',
    'CloudFSView',
    'DeleteSharesView',
    'AddRemoveMembersView',
    'ImportCertificateView',
]

# Tool definitions for navigation
TOOLS = [
    ("status", "Status Report", "Generate detailed status reports"),
    ("run_cmd", "Run Command", "Execute CLI commands on devices"),
    ("suspend_sync", "Suspend Sync", "Pause cloud synchronization"),
    ("unsuspend_sync", "Resume Sync", "Resume cloud synchronization"),
    ("enable_ssh", "Enable SSH", "Enable SSH access on devices"),
    ("disable_ssh", "Disable SSH", "Disable SSH access on devices"),
    ("enable_telnet", "Enable Telnet", "Enable telnet access on devices"),
    ("reset_password", "Reset Password", "Reset device passwords"),
    ("report_zones", "Zones Report", "Generate zones report"),
    ("shares_report", "Shares Report", "Generate shares report"),
    ("delete_shares", "Delete Shares", "Delete shares by substring match"),
    ("copy_shares", "Copy Shares", "Copy shares between devices"),
    ("populate_shares", "Populate Shares", "Populate cloud folders as shares"),
    ("create_shares", "Create Shares", "Create shares with permissions from CSV"),
    ("cloudfs", "CloudFS", "Create folder groups and folders from CSV"),
    ("add_mapping", "ID Mapping", "Configure AD ID mapping"),
    ("add_remove_members", "Add/Remove Members", "Manage Administrators group"),
    ("import_certificate", "Import Certificate", "Import SSL certificates"),
    ("worm_settings", "WORM Settings", "Configure WORM compliance"),
]
