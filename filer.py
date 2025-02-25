import logging
from cterasdk import CTERAException


def get_filer(self, device=None, tenant=None):
    """Return Filer object if found"""
    try:
        filer = self.devices.device(device, tenant)
        return filer
    except CTERAException as error:
        logging.debug(error)
        logging.error("Device not found.")
        return None


def get_filers(self, all_tenants=False, tenant=None):
    try:
        """Return all connected Filers from Admin Portal or Tenant"""
        connected_filers = []
        if all_tenants is True:
            self.portals.browse_global_admin()

            #tenant = self.users.session().current_tenant()

            tenant = self.users.session().user.tenant
            logging.info("Getting all Filers since tenant is %s", tenant)
            for tenant in self.portals.tenants():
                self.portals.browse(tenant.name)
                all_filers = self.devices.filers(include=[
                        'deviceConnectionStatus.connected',
                        'deviceReportedStatus.config.hostname'])
                connected_filers.extend([filer for filer in all_filers if filer.deviceConnectionStatus.connected])
        elif tenant is not None:
            logging.info("Getting Filers connected to %s", tenant)
            self.portals.browse(tenant)
            tenant_filers = self.devices.filers(include=[
                        'deviceConnectionStatus.connected',
                        'deviceReportedStatus.config.hostname'])
            connected_filers.extend([filer for filer in tenant_filers if filer.deviceConnectionStatus.connected])
        else:
            current_tenant = self.users.session().user.tenant
            logging.info("Getting Filers connected to %s", current_tenant)
            tenant_filers = self.devices.filers(include=[
                        'deviceConnectionStatus.connected',
                        'deviceReportedStatus.config.hostname'])
            connected_filers.extend([filer for filer in tenant_filers if filer.deviceConnectionStatus.connected])
        return connected_filers
    except CTERAException as error:
        logging.debug(error)
        logging.error("Error getting Filers.")
        return None
