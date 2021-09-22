from cterasdk import *
from getpass import getpass
import logging, sys

def login(address,username,password):
    try:
        logging.info("Logging into " + address)
        global_admin = GlobalAdmin(address)
        global_admin.login(username, password)
        logging.debug("Successfully logged in to " + address)
        global_admin.portals.browse_global_admin()
        allow_device_sso = global_admin.get('rolesSettings/readWriteAdminSettings/allowSSO')
        if allow_device_sso is True:
            logging.debug('Single Sign On to Devices is allowed')
        else:
            logging.warning("Allow Single Sign On to Devices is not enabled. " +
                            "Some tasks may fail or output may be incomplete")
        return global_admin
    except CTERAException as error:
        logging.warning(error)
        sys.exit("There was a problem logging in. Please try again.")
