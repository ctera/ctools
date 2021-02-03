#!/usr/bin/python3
# status.py
# Module for ctools.py, a CTERA Portal/Edge Filer Maintenance Tool
# Version 1.3
import menu
from login import login
from cterasdk import *
import csv, logging, os, re, sys

def status():
    logging.info('Starting status task')
    global_admin = login()
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
        gateway_writer.writerow(['Gateway',
                                 'CloudSync Status',
                                 'selfScanIntervalInHours',
                                 'FilesInUploadQueue',
                                 'scanningFiles',
                                 'selfVerificationscanningFiles',
                                 'MetaLogsSetting',
                                 'MetaLogMaxSize',
                                 'MetaLogMaxFiles',
                                 'CurrentFirmware',
                                 'License',
                                 'EvictionPercentage',
                                 'CurrentVolumeStorage',
                                 'IP Config',
                                 'Alerts',
                                 'TimeServer'])

    for tenant in global_admin.portals.tenants():
        global_admin.portals.browse(tenant.name)
        filers = global_admin.devices.filers(include=['deviceConnectionStatus.connected',
                                                      'deviceReportedStatus.config.hostname'])
        total_devices = 0
        for filer in filers:
            if filer.deviceConnectionStatus.connected:
                total_devices = total_devices + 1
                config = filer.get('/config')
                sync_status = filer.sync.get_status()
                sync_id = sync_status.id
                selfScanIntervalInHours = config.cloudsync.selfScanVerificationIntervalInHours
                FilesInUploadQueue = sync_status.uploadingFiles
                uploadingFiles = sync_status.uploadingFiles
                scanningFiles = sync_status.scanningFiles
                selfVerificationscanningFiles = sync_status.selfVerificationScanningFiles
                CurrentFirmware = filer.get('/status/device/runningFirmware')
                try:
                    MetaLogMaxSize = config.logging.metalog.maxFileSizeMB
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
                IP1 = filer.network.get_status().ip.address
                storageThresholdPercentTrigger = filer.get('/config/cloudsync/cloudExtender/storageThresholdPercentTrigger')
                VolumeStorage = filer.get('/proc/storage/summary')
                _total = VolumeStorage.totalVolumeSpace
                _used = VolumeStorage.usedVolumeSpace
                _free = VolumeStorage.freeVolumeSpace
                volume_summary = "Total: {} Used: {} Free: {}".format(_total,_used,_free)
                dbg_level = filer.support.set_debug_level()
                MetaLogs1 = dbg_level[-28:-18]
                Alerts = config.logging.alert
                TimeServer = config.time
                _mode = TimeServer.NTPMode
                _zone = TimeServer.TimeZone
                _servers = TimeServer.NTPServer
                time_summary = "Mode: {} Zone: {} Servers: {}".format(_mode,_zone,_servers)
                with open(filename, mode='a') as gatewayList:
                    gateway_writer = csv.writer(gatewayList, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    gateway_writer.writerow([filer.name,
                                             sync_id, 
                                             selfScanIntervalInHours,
                                             FilesInUploadQueue,
                                             scanningFiles,
                                             selfVerificationscanningFiles,
                                             MetaLogs1,
                                             MetaLogMaxSize,
                                             MetaLogMaxFiles,
                                             CurrentFirmware,
                                             License,
                                             storageThresholdPercentTrigger,
                                             volume_summary,
                                             IP1,
                                             Alerts,
                                             time_summary])

    global_admin.logout()

    logging.info('Finished status task')
    print('Finished task. Returning to menu.')
    menu.menu()

