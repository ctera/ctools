#!/usr/bin/python3
# unlock.py
# Module for ctools.py, a CTERA Portal/Edge Filer Maintenance Tool
# Get device name, firmware, and MAC and prompt for unlock code.
# Version 0.1 
from login import login
from cterasdk import *
import logging

def get_info():
 
    global_admin = login()
    global_admin.portals.browse_global_admin()
    for tenant in global_admin.portals.tenants():
        global_admin.portals.browse(tenant.name)
        filers = global_admin.devices.filers(include=['deviceConnectionStatus.connected'])
        for filer in filers:
            if filer.deviceConnectionStatus.connected:
                device_name = filer.name
                firmware = filer.get('/status/device/runningFirmware')
                mac = filer.get('/status/device/MacAddress')
                print(tenant.name, filer.name, firmware, mac)
                unlock(filer)
 
def unlock(filer):
    try:
        code = input("Enter unlock code: ")
    except CTERAException as error:
        logging.warning(error)
        print("Something went wrong with the prompt.")
    try:
        filer.telnet.enable(code)
    except CTERAException as error:
        logging.warning(error)
        print("Bad code or something went wrong unlocking device.")

# uncomment to debug module by running `python unlock.py`
#get_info()
