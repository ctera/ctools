#!/usr/bin/python3
# unlock.py
# Module for ctools.py, a CTERA Portal/Edge Filer Maintenance Tool
# Get device name, return firmware, and MAC and prompt for unlock code.
# Version 0.2 
import menu
from login import login
from cterasdk import *
import logging

def unlock():
    logging.info('Starting unlock task')
    global_admin = login()
    device = input("Enter device name to unlock: ")
    tenant = input("Enter tenant portal of " + device + " : ")
    try:
        filer = global_admin.devices.device(device, tenant)
        print("Device found.")
    except CTERAException as error:
        logging.warning(error)
        print("Device not found.")
    info(filer)
    enable(filer)

    logging.info('Finished unlock task')
    print('Finished task. Returning to menu.')
    menu.menu()
def info(filer):
    mac = filer.get('/status/device/MacAddress')
    firmware = filer.get('/status/device/runningFirmware')
    print("Provide the following to CTERA to unlock",filer.name)
    print(mac)
    print(firmware)

def enable(filer):
    try:
        code = input("Enter unlock code: ")
    except CTERAException as error:
        logging.warning(error)
        print("Something went wrong with the prompt.")
    try:
        filer.telnet.enable(code)
        print("Success. Telnet enabled on",filer.name)
    except CTERAException as error:
        logging.warning(error)
        print("Bad code or something went wrong unlocking device.")

