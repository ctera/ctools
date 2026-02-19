"""Card widgets for CTools GUI."""

from typing import Optional
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QWidget,
)
from PySide6.QtCore import Qt

from ..theme import COLORS


class Card(QFrame):
    """A card container for grouping content."""

    def __init__(self, title: str = "", parent: Optional[QFrame] = None):
        super().__init__(parent)
        self._setup_ui(title)

    def _setup_ui(self, title: str) -> None:
        self.setStyleSheet(f"""
            Card {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(16)

        if title:
            self.title_label = QLabel(title)
            self.title_label.setStyleSheet(f"""
                font-size: 16px;
                font-weight: 600;
                color: {COLORS['text_primary']};
            """)
            self.main_layout.addWidget(self.title_label)

    def addWidget(self, widget):
        """Add a widget to the card."""
        self.main_layout.addWidget(widget)

    def addLayout(self, layout):
        """Add a layout to the card."""
        self.main_layout.addLayout(layout)


class OutputCard(QFrame):
    """A collapsible card for displaying command output/logs."""

    def __init__(self, title: str = "Output", parent: Optional[QFrame] = None):
        super().__init__(parent)
        self._expanded = False
        self._title = title
        self._setup_ui(title)

    def _setup_ui(self, title: str) -> None:
        self.setStyleSheet(f"""
            OutputCard {{
                background-color: {COLORS['surface']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Clickable header bar
        self.header_bar = QFrame()
        self.header_bar.setCursor(Qt.PointingHandCursor)
        self.header_bar.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['surface']};
                border: none;
                border-radius: 12px;
                padding: 16px 24px;
            }}
            QFrame:hover {{
                background-color: {COLORS['background']};
            }}
        """)

        header_layout = QHBoxLayout(self.header_bar)
        header_layout.setContentsMargins(24, 16, 24, 16)
        header_layout.setSpacing(12)

        # Arrow button
        self.toggle_btn = QPushButton("▲")
        self.toggle_btn.setFixedSize(28, 28)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: 14px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
        """)
        self.toggle_btn.clicked.connect(self.toggle)
        header_layout.addWidget(self.toggle_btn)

        # Title
        self.header_label = QLabel(title)
        self.header_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            background: transparent;
        """)
        header_layout.addWidget(self.header_label)

        header_layout.addStretch()

        # Make header clickable
        self.header_bar.mousePressEvent = lambda e: self.toggle()

        layout.addWidget(self.header_bar)

        # Output content container
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(24, 0, 24, 24)
        content_layout.setSpacing(0)

        # Output text area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setObjectName("output_area")
        self.output.setMinimumHeight(200)
        self.output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['primary']};
                border: none;
                border-radius: 8px;
                color: {COLORS['text_light']};
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                padding: 16px;
            }}
        """)
        content_layout.addWidget(self.output)

        layout.addWidget(self.content_widget)

        # Start collapsed
        self.content_widget.setVisible(False)

    def toggle(self) -> None:
        """Toggle expanded/collapsed state."""
        self._expanded = not self._expanded
        self.content_widget.setVisible(self._expanded)
        self.toggle_btn.setText("▼" if self._expanded else "▲")

    def expand(self) -> None:
        """Expand the output area."""
        if not self._expanded:
            self.toggle()

    def collapse(self) -> None:
        """Collapse the output area."""
        if self._expanded:
            self.toggle()

    def setText(self, text: str) -> None:
        """Set the output text."""
        self.output.setText(text)
        # Auto-expand when content is set
        if text and not self._expanded:
            self.expand()

    def appendText(self, text: str) -> None:
        """Append text to the output."""
        self.output.append(text)
        # Auto-expand when content is appended
        if not self._expanded:
            self.expand()

    def clear(self) -> None:
        """Clear the output."""
        self.output.clear()

    def scrollToBottom(self) -> None:
        """Scroll to the bottom of the output."""
        scrollbar = self.output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
