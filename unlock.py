import menu
from login import login
from filer import get_filer
from cterasdk import *
import logging

def unlock():
    logging.info('Starting unlock task')
    global_admin = login()
    filer = get_filer(global_admin)
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

def start_ssh():
    """Start SSH Daemon and copy public key to a given Filer"""
    logging.info('Starting task to enable SSH on Filer')
    global_admin = login()
    filer = get_filer(global_admin)
    pubkey = input("Enter a public key or press Enter to create one:\n")
    if pubkey:
        print("Copying existing public key to",filer.name)
        filer.ssh.enable(pubkey)
    else:
        print("Creating a new private key and copying its public key to",
                filer.name)
        try:
            filer.ssh.enable()
        except (CTERAException) as e:
            logging.warning(e)
            logging.warning("Aborted task to enable SSH on Filer")
            print("Error creating new private key")
            print("Does ~/Downloads or %USERPROFILE%\Downloads folder exist?")
            menu.menu()
    print("You now try to ssh to the Filer:",filer.name)
    print("If connection is refused, make sure public key is valid.")
    logging.info('Finished task to enable SSH on Filer')
    menu.menu

