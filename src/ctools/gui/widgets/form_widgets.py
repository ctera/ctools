"""Form widgets for CTools GUI."""

from typing import Optional, List
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QFrame,
    QPushButton,
    QFileDialog,
    QComboBox,
)
from PySide6.QtCore import Qt

from ..theme import COLORS, DIMENSIONS


class FormField(QWidget):
    """A labeled text input field."""

    def __init__(
        self,
        label: str,
        placeholder: str = "",
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._setup_ui(label, placeholder)

    def _setup_ui(self, label: str, placeholder: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(6)

        self.label = QLabel(label)
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)

        layout.addWidget(self.label)
        layout.addWidget(self.input)

    def text(self) -> str:
        """Get the input text."""
        return self.input.text()

    def setText(self, text: str) -> None:
        """Set the input text."""
        self.input.setText(text)

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable the input."""
        self.input.setEnabled(enabled)


class PasswordField(FormField):
    """A labeled password input field."""

    def _setup_ui(self, label: str, placeholder: str) -> None:
        super()._setup_ui(label, placeholder)
        self.input.setEchoMode(QLineEdit.Password)


class FileField(QWidget):
    """A labeled file input field with browse button."""

    def __init__(
        self,
        label: str,
        placeholder: str = "",
        mode: str = "save",
        file_filter: str = "All Files (*.*)",
        parent: Optional[QWidget] = None
    ):
        """
        Initialize file field.

        Args:
            label: Field label text
            placeholder: Placeholder text for the input
            mode: "save" for output files, "open" for input files
            file_filter: File type filter (e.g., "CSV Files (*.csv)")
            parent: Parent widget
        """
        super().__init__(parent)
        self.mode = mode
        self.file_filter = file_filter
        self._setup_ui(label, placeholder)

    def _setup_ui(self, label: str, placeholder: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(6)

        self.label = QLabel(label)
        layout.addWidget(self.label)

        # Row with input and browse button
        row = QHBoxLayout()
        row.setSpacing(8)

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        row.addWidget(self.input)

        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)
        self.browse_btn.setCursor(Qt.PointingHandCursor)
        self.browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                border: none;
                border-radius: {DIMENSIONS['border_radius_sm']};
                color: {COLORS['text_light']};
                font-size: 13px;
                font-weight: 500;
                padding: 10px 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_light']};
            }}
        """)
        self.browse_btn.clicked.connect(self._browse)
        row.addWidget(self.browse_btn)

        layout.addLayout(row)

    def _browse(self) -> None:
        """Open file dialog for browsing."""
        if self.mode == "save":
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Select Output File",
                self.input.text() or "",
                self.file_filter
            )
        else:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Input File",
                self.input.text() or "",
                self.file_filter
            )

        if path:
            self.input.setText(path)

    def text(self) -> str:
        """Get the input text."""
        return self.input.text()

    def setText(self, text: str) -> None:
        """Set the input text."""
        self.input.setText(text)

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable the input and button."""
        self.input.setEnabled(enabled)
        self.browse_btn.setEnabled(enabled)


class CheckboxField(QWidget):
    """A checkbox with label."""

    def __init__(
        self,
        label: str,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._setup_ui(label)

    def _setup_ui(self, label: str) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)

        self.checkbox = QCheckBox(label)
        layout.addWidget(self.checkbox)
        layout.addStretch()

    def isChecked(self) -> bool:
        """Get the checkbox state."""
        return self.checkbox.isChecked()

    def setChecked(self, checked: bool) -> None:
        """Set the checkbox state."""
        self.checkbox.setChecked(checked)


class FormSection(QFrame):
    """A section of form fields with a title."""

    def __init__(
        self,
        title: str,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self.setProperty("class", "card")
        self._setup_ui(title)

    def _setup_ui(self, title: str) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 24, 24, 24)
        self.layout.setSpacing(8)

        if title:
            self.title_label = QLabel(title)
            self.title_label.setProperty("class", "card_title")
            self.title_label.setStyleSheet(
                "font-size: 16px; font-weight: 600; color: #1a1a2e; margin-bottom: 8px;"
            )
            self.layout.addWidget(self.title_label)

    def addField(self, field: QWidget) -> None:
        """Add a form field to this section."""
        self.layout.addWidget(field)

    def addRow(self, *fields: QWidget) -> None:
        """Add multiple fields in a horizontal row."""
        row = QHBoxLayout()
        row.setSpacing(16)
        for field in fields:
            row.addWidget(field)
        self.layout.addLayout(row)


class ComboBoxField(QWidget):
    """A labeled dropdown/combo box field."""

    def __init__(
        self,
        label: str,
        items: List[str],
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._setup_ui(label, items)

    def _setup_ui(self, label: str, items: List[str]) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(6)

        self.label = QLabel(label)
        self.combo = QComboBox()
        self.combo.addItems(items)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)

    def currentText(self) -> str:
        """Get the currently selected text."""
        return self.combo.currentText()

    def currentIndex(self) -> int:
        """Get the currently selected index."""
        return self.combo.currentIndex()

    def setCurrentIndex(self, index: int) -> None:
        """Set the currently selected index."""
        self.combo.setCurrentIndex(index)

    def setCurrentText(self, text: str) -> None:
        """Set the currently selected text."""
        self.combo.setCurrentText(text)

    def setEnabled(self, enabled: bool) -> None:
        """Enable or disable the combo box."""
        self.combo.setEnabled(enabled)
