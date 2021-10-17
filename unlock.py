import logging
from cterasdk import CTERAException


def catch(error=None, device_name=None):
    logging.debug(error)
    logging.error("Unable to complete task for device: %s", device_name)


def enable_telnet(self, device_name, tenant_name, code=None):
    """Enable telnet if code is given. Else, print info needed for code."""
    logging.info('Starting enable_telnet task')
    try:
        filer = self.devices.device(device_name, tenant_name)
    except CTERAException as error:
        catch(error, device_name)
    if code is None:
        logging.info("No code provided. Getting required info.")
        mac = filer.get('/status/device/MacAddress')
        firmware = filer.get('/status/device/runningFirmware')
        logging.info("Provide info CTERA Support: %s %s", mac, firmware)
        logging.info("Then re-run this task with the 7 digit code.")
        logging.info("Finished enable_telnet task with no code given.")
    else:
        logging.info("Attempting to use telnet unlock code: %s", code)
        try:
            filer.telnet.enable(code)
            logging.info("Success. Telnet enabled on %s.", filer.name)
            logging.info("Finished enable_telnet task with code.")
        except CTERAException as error:
            logging.debug(error)
            logging.info("Bad code or something went wrong unlocking device.")


def start_ssh(self, device_name, tenant_name, pubkey=None):
    """
    Start SSH Daemon on given 7.0+ Filer
    If provided, copy public key to given Filer
    If no public key, create a new keypair using device_name
    Save device_name.pub and device_name.pem to Downloads folder.
    """
    logging.info("Starting task to enable SSH on Filer.")
    try:
        filer = self.devices.device(device_name, tenant_name)
        filer.ssh.enable(public_key=pubkey)
        logging.info("Finished task to enable SSH on Filer.")
    except (CTERAException) as error:
        catch(error, device_name)
        logging.info("Failed task to enable SSH on Filer.")


def disable_ssh(self, device_name, tenant_name):
    """Stop SSH Daemon on a given Filer"""
    logging.info("Starting task to disable SSH on Filer: %s on Tenant: %s", device_name, tenant_name)
    try:
        filer = self.devices.device(device_name, tenant_name)
        filer.ssh.disable()
        logging.info("Finished task to disable SSH on Filer: %s on Tenant: %s.", device_name, tenant_name)
    except (CTERAException) as error:
        catch(error, device_name)
        logging.info("Failed task to disable SSH on Filer.")
