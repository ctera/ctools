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
    logging.info('Starting task to enable SSH on Filer')
    global_admin = login()
    filer = get_filer(global_admin)
    pubkey = input("Enter the public key:\n")
    cmd = ('exec /config/device startSSHD publicKey "{}"'.format(pubkey))
    filer.cli.run_command(cmd) # TODO: validate public key
    print("You may now try to ssh to the Filer:",filer.name)
    print("If connection is refused, make sure public key is valid.")
    menu.menu

