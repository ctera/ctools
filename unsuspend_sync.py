from filer import get_filer
from cterasdk import *
import logging

def unsuspend_filer_sync(self):
    """Unsuspend sync on a device"""
    logging.info("Starting unsuspend sync task.")
    self = get_filer(self)
    try:
        self.sync.unsuspend()
        print("Unsuspended sync on",self.name)
    except CTERAException as e:
        logging.warning(e)
        print("Error unsuspending sync on",self.name)

if __name__ == "__main__":
    unsuspend_filer_sync()
