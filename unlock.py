from filer import get_filer
from cterasdk import *
import logging, sys

def unlock(self):
    logging.info('Starting unlock task')
    filer = get_filer(self)
    info(filer)
    enable(filer)
    logging.info('Finished unlock task')
    print('Finished task.')

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

def start_ssh(self):
    """Start SSH Daemon and copy public key to a given Filer"""
    logging.info('Starting task to enable SSH on Filer')
    filer = get_filer(self)
    pubkey = input("Enter a public key or press Enter to create one:\n")
    if pubkey:
        print("Copying existing public key to",filer.name)
        filer.ssh.enable(pubkey)
    else:
        print("Creating a new private key and copying its public key to",
                filer.name)
        try:
            filer.ssh.enable()
            # TODO: Fix this error when no pubkey is provided.
            # TypeError: generate_private_key() missing 1 required positional argument: 'backend'
        except (CTERAException) as e:
            logging.warning(e)
            logging.warning("Aborted task to enable SSH on Filer")
            print("Error creating new private key")
            print("Does ~/Downloads or %USERPROFILE%\Downloads folder exist?")
            sys.exit("Exiting ctools.")
    print("You now try to ssh to the Filer:",filer.name)
    print("If connection is refused, make sure public key is valid.")
    logging.info('Finished task to enable SSH on Filer')
    sys.exit("Exiting ctools.")

def disable_ssh(self):
    """Stop SSH Daemon on a given Filer"""
    logging.info('Starting task to disable SSH on Filer')
    filer = get_filer(self)
    filer.ssh.disable()
    logging.info('Finished task to disable SSH on Filer')
