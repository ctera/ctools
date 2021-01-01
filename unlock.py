#!/usr/bin/python3
# unlock.py
# Module for ctools.py, a CTERA Portal/Edge Filer Maintenance Tool
# Get device name, firmware, and MAC and prompt for unlock code.
# Version 0.1 
from login import login
from cterasdk import *
import logging

def unlock():
    global_admin = login()
    print("Devices able to unlock")
    print('Tenant | Filer Name | Firmware | MAC Address | IP Address')
    for tenant in global_admin.portals.tenants():
        global_admin.portals.browse(tenant.name)
        filers = global_admin.devices.filers(include=['deviceConnectionStatus.connected'])
        for filer in filers:
            if filer.deviceConnectionStatus.connected:
                firmware = filer.get('/status/device/runningFirmware')
                mac = filer.get('/status/device/MacAddress')
                ip = filer.get('/status/network/ports/0/ip/address')
                print(tenant.name, filer.name, firmware, mac, ip)
    device = input("Enter device name to unlock: ")
    tenant = input("Enter tenant portal of " + device + " : ")
    filer = global_admin.devices.device(device, tenant)
    enable(filer)

def enable(filer):
    try:
        code = input("Enter unlock code: ")
    except CTERAException as error:
        logging.warning(error)
        print("Something went wrong with the prompt.")
    try:
        filer.telnet.enable(code)
        print('Success. Telnet access unlocked')
    except CTERAException as error:
        logging.warning(error)
        print("Bad code or something went wrong unlocking device.")

