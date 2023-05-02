import logging

from cterasdk import CTERAException
from filer import get_filer, get_filers


def single_filer_run(filer, command: str):
    """Run command against a single device on current tenant.

    :param str command: command to run
    :param str device_name: Name of device on current tenant
    """
    try:
        response = filer.cli.run_command(command)
        logging.info(response)
        logging.info("Finished single run_cmd task on %s", filer.name)
    except AttributeError as ae:
        logging.debug(ae)
    except CTERAException as ce:
        logging.debug(ce)
        logging.info("Failed run_cmd task on %s", filer.name)


def multi_filer_run(self, command: str, all_tenants=False):
    """Run command against all devices on a tenant or all tenants.

    :param str command: command to run
    :param bool,optional all_tenants: Scan all tenants
    """
    filers = get_filers(self, all_tenants)
    for filer in filers:
        try:
            logging.info("Running command on: %s", filer.name)
            response = filer.cli.run_command(command)
            logging.info(response)
            logging.info("Finished command on: %s", filer.name)
        except CTERAException as error:
            logging.debug(error)
            logging.warning("Something went wrong running the command on %s", filer.name)


def run_cmd(self, command: str, all_tenants=False, device_name=None):
    """Run a "hidden CLI command" on connected Filers.
    i.e. execute a RESTful API request to connected Filers, and
    print the response. On CLI, quote the command string.

    :param str command: command to be run
    :param bool,optional all_tenants: Scan all tenants true or false
    :param str,optional device_name: Name of device on current tenant
    """
    logging.info('Starting run_cmd task.')
    tenant = self.users.session().user.tenant
    if device_name:
        filer = get_filer(self, device_name, tenant)
        single_filer_run(filer, command)
    elif all_tenants is True:
        multi_filer_run(self, command, all_tenants=True)
        logging.info('Finished run_cmd task on all Filers.')
    else:
        multi_filer_run(self, command, all_tenants=False)
        logging.info("Finished run_cmd task on all Filers in Tenant: %s", tenant)
