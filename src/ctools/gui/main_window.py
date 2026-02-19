"""Main application window for CTools."""

import sys
from typing import List
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)
from PySide6.QtCore import Qt

from .theme import APP_STYLESHEET, COLORS
from .widgets import Sidebar
from .views import (
    StatusView,
    RunCmdView,
    SuspendSyncView,
    UnsuspendSyncView,
    EnableSSHView,
    DisableSSHView,
    EnableTelnetView,
    ResetPasswordView,
    ReportZonesView,
    SharesReportView,
    CopySharesView,
    PopulateSharesView,
    CreateSharesView,
    AddMappingView,
    WormSettingsView,
    CloudFSView,
    DeleteSharesView,
    AddRemoveMembersView,
    ImportCertificateView,
    TOOLS,
)


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation."""

    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_ui()

    def _setup_window(self) -> None:
        """Configure window properties."""
        self.setWindowTitle("CTools - CTERA Management Suite")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Apply stylesheet
        self.setStyleSheet(APP_STYLESHEET)

    def _setup_ui(self) -> None:
        """Set up the main UI layout."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        layout.addWidget(self.sidebar)

        # Content area with stacked views
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_area")
        self.content_stack.setStyleSheet(f"""
            #content_area {{
                background-color: {COLORS['background']};
            }}
        """)
        layout.addWidget(self.content_stack)

        # Create views and navigation
        self._create_views()
        self._setup_navigation()

        # Set initial view
        self.sidebar.set_current(0)

    def _create_views(self) -> None:
        """Create all tool views."""
        idx = 0

        # Reports section
        self.sidebar.add_section("Reports")
        self._add_view(StatusView(), "Status Report", idx); idx += 1
        self._add_view(ReportZonesView(), "Zones Report", idx); idx += 1
        self._add_view(SharesReportView(), "Shares Report", idx); idx += 1

        # Device Operations section
        self.sidebar.add_section("Device Operations")
        self._add_view(RunCmdView(), "Run Command", idx); idx += 1
        self._add_view(SuspendSyncView(), "Suspend Sync", idx); idx += 1
        self._add_view(UnsuspendSyncView(), "Resume Sync", idx); idx += 1

        # Access Control section
        self.sidebar.add_section("Access Control")
        self._add_view(EnableSSHView(), "Enable SSH", idx); idx += 1
        self._add_view(DisableSSHView(), "Disable SSH", idx); idx += 1
        self._add_view(EnableTelnetView(), "Enable Telnet", idx); idx += 1
        self._add_view(ResetPasswordView(), "Reset Password", idx); idx += 1
        self._add_view(AddRemoveMembersView(), "Add/Remove Members", idx); idx += 1

        # Shares section
        self.sidebar.add_section("Shares")
        self._add_view(CopySharesView(), "Copy Shares", idx); idx += 1
        self._add_view(PopulateSharesView(), "Populate Shares", idx); idx += 1
        self._add_view(CreateSharesView(), "Create Shares", idx); idx += 1
        self._add_view(DeleteSharesView(), "Delete Shares", idx); idx += 1

        # CloudFS section
        self.sidebar.add_section("CloudFS")
        self._add_view(CloudFSView(), "CloudFS", idx); idx += 1
        self._add_view(WormSettingsView(), "WORM Settings", idx); idx += 1

        # Configuration section
        self.sidebar.add_section("Configuration")
        self._add_view(AddMappingView(), "ID Mapping", idx); idx += 1
        self._add_view(ImportCertificateView(), "Import Certificate", idx); idx += 1

        self.sidebar.add_stretch()

    def _add_view(self, view: QWidget, name: str, index: int) -> None:
        """Add a view to the content stack and navigation."""
        self.content_stack.addWidget(view)
        self.sidebar.add_item(name, index)

    def _setup_navigation(self) -> None:
        """Connect navigation signals."""
        self.sidebar.navigation_changed.connect(self._on_navigation_changed)

    def _on_navigation_changed(self, index: int) -> None:
        """Handle navigation changes."""
        self.content_stack.setCurrentIndex(index)
