#!/usr/bin/python3
# status.py
# Module for ctools.py, a CTERA Portal/Edge Filer Maintenance Tool
# Version 1.3
import menu
from filer import get_filers
from login import login
from cterasdk import *
import csv, logging, os, re, sys

def write_status(p_filename):
    """Save and write Filer status information to filename param."""
    global_admin = login()
    for filer in get_filers(global_admin):
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
        uptime = filer.get('/proc/time/uptime')
        performance = filer.get('/proc/perfMonitor')
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

        """Parse Performance History"""
        #def get_perf_history():
        #    for sample in performance.samples:
        #        samples.append("{} CPU: {} Mem {}".format(sample.timestamp,sample.cpu,sample.memUsage))
        #    return samples

        def get_max_cpu():
            cpu_history = []
            for i in performance.samples:
                cpu_history.append(i.cpu)
            return max(cpu_history)

        def get_max_memory():
            memory_history = []
            for i in performance.samples:
                memory_history.append(i.memUsage)
            return max(memory_history)


        """Write results to output filename"""
        with open(p_filename, mode='a') as gatewayList:
            gateway_writer = csv.writer(gatewayList, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            gateway_writer.writerow([
                    filer.name,
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
                    time_summary,
                    uptime,
                    "CPU: {} Mem: {}".format(performance.current.cpu,performance.current.memUsage),
                    get_max_cpu(),
                    get_max_memory(), 
                    ])
    global_admin.logout()

def write_header(p_filename):
    """Write CSV header to given filename parameter """
    try:
        with open(p_filename, mode='a') as gatewayList:
            gateway_writer = csv.writer(
                    gatewayList,
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL
                    )
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
                                     'TimeServer',
                                     'uptime',
                                     'Current Performance',
                                     'Max CPU',
                                     'Max Memory',
                                     ])
    except FileNotFoundError as error:
        logging.error(error)
        print("ERROR: Unable to open filename specified: {}".format(p_filename))
        sys.exit("Make sure you entered a valid file name and it exists")

def create_csv():
    """Prompt to create a CSV or append to existing. Return filename."""
    _filename = input("Enter output filename. Make sure extension is csv: ")
    if os.path.exists(_filename):
        print ('File exists. It will be deleted and a new one will be created')
        deletefile = input("Delete File? Type Y/n: ")
        if deletefile in ('Y', 'y'):
            os.remove(_filename)
            write_header(_filename)
        if deletefile in ('N', 'n'):
            print ('Contents will be appended to the existing file')
    else:
        print("Output file does not exist. Creating new file")
        write_header(_filename)
    return _filename

def run_status():
    logging.info('Starting status task')
    filename = create_csv()
    write_status(filename)
    logging.info('Finished status task.')
    menu.menu()

