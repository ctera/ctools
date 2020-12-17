#!/usr/bin/python3
# ctools.py
# CTERA Portal/Edge Filer Maintenance Tool
# Version 1.2
import logging
import os
import sys
import requests
import csv
import re
from cterasdk import *
#from sample_base import CTERASDKSampleBase
from getpass import getpass
requests.packages.urllib3.disable_warnings()

def login():
    try:
        address = input("Portal (IP, Hostname or FQDN): ")
        username = input("Admin Username: ")
        password = getpass("Admin Password: ")
    except CTERAException as error:
        logging.error(error)
    
    try:
        logging.info("Logging into " + address)
        global_admin = GlobalAdmin(address)
        global_admin.login(username, password)
        logging.info("Successfully logged in to " + address)
        return global_admin
    except CTERAException as error:
        logging.warning(error)

def status():
   
    global_admin = login()
    global_admin.portals.browse_global_admin()
    filename = input("Enter output filename. Make sure extension is csv: ")
    import os
    if os.path.exists(filename):
        print ('File exists. It will be deleted and a new one will be created')
        deletefile = input("Delete File? Type Y/N: ")
        if deletefile in ('Y', 'y'):
            os.remove(filename)
        if deletefile in ('N', 'n'):
            print ('Contents will be appended to the existing file')
    else:
        print("Output file does not exist. Creating new file")
        
    import csv
    with open(filename, mode='a') as gatewayList:
        gateway_writer = csv.writer(gatewayList, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        gateway_writer.writerow(['Gateway', 'CloudSync Status', 'selfScanIntervalInHours', 'FilesInUploadQueue', 'scanningFiles', 'selfVerificationscanningFiles', 'MetaLogsSetting', 'MetaLogMaxSize', 'MetaLogMaxFiles', 'CurrentFirmware', 'License', 'EvictionPercentage', 'CurrentVolumeStorage', 'IP Config', 'Alerts'])

    for tenant in global_admin.portals.tenants():
        global_admin.portals.browse(tenant.name)
        filers = global_admin.devices.filers(include=['deviceConnectionStatus.connected', 'deviceReportedStatus.config.hostname'])
        total_devices = 0
        for filer in filers:
            if filer.deviceConnectionStatus.connected:
                total_devices = total_devices + 1
                cloudSyncStatus = filer.get('/proc/cloudsync/serviceStatus')
                cloudSyncStatusstr = str(cloudSyncStatus)
                cloudSyncStatus1 = re.findall('id.*', cloudSyncStatusstr)
                selfScanIntervalInHours = filer.get('/config/cloudsync/selfScanVerificationIntervalInHours')
                FilesInUploadQueue = filer.get('/proc/cloudsync/serviceStatus/uploadingFiles')
                scanningFiles = filer.get('/proc/cloudsync/serviceStatus/scanningFiles')
                selfVerificationscanningFiles = filer.get('/proc/cloudsync/serviceStatus/selfVerificationScanningFiles')
                CurrentFirmware = filer.get('/status/device/runningFirmware')
                try:
                    MetaLogMaxSize = filer.get('/config/logging/metalog/maxFileSizeMB')
                except:
                    try:
                        MetaLogMaxSize = filer.get('/config/logging/log2File/maxFileSizeMB')
                    except:
                        MetaLogMaxSize = ('Not Applicable')
                try:
                    MetaLogMaxFiles = filer.get('/config/logging/metalog/maxfiles')
                except:
                    try:
                        MetaLogMaxFiles = filer.get('/config/logging/log2File/maxfiles')
                    except:
                        MetaLogMaxFiles = ('Not Applicable')
                try:
                    MetaLogs = filer.cli.run_command('dbg le')
                except:
                    MetaLogs = ('Not Applicable')
                License = filer.licenses.get()
                IP = filer.network.ipconfig()
                IPstr = str(IP)
                IP1 = re.findall ('address.*', IPstr)
                storageThresholdPercentTrigger = filer.get('/config/cloudsync/cloudExtender/storageThresholdPercentTrigger')
                VolumeStorage = filer.get('/proc/storage/summary')
                #MetaLogs = filer.cli.run_command('dbg le')
                MetaLogsstr = str(MetaLogs)
                MetaLogs1 = re.findall ('...........Current.*', MetaLogsstr)
                Alerts = filer.get('/config/logging/alert')
                #MetaLogs1 = 'test'
                import csv
                with open(filename, mode='a') as gatewayList:
                    gateway_writer = csv.writer(gatewayList, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    gateway_writer.writerow([filer.name, cloudSyncStatus1, selfScanIntervalInHours, FilesInUploadQueue, scanningFiles, selfVerificationscanningFiles, MetaLogs1, MetaLogMaxSize, MetaLogMaxFiles, CurrentFirmware, License, storageThresholdPercentTrigger, VolumeStorage, IP1, Alerts])
#                import sys
#                sys.stdout = open('output.csv','a')
#                print(filer.name, selfScanIntervalInHours, FilesInUploadQueue, scanningFiles, selfVerificationscanningFiles,MetaLogs1, MetaLogMaxSize, MetaLogMaxFiles, CurrentFirmware, License, storageThresholdPercentTrigger, VolumeStorage, IP1, Alerts)

    global_admin.logout()

# Print possible tasks and prompt user to pick a task by entering corresponding number.
def switch():
    print("Tasks to run:\n1. Get Details of all Connected Edge Filers to a specific Portal.")
    option = int(input("Enter a task number to execute: "))
    tasks.get(option,default)()

# Dictionary to map numbers to functions/tasks user can choose to run.
tasks = {
        1 : status,
}
# If an invalid number is entered, call this function and exit.
def default():
    print("ERROR: Invalid option given.")
    logging.warning("Invalid option given. Exiting ctools.exe")

if __name__ == "__main__":
    switch()

