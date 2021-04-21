from filer import get_filer
from cterasdk import *
import logging

def suspend_filer_sync(self):
    """Suspend sync on a device"""
    logging.info("Starting suspend sync task.")
    self = get_filer(self)
    try:
        self.sync.suspend(wait=True)
        print("Suspended sync on",self.name)
    except CTERAException as e:
        logging.warning(e)
        print("Error suspending sync on",self.name)

if __name__ == "__main__":
    suspend_filer_sync()
