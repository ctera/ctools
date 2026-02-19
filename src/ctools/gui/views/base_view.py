"""Base view class for tool views."""

import asyncio
import logging
from abc import abstractmethod
from typing import Optional
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap

from ..theme import COLORS
from ...core.resources import get_logo_path
from ..widgets import FormField, PasswordField, CheckboxField, FormSection
from ..widgets import PrimaryButton, SecondaryButton, OutputCard
from ...core.auth import global_admin_login, enable_device_sso
from ...core.logging import setup_logging


class WorkerThread(QThread):
    """Background worker thread for running tools."""

    finished = Signal(bool, str)  # success, message
    progress = Signal(str)  # log message

    def __init__(self, func, log_level=logging.INFO, log_file='info-log.txt', *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.log_level = log_level
        self.log_file = log_file

    def run(self):
        # Create a new event loop for this thread (required by cterasdk)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Set up logging with signal callback for real-time output
        setup_logging(
            level=self.log_level,
            log_file=self.log_file,
            signal_callback=self.progress.emit
        )

        try:
            self.func(*self.args, **self.kwargs)
            self.finished.emit(True, "Operation completed successfully")
        except Exception as e:
            self.finished.emit(False, str(e))
        finally:
            loop.close()


class BaseToolView(QWidget):
    """Base class for all tool views."""

    # Subclasses should override these
    title: str = "Tool"
    description: str = "Tool description"
    icon: str = ""

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

        # Connection settings (common to all tools)
        self._create_connection_section()

        # Tool-specific settings
        self._create_tool_section()

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
        title.setObjectName("page_title")
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: 700;
        """)

        desc = QLabel(self.description)
        desc.setObjectName("page_description")
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

    def _create_connection_section(self) -> None:
        """Create the connection settings section."""
        section = FormSection("Connection")

        self.address_field = FormField("Portal Address", "e.g., portal.company.com")
        self.username_field = FormField("Username", "Global admin username")
        self.password_field = PasswordField("Password", "Admin password")

        section.addRow(self.address_field, self.username_field)
        section.addField(self.password_field)

        self.content_layout.addWidget(section)

    @abstractmethod
    def _create_tool_section(self) -> None:
        """Create tool-specific form section. Subclasses must implement."""
        pass

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
        # Validate inputs
        if not self._validate_inputs():
            return

        # Disable run button
        self.run_button.setEnabled(False)
        self.run_button.setText("Running...")

        # Clear output and expand
        self.output_card.clear()
        self.output_card.expand()

        # Determine logging level
        verbose = getattr(self, 'verbose_checkbox', None)
        log_level = logging.DEBUG if verbose and verbose.isChecked() else logging.INFO
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
        if not self.address_field.text():
            self.output_card.appendText("Error: Portal address is required\n")
            return False
        if not self.username_field.text():
            self.output_card.appendText("Error: Username is required\n")
            return False
        if not self.password_field.text():
            self.output_card.appendText("Error: Password is required\n")
            return False
        return True

    def _get_session(self):
        """Create and return an authenticated session."""
        address = self.address_field.text()
        username = self.username_field.text()
        password = self.password_field.text()

        # First login to enable SSO
        admin = global_admin_login(address, username, password, ignore_cert=True)
        if admin:
            enable_device_sso(admin)
            admin.logout()

        # Second login with SSO enabled
        return global_admin_login(address, username, password, ignore_cert=True)

    @abstractmethod
    def _execute_tool(self) -> None:
        """Execute the tool. Subclasses must implement."""
        pass

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
