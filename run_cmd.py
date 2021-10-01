import logging
from filer import get_filer, get_filers

def single_filer_run(self, command: str,device_name=None):
    """Run command against a single device on current tenant.

    :param str command: command to be run
    :param str,optional device_name: Name of device on current tenant
    """
    tenant = self.users.session().user.tenant
    filer = self.devices.device(device_name, tenant)
    logging.info(f"Running command on: {filer.name}")
    response = filer.cli.run_command(command)
    logging.info(response)
    logging.info(f"Finished command on: {filer.name}")

def multi_filer_run(self, command: str,all_tenants=False):
    """Run command against all devices on a tenant or all tenants.

    :param str command: command to be run
    :param bool,optional all_tenants: Scan all tenants ture or false
    """
    filers = get_filers(self,all_tenants)
    for filer in filers:
        try:
            logging.info(f"Running command on: {filer.name}")
            response = filer.cli.run_command(command)
            logging.info(f"Finished command on: {filer.name}")
        except CTERAException as error:
            logging.warning(error)
            print("Something went wrong running the command")

def run_cmd(self,command: str,all_tenants=False,device_name=None):
    """Run a "hidden CLI command" on connected Filers.
    i.e. execute a RESTful API request to connected Filers, and
    print the response. On CLI, use quotes around the command.

    :param str command: command to be run
    :param bool,optional all_tenants: Scan all tenants ture or false
    :param str,optional device_name: Name of device on current tenant
    """
    logging.info('Starting run_cmd task')
    if device_name:
        single_filer_run(self,command,device_name)
        logging.info('Finished single run_cmd task.')
    elif all_tenants is True:
        multi_filer_run(self,command,all_tenants=True)
        logging.info('Finished run_cmd task on all Tenants.')
    else:
        tenant = self.users.session().user.tenant
        multi_filer_run(self,command,all_tenants=False)
        logging.info(f"Finished run_cmd task on all Filers in Tenant: {tenant}.")

