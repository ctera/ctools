import logging
import os
import sys
import requests
import csv
import re
from cterasdk import *
from sample_base import CTERASDKSampleBase
from getpass import getpass
requests.packages.urllib3.disable_warnings()

def status():
    address = input("Portal (IP, Hostname or FQDN): ")
    username = input("Admin Username: ")
    password = getpass("Admin Password: ")
    filename = input("Output filename. Make sure extension is csv: ")

    global_admin = GlobalAdmin(address)
    global_admin.login(username, password)
    global_admin.portals.browse_global_admin()
    
    import os
    if os.path.exists(filename):
        print ('File exists. It will be deleted and a new one will be created')
        deletefile = input("Delete File? Type Y/N: ")
        if deletefile in ('Y', 'y'):
            os.remove(filename)
        if deletefile in ('N', 'n'):
            print ('Contents will be appended to the existing file')
    else:
        print("The file does not exist")
        
    import csv
    with open(filename, mode='a') as gatewayList:
        gateway_writer = csv.writer(gatewayList, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        gateway_writer.writerow(['Gateway', 'CloudSync Status', 'selfScanIntervalInHours', 'FilesInUploadQueue', 'scanningFiles', 'selfVerificationscanningFiles', 'MetaLogsSetting', 'MetaLogMaxSize', 'MetaLogMaxFiles', 'CurrentFirmware', 'License', 'EvictionPercentage', 'CurrentVolumeStorage', 'IP Config'])
    
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
                    MetaLogMaxSize = ('Not Applicable')
                try:
                    MetaLogMaxFiles = filer.get('/config/logging/metalog/maxfiles')
                except:
                    MetaLogMaxFiles = ('Not Applicable')
                License = filer.licenses.get()
                IP = filer.network.ipconfig()
                IPstr = str(IP)
                IP1 = re.findall ('address.*', IPstr)            
                storageThresholdPercentTrigger = filer.get('/config/cloudsync/cloudExtender/storageThresholdPercentTrigger')
                VolumeStorage = filer.get('/proc/storage/summary')
                MetaLogs = filer.cli.run_command('dbg le')
                MetaLogsstr = str(MetaLogs)
                MetaLogs1 = re.findall ('...........Current.*', MetaLogsstr)
                import csv
                with open(filename, mode='a') as gatewayList:
                    gateway_writer = csv.writer(gatewayList, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    gateway_writer.writerow([filer.name, cloudSyncStatus1, selfScanIntervalInHours, FilesInUploadQueue, scanningFiles, selfVerificationscanningFiles, MetaLogs1, MetaLogMaxSize, MetaLogMaxFiles, CurrentFirmware, License, storageThresholdPercentTrigger, VolumeStorage, IP1])
#                import sys
#                sys.stdout = open('output.csv','a')
#                print(filer.name, selfScanIntervalInHours, FilesInUploadQueue, scanningFiles, selfVerificationscanningFiles,MetaLogs1, MetaLogMaxSize, MetaLogMaxFiles, CurrentFirmware, License, storageThresholdPercentTrigger, VolumeStorage, IP1)

                        
    global_admin.logout()


  


if __name__ == "__main__":
    status()