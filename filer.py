from cterasdk import *
import logging, sys
from tkinter import messagebox


def get_filer(mode, self, device_name, tenant_p):
    """Prompt for Filer and Return Filer object if found"""
    if mode == 'T':
        device = input("Enter device name: ")
        tenant = input("Enter tenant portal of " + device + " : ")
    # passing values
    else:
        device = device_name
        tenant = tenant_p
    try:
        filer = self.devices.device(device, tenant)
        if mode == 'G':
            messagebox.showinfo("Success", "Device found.")
        print("Device found.")
        return filer
    except CTERAException as error:
        logging.warning(error)
        print("Device not found.")
        if mode == 'G':
            messagebox.showerror("Error:", "Device not found." + error)
        else:
            sys.exit("Exiting...")


def get_filers(self):
    """Return all connected Filers from each Tenant"""
    connected_filers = []
    for tenant in self.portals.tenants():
        self.portals.browse(tenant.name)
        all_filers = self.devices.filers(include=[
            'deviceConnectionStatus.connected',
            'deviceReportedStatus.config.hostname'])
        for filer in all_filers:
            if filer.deviceConnectionStatus.connected:
                connected_filers.append(filer)
    return connected_filers
