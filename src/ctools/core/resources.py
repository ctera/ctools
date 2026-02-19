"""Resource path utilities for CTools."""

import os
import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and PyInstaller bundle.

    Args:
        relative_path: Path relative to the assets folder

    Returns:
        Absolute path to the resource
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = Path(sys._MEIPASS)
    else:
        # Running in development
        base_path = Path(__file__).parent.parent.parent.parent

    return str(base_path / "assets" / relative_path)


def get_logo_path() -> str:
    """Get the path to the logo image."""
    return get_resource_path("logo.png")


def get_icon_path() -> str:
    """Get the path to the application icon."""
    return get_resource_path("ctools.ico")
