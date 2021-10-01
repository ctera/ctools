from cterasdk import *
import logging,sys

def get_filer(self,device=None,tenant=None):
    """Prompt for Filer and Return Filer object if found"""
    try:
        filer = self.devices.device(device, tenant)
        print("Device found.")
        return filer
    except CTERAException as error:
        logging.warning(error)
        print("Device not found.")
        sys.exit("Exiting...")

def get_filers(self,all_tenants=False):
    """Return all connected Filers from Admin Portal or Tenant"""
    connected_filers = []
    if all_tenants is True:
        self.portals.browse_global_admin()
        tenant = self.users.session().user.tenant
        logging.info("Getting all Filers since tenant is " + tenant)
        for tenant in self.portals.tenants():
            self.portals.browse(tenant.name)
            all_filers = self.devices.filers(include=[
                    'deviceConnectionStatus.connected',
                    'deviceReportedStatus.config.hostname'])
            for filer in all_filers:
                if filer.deviceConnectionStatus.connected:
                    connected_filers.append(filer)
    else:
        tenant = self.users.session().user.tenant
        logging.info("Getting Filers connected to " + tenant)
        tenant_filers = self.devices.filers(include=[
                    'deviceConnectionStatus.connected',
                    'deviceReportedStatus.config.hostname'])
        for filer in tenant_filers:
            if filer.deviceConnectionStatus.connected:
                connected_filers.append(filer)
    return connected_filers

