import logging
from cterasdk import CTERAException


def suspend_filer_sync(self=None, device_name=None, tenant_name=None):
    """Suspend sync on a device"""
    logging.info("Starting suspend sync task.")
    device = self.devices.device(device_name, tenant_name)
    try:
        device.sync.suspend(wait=True)
        logging.info("Suspended sync on %s", device.name)
    except CTERAException as e:
        logging.warning(e)
        logging.info("Error suspending sync on %s", device.name)
