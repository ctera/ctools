from filer import get_filers
from cterasdk import *
import csv, logging, os, re, sys

def write_status(self,p_filename,all_tenants):
    """Save and write Filer status information to given filename."""
    get_list = ['config',
                'status',
                'proc/cloudsync',
                'proc/time/',
                'proc/storage/summary',
                'proc/perfMonitor']
    for filer in get_filers(self,all_tenants):
        info = filer.get_multi('', get_list)
        tenant = filer.session().user.tenant
        sync_id = info.proc.cloudsync.serviceStatus.id
        try:
            selfScanIntervalInHours = info.config.cloudsync.selfScanVerificationIntervalInHours
        except:
            selfScanIntervalInHours = ('Not Applicable')
        uploadingFiles = info.proc.cloudsync.serviceStatus.uploadingFiles
        scanningFiles = info.proc.cloudsync.serviceStatus.scanningFiles
        try:
            selfVerificationscanningFiles = info.proc.cloudsync.serviceStatus.selfVerificationScanningFiles
        except:
            selfVerificationscanningFiles = ('Not Applicable')
        CurrentFirmware = info.status.device.runningFirmware
        try:
            MetaLogMaxSize = info.config.logging.metalog.maxFileSizeMB
        except:
            try:
                MetaLogMaxSize = info.config.logging.log2File.maxFileSizeMB
            except:
                MetaLogMaxSize = ('Not Applicable')
        try:
            MetaLogMaxFiles = info.config.logging.metalog.maxfiles
        except:
            try:
                MetaLogMaxFiles = info.config.logging.log2File.maxfiles
            except:
                MetaLogMaxFiles = ('Not Applicable')
        try:
            MetaLogs = filer.cli.run_command('dbg level')
            MetaLogs1 = MetaLogs[-28:-18]
        except:
            MetaLogs1 = ('Not Applicable')
        License = filer.licenses.get()
        # License = info.config.device.activeLicenseType
        IP1 = info.status.network.ports[0].ip.address
        DNS1 = info.status.network.ports[0].ip.DNSServer1
        DNS2 = info.status.network.ports[0].ip.DNSServer2
        try:
            storageThresholdPercentTrigger = info.config.cloudsync.cloudExtender.storageThresholdPercentTrigger
        except:
            storageThresholdPercentTrigger = ('Not Applicable')
        uptime = info.proc.time.uptime
        curr_cpu = info.proc.perfMonitor.current.cpu
        curr_mem = info.proc.perfMonitor.current.memUsage
        _total = info.proc.storage.summary.totalVolumeSpace
        _used = info.proc.storage.summary.usedVolumeSpace
        _free = info.proc.storage.summary.freeVolumeSpace
        volume = "Total: {} Used: {} Free: {}".format(_total,_used,_free)
        #dbg_level = filer.support.set_debug_level()
        #MetaLogs1 = dbg_level[-28:-18]
        Alerts = info.config.logging.alert
        TimeServer = info.config.time
        _mode = TimeServer.NTPMode
        _zone = TimeServer.TimeZone
        _servers = TimeServer.NTPServer
        time = "Mode: {} Zone: {} Servers: {}".format(_mode,_zone,_servers)

        def get_max_cpu():
            """Return the max CPU usage recorded in last few hours."""
            cpu_history = []
            for i in info.proc.perfMonitor.samples:
                cpu_history.append(i.cpu)
            return "{}%".format(max(cpu_history))

        def get_max_memory():
            """Return the max memory usage recorded in last few hours."""
            memory_history = []
            for i in info.proc.perfMonitor.samples:
                memory_history.append(i.memUsage)
            return "{}%".format(max(memory_history))


        with open(p_filename, mode='a', newline='', encoding="utf-8-sig") as gatewayList:
            gateway_writer = csv.writer(gatewayList, 
                    dialect='excel',
                    delimiter=',', 
                    quotechar='"', 
                    quoting=csv.QUOTE_MINIMAL)

            gateway_writer.writerow([
                    tenant,
                    filer.name,
                    sync_id,
                    selfScanIntervalInHours,
                    uploadingFiles,
                    scanningFiles,
                    selfVerificationscanningFiles,
                    MetaLogs1,
                    MetaLogMaxSize,
                    MetaLogMaxFiles,
                    CurrentFirmware,
                    License,
                    storageThresholdPercentTrigger,
                    volume,
                    IP1,
                    DNS1,
                    DNS2,
                    Alerts,
                    time,
                    uptime,
                    "CPU: {}% Mem: {}%".format(curr_cpu,curr_mem),
                    get_max_cpu(),
                    get_max_memory()
                    ])
    self.logout()

def write_header(p_filename):
    """Write CSV header to given filename parameter """
    try:
        with open(p_filename, mode='a', newline='', encoding="utf-8-sig") as gatewayList:
            gateway_writer = csv.writer(
                    gatewayList,
                    dialect='excel',
                    delimiter=',',
                    quotechar='"',
                    quoting=csv.QUOTE_MINIMAL
                    )
            gateway_writer.writerow(['Tenant',
                                     'Filer Name',
                                     'CloudSync Status',
                                     'selfScanIntervalInHours',
                                     'uploadingFiles',
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
                                     'DNS Server1',
                                     'DNS Server2',
                                     'Alerts',
                                     'TimeServer',
                                     'uptime',
                                     'Current Performance',
                                     'Max CPU',
                                     'Max Memory'
                                     ])
    except FileNotFoundError as error:
        logging.error(error)
        print("ERROR: Unable to open filename specified: {}".format(p_filename))
        sys.exit("Make sure you entered a valid file name and it exists")

def run_status(self,filename,all_tenants):
    """Log start/end of task and call main function."""
    logging.info('Starting status task')
    if os.path.exists(filename):
        logging.info('Appending to existing file.')
    else:
        logging.debug('File does not exist. Creating it.')
        write_header(filename)
    write_status(self,filename,all_tenants)
    logging.info('Finished status task.')

