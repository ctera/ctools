"""Button widgets for CTools GUI."""

from typing import Optional, Callable
from PySide6.QtWidgets import QPushButton, QWidget


class PrimaryButton(QPushButton):
    """Primary action button with accent color."""

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(text, parent)
        self.setProperty("class", "btn_primary")
        self.setCursor(Qt.PointingHandCursor)

        if on_click:
            self.clicked.connect(on_click)


class SecondaryButton(QPushButton):
    """Secondary action button with outline style."""

    def __init__(
        self,
        text: str,
        on_click: Optional[Callable] = None,
        parent: Optional[QWidget] = None
    ):
        super().__init__(text, parent)
        self.setProperty("class", "btn_secondary")
        self.setCursor(Qt.PointingHandCursor)

        if on_click:
            self.clicked.connect(on_click)


# Import Qt here to avoid issues
from PySide6.QtCore import Qt
