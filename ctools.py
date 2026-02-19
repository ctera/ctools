#!/usr/bin/env python3
"""
CTools - A GUI and CLI toolset for CTERA environments.

This file serves as the entry point for both development and PyInstaller builds.
"""

import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ctools.app import main

if __name__ == "__main__":
    main()
