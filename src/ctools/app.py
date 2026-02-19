"""CTools Application - Main entry point."""

import os
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from .core.resources import get_icon_path


def run_gui() -> int:
    """
    Launch the CTools GUI application.

    Returns:
        Application exit code
    """
    # Enable high DPI scaling
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    # Create application
    app = QApplication(sys.argv)

    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Set application icon - ICO files contain multiple sizes for crisp rendering
    icon_path = get_icon_path()
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        if not icon.isNull():
            app.setWindowIcon(icon)

    # Import here to avoid circular imports
    from .gui import MainWindow

    # Create and show main window
    window = MainWindow()
    window.show()

    return app.exec()


def main() -> None:
    """Main entry point - handles CLI vs GUI mode."""
    if len(sys.argv) > 1:
        # CLI mode
        from .cli.main import cli_main
        cli_main()
    else:
        # GUI mode
        sys.exit(run_gui())


if __name__ == "__main__":
    main()
