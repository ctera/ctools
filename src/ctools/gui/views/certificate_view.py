"""Import Certificate view - Import SSL certificates to Edge Filers."""

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

from .base_view import WorkerThread
from ..theme import COLORS
from ...core.resources import get_logo_path
from ..widgets import FormField, PasswordField, FileField, CheckboxField, FormSection
from ..widgets import PrimaryButton, SecondaryButton, OutputCard
from ...tools.import_certificate import import_certificate


class ImportCertificateView(QWidget):
    """View for importing SSL certificates to Edge Filers (direct device connection)."""

    title = "Import Certificate"
    description = "Import SSL certificates to an Edge Filer"

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

        # Device connection section
        device_section = FormSection("Device Connection")
        self.device_ip = FormField("Device IP/Hostname", "e.g., 192.168.1.100")
        self.device_username = FormField("Admin Username", "Device admin username")
        self.device_password = PasswordField("Password", "Device admin password")
        device_section.addField(self.device_ip)
        device_section.addRow(self.device_username, self.device_password)
        self.content_layout.addWidget(device_section)

        # Certificate files section
        cert_section = FormSection("Certificate Files")
        self.private_key_field = FileField(
            "Private Key File",
            "Select private key file (.pem, .key)",
            mode="open",
            file_filter="Key Files (*.pem *.key);;All Files (*.*)"
        )
        self.cert_file_1 = FileField(
            "Certificate File 1",
            "Select certificate file (.pem, .crt)",
            mode="open",
            file_filter="Certificate Files (*.pem *.crt *.cer);;All Files (*.*)"
        )
        self.cert_file_2 = FileField(
            "Certificate File 2 (Optional)",
            "Select additional certificate file (chain cert)",
            mode="open",
            file_filter="Certificate Files (*.pem *.crt *.cer);;All Files (*.*)"
        )
        self.cert_file_3 = FileField(
            "Certificate File 3 (Optional)",
            "Select additional certificate file (root cert)",
            mode="open",
            file_filter="Certificate Files (*.pem *.crt *.cer);;All Files (*.*)"
        )
        cert_section.addField(self.private_key_field)
        cert_section.addField(self.cert_file_1)
        cert_section.addField(self.cert_file_2)
        cert_section.addField(self.cert_file_3)
        self.content_layout.addWidget(cert_section)

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
                scaled_pixmap = pixmap.scaledToHeight(48, Qt.SmoothTransformation)
                logo_label = QLabel()
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setStyleSheet("background: transparent;")
                main_layout.addWidget(logo_label)
        except Exception:
            pass

        return header

    def _create_action_buttons(self) -> None:
        """Create the action buttons."""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.run_button = PrimaryButton("Import", self._on_run)
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
        self.run_button.setText("Importing...")

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
        if not self.device_ip.text():
            self.output_card.appendText("Error: Device IP is required\n")
            return False
        if not self.device_username.text():
            self.output_card.appendText("Error: Username is required\n")
            return False
        if not self.device_password.text():
            self.output_card.appendText("Error: Password is required\n")
            return False
        if not self.private_key_field.text():
            self.output_card.appendText("Error: Private key file is required\n")
            return False
        if not self.cert_file_1.text():
            self.output_card.appendText("Error: At least one certificate file is required\n")
            return False
        return True

    def _execute_tool(self) -> None:
        """Execute the import certificate tool."""
        # Collect certificate files
        cert_files = [self.cert_file_1.text()]
        if self.cert_file_2.text():
            cert_files.append(self.cert_file_2.text())
        if self.cert_file_3.text():
            cert_files.append(self.cert_file_3.text())

        import_certificate(
            address=self.device_ip.text(),
            username=self.device_username.text(),
            password=self.device_password.text(),
            private_key_file=self.private_key_field.text(),
            certificate_files=cert_files
        )

    def _on_finished(self, success: bool, message: str) -> None:
        """Handle tool completion."""
        self.run_button.setEnabled(True)
        self.run_button.setText("Import")

        if success:
            self.output_card.output.append(f"\n✓ {message}")
        else:
            self.output_card.output.append(f"\n✗ Error: {message}")

        self.output_card.scrollToBottom()

    def _on_clear(self) -> None:
        """Clear the output area."""
        self.output_card.clear()
