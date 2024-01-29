import logging
from getpass import getpass
from filer import get_filer, get_filers

from cterasdk import CTERAException


def reset_filer_password(self, device_name, tenant_name, user_name, filer_password, all_filers_flag=False):
    """Set/reset a local user's password on specified Filer"""
    logging.info("Starting reset_password task.")
    try:
        if not all_filers_flag:
            filer = get_filer(device_name, tenant_name)
            filer.users.modify(user_name, filer_password)
            logging.info("Success. Password set for %s", user_name)
            logging.info("Finished reset_password task.")
        else:
            filers = get_filers(self, True)
            for filer in filers:
                filer.users.modify(user_name, filer_password)
                logging.info("Success. Password set for " + str(user_name) + " on filer: " + str(filer.name))
            logging.info("Finished reset_password task.")
    except CTERAException as error:
        logging.debug(error)
        logging.error("Failed reset_password task. Make sure that the password is 8 characters and contains at least one letter, one digit and one special character")