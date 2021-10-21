import logging
import sys
from io import StringIO
import urllib3

from cterasdk.object import GlobalAdmin
from cterasdk import CTERAException
from cterasdk import config as cterasdk_config


def check_allow_device_sso(self):
    """
    Check if 'Allow Single Sign On to Devices' is enabled for
    read-write admins of the current tenant. If not, log a warning.

    :param self: GlobalAdmin instance
    """
    device_sso = self.get('rolesSettings/readWriteAdminSettings/allowSSO')
    if device_sso is True:
        logging.debug('Single Sign On to Devices is allowed.')
    else:
        logging.warning("Allow Single Sign On to Devices is not enabled.")
        logging.warning("Some tasks may fail or output may be incomplete.")


def handle_exceptions(address: str, error):
    """
    Catch and log exceptions then exit.
    If untrusted cert is detected, cancel task and suggest ignore flag.

    :param str address: Portal IP, hostname, or FQDN
    """
    if error.message == 'Untrusted security certificate':
        logging.info("Not proceeding with login.")
        logging.warning('Invalid or expired certificate found at %s', address)
        logging.info("Verify certificate or use ignore_cert flag to proceed.")
        sys.exit("Exiting ctools.")
    elif error.reason == "Forbidden":
        logging.debug(error)
        logging.info("Access denied")
    else:
        logging.info("There was a problem logging in.")
        logging.debug(error)
        sys.exit("Exiting ctools.")


def global_admin_login(address: str, username: str, password: str, ignore_cert=False):
    """
    Log into provided portal address and return GlobalAdmin object.
    If prompted to proceed with insecure connection, answer no.
    If --ignore_cert is set, then trust the cert and disable warnings.

    :param str address: Portal IP, hostname, or FQDN
    :param str username: User name to log in as
    :param str password: User password
    :param bool,optional ignore_cert: Ignore and disable certificate warnings
    """
    if ignore_cert is True:
        cterasdk_config.http['ssl'] = 'Trust'
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    sys.stdin = StringIO('n')  # if prompted, answer no
    try:
        logging.info("Logging into %s", address)
        global_admin = GlobalAdmin(address)
        global_admin.login(username, password)
        logging.debug("Successfully logged in to %s", address)
        check_allow_device_sso(global_admin)
        return global_admin
    except CTERAException as error:
        handle_exceptions(address, error)
        return None
