# return a single filer 
from cterasdk import *
import logging

def get_filer(self):
    device = input("Enter device name: ")
    tenant = input("Enter tenant portal of " + device + " : ")
    try:
        filer = self.devices.device(device, tenant)
        print("Device found.")
        return filer
    except CTERAException as error:
        logging.warning(error)
        print("Device not found.")

