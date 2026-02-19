"""Sidebar navigation widget for CTools GUI."""

from typing import Optional, List, Callable, Tuple
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    QButtonGroup,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

from ..theme import COLORS, DIMENSIONS
from ...core.resources import get_resource_path


class NavButton(QPushButton):
    """Navigation button for the sidebar."""

    def __init__(
        self,
        text: str,
        icon: str = "",
        parent: Optional[QWidget] = None
    ):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(44)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
                font-weight: 500;
                padding: 12px 16px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_light']};
                color: {COLORS['text_light']};
            }}
            QPushButton:checked {{
                background-color: {COLORS['accent']};
                color: {COLORS['text_light']};
            }}
        """)


class Sidebar(QFrame):
    """Sidebar navigation component."""

    navigation_changed = Signal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(DIMENSIONS['sidebar_width'])
        self.buttons: List[NavButton] = []
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.setStyleSheet(f"""
            #sidebar {{
                background-color: {COLORS['primary']};
                border: none;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = self._create_header()
        layout.addWidget(header)

        # Navigation scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background-color: transparent;
            }
        """)

        self.nav_container = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_container)
        self.nav_layout.setContentsMargins(12, 8, 12, 8)
        self.nav_layout.setSpacing(4)

        scroll.setWidget(self.nav_container)
        layout.addWidget(scroll)

        # Footer
        footer = self._create_footer()
        layout.addWidget(footer)

    def _create_header(self) -> QFrame:
        """Create the sidebar header with branding."""
        header = QFrame()
        header.setObjectName("sidebar_header")
        header.setFixedHeight(120)
        header.setStyleSheet(f"""
            #sidebar_header {{
                background-color: {COLORS['primary']};
                border-bottom: 1px solid {COLORS['primary_light']};
            }}
        """)

        layout = QVBoxLayout(header)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(4)

        title = QLabel("CTools")
        title.setObjectName("app_title")
        title.setStyleSheet(f"""
            color: {COLORS['text_light']};
            font-size: 26px;
            font-weight: 700;
        """)

        subtitle = QLabel("CTERA Management Suite")
        subtitle.setObjectName("app_subtitle")
        subtitle.setStyleSheet(f"""
            color: {COLORS['accent']};
            font-size: 12px;
            font-weight: 500;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        return header

    def _create_footer(self) -> QFrame:
        """Create the sidebar footer."""
        footer = QFrame()
        footer.setFixedHeight(50)
        footer.setStyleSheet(f"""
            background-color: {COLORS['primary']};
            border-top: 1px solid {COLORS['primary_light']};
        """)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 0, 20, 0)

        version = QLabel("v4.1.1")
        version.setStyleSheet(f"""
            color: rgba(255, 255, 255, 0.5);
            font-size: 12px;
        """)
        layout.addWidget(version)
        layout.addStretch()

        # Add CTERA logo
        try:
            logo_path = get_resource_path("ctera-logo-white.svg")
            renderer = QSvgRenderer(logo_path)
            if renderer.isValid():
                # Get native SVG size and scale to fit footer height while preserving aspect ratio
                default_size = renderer.defaultSize()
                target_height = 20
                aspect_ratio = default_size.width() / default_size.height()
                target_width = int(target_height * aspect_ratio)

                logo_pixmap = QPixmap(target_width, target_height)
                logo_pixmap.fill(Qt.transparent)
                painter = QPainter(logo_pixmap)
                renderer.render(painter)
                painter.end()

                logo_label = QLabel()
                logo_label.setPixmap(logo_pixmap)
                logo_label.setStyleSheet("background: transparent;")
                layout.addWidget(logo_label)
        except Exception:
            pass  # Silently fail if logo can't be loaded

        return footer

    def add_section(self, title: str) -> None:
        """Add a section header to the navigation."""
        label = QLabel(title)
        label.setStyleSheet(f"""
            color: rgba(255, 255, 255, 0.5);
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 16px 4px 8px 4px;
        """)
        self.nav_layout.addWidget(label)

    def add_item(self, text: str, index: int) -> NavButton:
        """Add a navigation item."""
        button = NavButton(text)
        self.buttons.append(button)
        self.button_group.addButton(button, index)
        self.nav_layout.addWidget(button)

        button.clicked.connect(lambda: self.navigation_changed.emit(index))

        return button

    def add_stretch(self) -> None:
        """Add a stretch to push items to the top."""
        self.nav_layout.addStretch()

    def set_current(self, index: int) -> None:
        """Set the currently selected navigation item."""
        if 0 <= index < len(self.buttons):
            self.buttons[index].setChecked(True)
