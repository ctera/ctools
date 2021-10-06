from filer import get_filer
from cterasdk import *
import logging, sys

def enable_telnet(self,device_name,tenant_name,code=None):
    """Enable telnet if code is given. Else, print info needed for code."""
    logging.info('Starting enable_telnet task')
    filer = self.devices.device(device_name,tenant_name)
    if code is None:
        print("No code provided. Getting required info.")
        #get_telnet_info(filer)
        mac = filer.get('/status/device/MacAddress')
        firmware = filer.get('/status/device/runningFirmware')
        print("Provide the following to CTERA to unlock",filer.name)
        print(mac)
        print(firmware)
        print("Then re-run this task with the 6 digit code")
        logging.info("Provide info CTERA Support: {} {}".format(mac,firmware))
        logging.info("Finished enable_telnet task with no code given.")
    else:
        print("Attempting to use telnet unlock code: " + code)
        try:
            filer.telnet.enable(code)
            print("Success. Telnet enabled on",filer.name)
        except CTERAException as error:
            logging.warning(error)
            logging.warning("Bad code or something went wrong unlocking device.")
            print("Bad code or something went wrong unlocking device.")
        logging.info("Finished enable_telnet task with code.")

def start_ssh(self,device_name,tenant_name,pubkey=None):
    """Start SSH Daemon on given 7.0+ Filer
        If provided, copy public key to a given Filer
        If no public key: - Create a new keypair using device_name
        Save device_name.pub and device_name.pem to $HOME\Downloads
    """
    logging.info('Starting task to enable SSH on Filer')
    filer = self.devices.device(device_name,tenant_name)
    if pubkey:
        logging.info("Copying provided public key to Filer: {}.".format(device_name))
        filer.ssh.enable(pubkey)
    else:
        logging.info("Creating new public/private key pair for Filer {} in $HOME\Downloads."
                .format(device_name))
        try:
            filer.ssh.enable()
        except (CTERAException) as e:
            logging.warning(e)
            logging.warning("Aborted task to enable SSH on Filer")
            logging.warning("Error creating new private key")
    logging.info('Finished task to enable SSH on Filer')

def disable_ssh(self,device_name,tenant_name):
    """Stop SSH Daemon on a given Filer"""
    logging.info('Starting task to disable SSH on Filer: {} on Tenant: {}'.format(
                device_name,tenant_name))
    filer = self.devices.device(device_name,tenant_name)
    filer.ssh.disable()
    logging.info('Finished task to disable SSH on Filer: {} on Tenant: {}'.format(
                device_name,tenant_name))
