import csv
import hashlib
import logging
import os
import re
import sys
from filer import get_filers, safe_cli_command, get_portal_name


def write_status(self, p_filename, all_tenants):
    """Save and write Filer status information to given filename."""
    get_list = ['config',
                'status',
                'proc/cloudsync',
                'proc/time/',
                'proc/storage/summary',
                'proc/perfMonitor']
    
    logging.info("Gathering status for all filers...")
    for filer in get_filers(self, all_tenants):
        logging.info(f"Gathering status for {filer.name}...")
        info = filer.api.get_multi('/', get_list)

        logging.info("Checking for tenant...")

        tenant = get_portal_name(filer)

        #tenant = filer.session().current_tenant()

        logging.info(f"Tenant: {tenant}")
        logging.info("Success")
        
        sync_id = info.proc.cloudsync.serviceStatus.id
        try:
            selfScanIntervalInHours = info.config.cloudsync.selfScanVerificationIntervalInHours
        except AttributeError:
            selfScanIntervalInHours = 'Not Applicable'
        uploadingFiles = info.proc.cloudsync.serviceStatus.uploadingFiles
        scanningFiles = info.proc.cloudsync.serviceStatus.scanningFiles
        try:
            selfVerificationscanningFiles = info.proc.cloudsync.serviceStatus.selfVerificationScanningFiles
        except AttributeError:
            selfVerificationscanningFiles = 'Not Applicable'
        CurrentFirmware = info.status.device.runningFirmware
        try:
            MetaLogMaxSize = info.config.logging.metalog.maxFileSizeMB
        except AttributeError:
            try:
                MetaLogMaxSize = info.config.logging.log2File.maxFileSizeMB
            except AttributeError:
                MetaLogMaxSize = 'Not Applicable'
        try:
            MetaLogMaxFiles = info.config.logging.metalog.maxfiles
        except AttributeError:
            try:
                MetaLogMaxFiles = info.config.logging.log2File.maxfiles
            except AttributeError:
                MetaLogMaxFiles = 'Not Applicable'
        AuditLogsStatus = safe_cli_command(filer, 'show /config/logging/files/mode')
        DeviceLocation = safe_cli_command(filer, 'show /config/device/location')
        AuditLogsPath = safe_cli_command(filer, 'show /config/logging/files/path')
        MetaLogs = safe_cli_command(filer, 'dbg level')
        # Extract substring from MetaLogs if it's a valid string
        if isinstance(MetaLogs, str) and len(MetaLogs) >= 28:
            MetaLogs1 = MetaLogs[-28:-18]
        else:
            MetaLogs1 = MetaLogs if MetaLogs != 'Not Applicable' else 'Not Applicable'
        ad_mapping = safe_cli_command(filer, 'show /config/fileservices/cifs/idMapping/map')
        try:
            License = filer.licenses.get()
            # Handle None or invalid response
            if License is None:
                raise ValueError("License returned None")
        except Exception:
            # Fallback for SDK 7.11+ where licenses.get() may fail
            try:
                License = filer.api.get('/config/device/activeLicenseType')
                if License is not None and hasattr(License, 'current'):
                    License = License.current
                elif License is None:
                    License = 'Not Applicable'
            except Exception:
                License = 'Not Applicable'
        # License = info.config.device.activeLicenseType
        SN = info.status.device.SerialNumber
        MAC = info.status.device.MacAddress
        IP1 = info.status.network.ports[0].ip.address
        DNS1 = info.status.network.ports[0].ip.DNSServer1
        DNS2 = info.status.network.ports[0].ip.DNSServer2
        try:
            storageThresholdPercentTrigger = info.config.cloudsync.cloudExtender.storageThresholdPercentTrigger
        except AttributeError:
            storageThresholdPercentTrigger = 'Not Applicable'
        uptime = info.proc.time.uptime
        try:
            curr_cpu = info.proc.perfMonitor.current.cpu
            curr_mem = info.proc.perfMonitor.current.memUsage
        except (AttributeError, TypeError):
            curr_cpu = 'N/A'
            curr_mem = 'N/A'
        _total = info.proc.storage.summary.totalVolumeSpace
        _used = info.proc.storage.summary.usedVolumeSpace
        _free = info.proc.storage.summary.freeVolumeSpace
        volume = (f"Total: {_total} Used: {_used} Free: {_free}")
        # dbg_level = filer.support.set_debug_level()
        # MetaLogs1 = dbg_level[-28:-18]
        Alerts = info.config.logging.alert
        TimeServer = info.config.time
        _mode = TimeServer.NTPMode
        _zone = TimeServer.TimeZone
        _servers = TimeServer.NTPServer
        time = (f"Mode: {_mode} Zone: {_zone} Servers: {_servers}")

        def get_max_cpu():
            """Return the max CPU usage recorded in last few hours."""
            try:
                samples = info.proc.perfMonitor.samples
                if samples is None:
                    return 'N/A'
                cpu_history = []
                for i in samples:
                    cpu_history.append(i.cpu)
                max_cpu = format(max(cpu_history))
                return f"{max_cpu}%"
            except (AttributeError, TypeError, ValueError):
                return 'N/A'

        def get_max_memory():
            """Return the max memory usage recorded in last few hours."""
            try:
                samples = info.proc.perfMonitor.samples
                if samples is None:
                    return 'N/A'
                memory_history = []
                for i in samples:
                    memory_history.append(i.memUsage)
                max_memory = format(max(memory_history))
                return f"{max_memory}%"
            except (AttributeError, TypeError, ValueError):
                return 'N/A'

        def get_ad_status(result=info.status.fileservices.cifs.joinStatus):
            """
            Parse domain join value and return the Domain Join Status as string.
            joinStatus: -1 = workgroup, 0 = OK, 2 = Failed
            """
            if result == 0:
                return 'Ok'
            if result == -1:
                return 'Workgroup'
            if result == 2:
                return 'Failed'
            return result
        
        def get_db_size():
            try:
                get_list = ['status', 'config']
                info = filer.api.get_multi('/', get_list)

                # Handle MacAddress being a list or string
                mac_addr = info.status.device.MacAddress
                if isinstance(mac_addr, list):
                    mac_addr = mac_addr[0] if mac_addr else ''
                mac_addr = str(mac_addr)

                firmware = str(info.status.device.runningFirmware)

                filer.telnet.enable(hashlib.sha1(
                    (mac_addr + '-' + firmware).encode('utf-8')).hexdigest()[:8])

                output = filer.shell.run_command('stat /var/volumes/*/.ctera/cloudSync/CloudSync.db')
                print(output)
                size_bytes = int(re.search(r'(?<=Size:\ )[0-9]*', output).group())
                size_gb = round(size_bytes/2**30,2)

                filer.telnet.disable()

                return size_gb
            except Exception as e:
                logging.debug(f"get_db_size failed: {e}")
                return 'N/A'

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
                    AuditLogsStatus,
                    DeviceLocation,
                    AuditLogsPath,
                    MetaLogMaxSize,
                    MetaLogMaxFiles,
                    CurrentFirmware,
                    License,
                    storageThresholdPercentTrigger,
                    volume,
                    SN,
                    MAC,
                    IP1,
                    DNS1,
                    DNS2,
                    get_ad_status(),
                    ad_mapping,
                    Alerts,
                    time,
                    uptime,
                    f"CPU: {curr_cpu}% Mem: {curr_mem}%",
                    get_max_cpu(),
                    get_max_memory(),
                    get_db_size()
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
                                     'AuditLogsStatus',
                                     'DeviceLocation',
                                     'AuditLogsPath',
                                     'MetaLogMaxSize',
                                     'MetaLogMaxFiles',
                                     'CurrentFirmware',
                                     'License',
                                     'EvictionPercentage',
                                     'CurrentVolumeStorage',
                                     'SN',
                                     'MAC',
                                     'IP Config',
                                     'DNS Server1',
                                     'DNS Server2',
                                     'AD Domain Status',
                                     'AD Mapping',
                                     'Alerts',
                                     'TimeServer',
                                     'uptime',
                                     'Current Performance',
                                     'Max CPU',
                                     'Max Memory',
                                     'DB Size'
                                     ])
    except FileNotFoundError as error:
        logging.error(error)
        logging.info("ERROR: Unable to open filename specified: %s", p_filename)
        sys.exit("Make sure you entered a valid file name and it exists")


def run_status(self, filename, all_tenants):
    """Log start/end of task and call main function."""
    logging.info('Starting status task')
    if os.path.exists(filename):
        logging.info('Appending to existing file.')
    else:
        logging.debug('File does not exist. Creating it.')
        write_header(filename)
    try:
        write_status(self, filename, all_tenants)
    except Exception as e:
        logging.warning("An error occurred: " + str(e))
    logging.info('Finished status task.')