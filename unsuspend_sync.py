import logging
from cterasdk import CTERAException


def unsuspend_filer_sync(self=None, device_name=None, tenant_name=None):
    """Unsuspend sync on a device"""
    logging.info("Starting unsuspend sync task.")
    device = self.devices.device(device_name, tenant_name)
    try:
        device.sync.unsuspend()
        logging.info("Unsuspended sync on %s", device.name)
    except CTERAException as e:
        logging.warning(e)
        logging.info("Error unsuspending sync on %s", device.name)
