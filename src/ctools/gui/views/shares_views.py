"""Shares-related views."""

import logging
from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from .base_view import BaseToolView, WorkerThread
from ..theme import COLORS
from ...core.resources import get_logo_path
from ..widgets import FormField, PasswordField, FileField, CheckboxField, FormSection
from ..widgets import PrimaryButton, SecondaryButton, OutputCard
from ...tools.shares_report import shares_report
from ...tools.copy_shares import copy_shares
from ...tools.populate_shares import populate_shares


class SharesReportView(BaseToolView):
    """View for generating shares reports."""

    title = "Shares Report"
    description = "Generate a report of all shares on filers"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Report Settings")

        self.filename_field = FileField(
            "Output File",
            "e.g., shares_report.csv",
            mode="save",
            file_filter="CSV Files (*.csv);;All Files (*.*)"
        )
        self.tenant_field = FormField("Tenant Name", "Leave blank for all tenants")
        self.device_field = FormField("Device Name", "Leave blank for all devices")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.filename_field)
        section.addRow(self.tenant_field, self.device_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.filename_field.text():
            self.output_card.appendText("Error: Output filename is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the shares report tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            shares_report(
                session,
                filename=self.filename_field.text(),
                tenant=self.tenant_field.text() or None,
                device=self.device_field.text() or None,
                all_tenants=not self.tenant_field.text()
            )
        finally:
            try:
                session.logout()
            except:
                pass


class CopySharesView(QWidget):
    """View for copying shares between devices (direct device connection)."""

    title = "Copy Shares"
    description = "Copy shares from one device to another"

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.worker: Optional[WorkerThread] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the view layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = self._create_header()
        layout.addWidget(header)

        # Scrollable form area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLORS['background']};
                border: none;
            }}
        """)

        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(32, 24, 32, 24)
        self.content_layout.setSpacing(24)

        # Source device section
        source_section = FormSection("Source Device")
        self.source_ip = FormField("Device IP/Hostname", "e.g., 192.168.1.100")
        self.source_username = FormField("Admin Username", "Device admin username")
        self.source_password = PasswordField("Password", "Device admin password")
        source_section.addField(self.source_ip)
        source_section.addRow(self.source_username, self.source_password)
        self.content_layout.addWidget(source_section)

        # Destination device section
        dest_section = FormSection("Destination Device")
        self.dest_ip = FormField("Device IP/Hostname", "e.g., 192.168.1.101")
        self.dest_username = FormField("Admin Username", "Device admin username")
        self.dest_password = PasswordField("Password", "Device admin password")
        dest_section.addField(self.dest_ip)
        dest_section.addRow(self.dest_username, self.dest_password)
        self.content_layout.addWidget(dest_section)

        # Options section
        options_section = FormSection("Options")
        self.verbose_checkbox = CheckboxField("Verbose logging")
        options_section.addField(self.verbose_checkbox)
        self.content_layout.addWidget(options_section)

        # Action buttons
        self._create_action_buttons()

        self.content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll, 1)  # Takes available space

        # Output area (bottom, collapsible)
        output_container = QWidget()
        output_container.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['background']};
            }}
        """)
        output_layout = QVBoxLayout(output_container)
        output_layout.setContentsMargins(32, 8, 32, 16)
        output_layout.setSpacing(0)

        self.output_card = OutputCard("Output")
        output_layout.addWidget(self.output_card)

        layout.addWidget(output_container)

    def _create_header(self) -> QFrame:
        """Create the page header."""
        header = QFrame()
        header.setObjectName("content_header")
        header.setStyleSheet(f"""
            #content_header {{
                background-color: {COLORS['surface']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)

        # Main horizontal layout for header
        main_layout = QHBoxLayout(header)
        main_layout.setContentsMargins(32, 24, 32, 24)
        main_layout.setSpacing(16)

        # Left side: title and description
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title = QLabel(self.title)
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: 700;
        """)

        desc = QLabel(self.description)
        desc.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 14px;
        """)

        text_layout.addWidget(title)
        text_layout.addWidget(desc)

        main_layout.addLayout(text_layout)
        main_layout.addStretch()

        # Right side: logo
        try:
            logo_path = get_logo_path()
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Scale to 48px height while preserving aspect ratio
                scaled_pixmap = pixmap.scaledToHeight(48, Qt.SmoothTransformation)
                logo_label = QLabel()
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setStyleSheet("background: transparent;")
                main_layout.addWidget(logo_label)
        except Exception:
            pass  # Silently fail if logo can't be loaded

        return header

    def _create_action_buttons(self) -> None:
        """Create the action buttons."""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.run_button = PrimaryButton("Run", self._on_run)
        self.clear_button = SecondaryButton("Clear Output", self._on_clear)

        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.run_button)

        self.content_layout.addLayout(button_layout)

    def _on_run(self) -> None:
        """Handle the Run button click."""
        if not self._validate_inputs():
            return

        self.run_button.setEnabled(False)
        self.run_button.setText("Running...")

        self.output_card.clear()
        self.output_card.expand()

        # Determine logging level
        log_level = logging.DEBUG if self.verbose_checkbox.isChecked() else logging.INFO
        log_file = 'debug-log.txt' if log_level == logging.DEBUG else 'info-log.txt'

        # Run in background thread with real-time logging
        self.worker = WorkerThread(self._execute_tool, log_level=log_level, log_file=log_file)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_progress(self, message: str) -> None:
        """Handle progress updates (log messages)."""
        self.output_card.output.append(message)
        self.output_card.scrollToBottom()

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not self.source_ip.text():
            self.output_card.appendText("Error: Source device IP is required\n")
            return False
        if not self.source_username.text():
            self.output_card.appendText("Error: Source username is required\n")
            return False
        if not self.source_password.text():
            self.output_card.appendText("Error: Source password is required\n")
            return False
        if not self.dest_ip.text():
            self.output_card.appendText("Error: Destination device IP is required\n")
            return False
        if not self.dest_username.text():
            self.output_card.appendText("Error: Destination username is required\n")
            return False
        if not self.dest_password.text():
            self.output_card.appendText("Error: Destination password is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the copy shares tool."""
        copy_shares(
            source_ip=self.source_ip.text(),
            source_username=self.source_username.text(),
            source_password=self.source_password.text(),
            dest_ip=self.dest_ip.text(),
            dest_username=self.dest_username.text(),
            dest_password=self.dest_password.text()
        )

    def _on_finished(self, success: bool, message: str) -> None:
        """Handle tool completion."""
        self.run_button.setEnabled(True)
        self.run_button.setText("Run")

        if success:
            self.output_card.output.append(f"\n✓ {message}")
        else:
            self.output_card.output.append(f"\n✗ Error: {message}")

        self.output_card.scrollToBottom()

    def _on_clear(self) -> None:
        """Clear the output area."""
        self.output_card.clear()


class PopulateSharesView(BaseToolView):
    """View for populating cloud folders as shares."""

    title = "Populate Shares"
    description = "Populate cloud folders as shares on a device"

    def _create_tool_section(self) -> None:
        """Create tool-specific form fields."""
        section = FormSection("Device Settings")

        self.device_field = FormField("Device Name", "Name of the device to populate shares on")
        self.domain_field = FormField("Domain Name", "Only needed if domain users are cloud folder owners")
        self.verbose_checkbox = CheckboxField("Verbose logging")

        section.addField(self.device_field)
        section.addField(self.domain_field)
        section.addField(self.verbose_checkbox)

        self.content_layout.addWidget(section)

    def _validate_inputs(self) -> bool:
        """Validate required inputs."""
        if not super()._validate_inputs():
            return False
        if not self.device_field.text():
            self.output_card.appendText("Error: Device name is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the populate shares tool."""
        session = self._get_session()
        if not session:
            raise Exception("Failed to connect to portal")

        try:
            populate_shares(
                session,
                device=self.device_field.text(),
                domain=self.domain_field.text() or None
            )
        finally:
            try:
                session.logout()
            except:
                pass
