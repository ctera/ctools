#!/usr/bin/python3
# ctools.py
# CTERA Portal/Edge Filer Maintenance Tool
# Version 1.5
from menu import menu
from cterasdk import *
import logging

if __name__ == "__main__":
    logging.info('Starting ctools')
    menu()

