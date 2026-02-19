"""Status reporting tool for CTERA filers."""

import csv
import hashlib
import logging
import os
import re
from typing import Any, Optional

from ..core.filer import get_filers, safe_cli_command, get_portal_name


def write_header(filename: str) -> None:
    """Write CSV header to the given filename."""
    headers = [
        'Tenant', 'Filer Name', 'CloudSync Status', 'selfScanIntervalInHours',
        'uploadingFiles', 'scanningFiles', 'selfVerificationscanningFiles',
        'MetaLogsSetting', 'AuditLogsStatus', 'DeviceLocation', 'AuditLogsPath',
        'MetaLogMaxSize', 'MetaLogMaxFiles', 'CurrentFirmware', 'License',
        'EvictionPercentage', 'CurrentVolumeStorage', 'SN', 'MAC', 'IP Config',
        'DNS Server1', 'DNS Server2', 'AD Domain Status', 'AD Mapping', 'Alerts',
        'TimeServer', 'uptime', 'Current Performance', 'Max CPU', 'Max Memory',
        'DB Size'
    ]

    try:
        with open(filename, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(headers)
    except FileNotFoundError as error:
        logging.error("Unable to open file: %s - %s", filename, error)
        raise


def get_safe_attr(obj: Any, *attrs: str, default: str = 'Not Applicable') -> Any:
    """Safely get nested attribute from object."""
    current = obj
    for attr in attrs:
        try:
            current = getattr(current, attr)
        except AttributeError:
            return default
    return current if current is not None else default


def get_ad_status(join_status: int) -> str:
    """Parse domain join status value."""
    status_map = {0: 'Ok', -1: 'Workgroup', 2: 'Failed'}
    return status_map.get(join_status, str(join_status))


def get_max_metric(samples: Any, metric: str) -> str:
    """Get maximum value of a metric from performance samples."""
    try:
        if samples is None:
            return 'N/A'
        values = [getattr(s, metric) for s in samples]
        return f"{max(values)}%"
    except (AttributeError, TypeError, ValueError):
        return 'N/A'


def get_db_size(filer: Any) -> str:
    """Get CloudSync database size."""
    try:
        info = filer.api.get_multi('/', ['status', 'config'])

        mac_addr = info.status.device.MacAddress
        if isinstance(mac_addr, list):
            mac_addr = mac_addr[0] if mac_addr else ''
        mac_addr = str(mac_addr)

        firmware = str(info.status.device.runningFirmware)

        filer.telnet.enable(
            hashlib.sha1((mac_addr + '-' + firmware).encode('utf-8')).hexdigest()[:8]
        )

        output = filer.shell.run_command('stat /var/volumes/*/.ctera/cloudSync/CloudSync.db')
        size_bytes = int(re.search(r'(?<=Size:\ )[0-9]*', output).group())
        size_gb = round(size_bytes / 2**30, 2)

        filer.telnet.disable()
        return str(size_gb)
    except Exception as e:
        logging.debug("get_db_size failed: %s", e)
        return 'N/A'


def write_filer_status(
    session: Any,
    filename: str,
    all_tenants: bool,
    tenant: Optional[str] = None
) -> None:
    """Write status information for all filers to CSV."""
    get_list = [
        'config', 'status', 'proc/cloudsync',
        'proc/time/', 'proc/storage/summary', 'proc/perfMonitor'
    ]

    logging.info("Gathering status for all filers...")
    filers = get_filers(session, all_tenants, tenant)

    if not filers:
        logging.warning("No filers found")
        return

    for filer in filers:
        logging.info("Gathering status for %s...", filer.name)

        try:
            info = filer.api.get_multi('/', get_list)
        except Exception as e:
            logging.warning("Failed to get info for %s: %s", filer.name, e)
            continue

        tenant = get_portal_name(filer)
        logging.info("Tenant: %s", tenant)

        # Extract all metrics with safe fallbacks
        sync_id = get_safe_attr(info, 'proc', 'cloudsync', 'serviceStatus', 'id')
        self_scan_interval = get_safe_attr(
            info, 'config', 'cloudsync', 'selfScanVerificationIntervalInHours'
        )
        uploading = get_safe_attr(info, 'proc', 'cloudsync', 'serviceStatus', 'uploadingFiles')
        scanning = get_safe_attr(info, 'proc', 'cloudsync', 'serviceStatus', 'scanningFiles')
        self_verification = get_safe_attr(
            info, 'proc', 'cloudsync', 'serviceStatus', 'selfVerificationScanningFiles'
        )
        firmware = get_safe_attr(info, 'status', 'device', 'runningFirmware')

        # MetaLog settings - try multiple paths
        metalog_size = get_safe_attr(info, 'config', 'logging', 'metalog', 'maxFileSizeMB')
        if metalog_size == 'Not Applicable':
            metalog_size = get_safe_attr(info, 'config', 'logging', 'log2File', 'maxFileSizeMB')

        metalog_files = get_safe_attr(info, 'config', 'logging', 'metalog', 'maxfiles')
        if metalog_files == 'Not Applicable':
            metalog_files = get_safe_attr(info, 'config', 'logging', 'log2File', 'maxfiles')

        # CLI commands
        audit_status = safe_cli_command(filer, 'show /config/logging/files/mode')
        device_location = safe_cli_command(filer, 'show /config/device/location')
        audit_path = safe_cli_command(filer, 'show /config/logging/files/path')
        metalogs = safe_cli_command(filer, 'dbg level')

        # Extract debug level
        if isinstance(metalogs, str) and len(metalogs) >= 28:
            metalogs_setting = metalogs[-28:-18]
        else:
            metalogs_setting = metalogs if metalogs != 'Not Applicable' else 'Not Applicable'

        ad_mapping = safe_cli_command(filer, 'show /config/fileservices/cifs/idMapping/map')

        # License
        try:
            license_info = filer.licenses.get()
            if license_info is None:
                raise ValueError("License returned None")
        except Exception:
            try:
                license_info = filer.api.get('/config/device/activeLicenseType')
                if license_info and hasattr(license_info, 'current'):
                    license_info = license_info.current
                elif license_info is None:
                    license_info = 'Not Applicable'
            except Exception:
                license_info = 'Not Applicable'

        # Device info
        serial = get_safe_attr(info, 'status', 'device', 'SerialNumber')
        mac = get_safe_attr(info, 'status', 'device', 'MacAddress')
        ip = get_safe_attr(info, 'status', 'network', 'ports', default=[{}])
        if isinstance(ip, list) and ip:
            ip = get_safe_attr(ip[0], 'ip', 'address', default='N/A')
            dns1 = get_safe_attr(info.status.network.ports[0], 'ip', 'DNSServer1', default='N/A')
            dns2 = get_safe_attr(info.status.network.ports[0], 'ip', 'DNSServer2', default='N/A')
        else:
            ip = dns1 = dns2 = 'N/A'

        eviction = get_safe_attr(
            info, 'config', 'cloudsync', 'cloudExtender', 'storageThresholdPercentTrigger'
        )
        uptime = get_safe_attr(info, 'proc', 'time', 'uptime')

        # Performance metrics
        try:
            curr_cpu = info.proc.perfMonitor.current.cpu
            curr_mem = info.proc.perfMonitor.current.memUsage
        except (AttributeError, TypeError):
            curr_cpu = curr_mem = 'N/A'

        # Storage
        try:
            total = info.proc.storage.summary.totalVolumeSpace
            used = info.proc.storage.summary.usedVolumeSpace
            free = info.proc.storage.summary.freeVolumeSpace
            volume = f"Total: {total} Used: {used} Free: {free}"
        except AttributeError:
            volume = 'N/A'

        # AD status
        ad_status = get_ad_status(
            get_safe_attr(info, 'status', 'fileservices', 'cifs', 'joinStatus', default=-1)
        )

        # Alerts and time
        alerts = get_safe_attr(info, 'config', 'logging', 'alert')
        time_config = get_safe_attr(info, 'config', 'time', default=None)
        if time_config:
            time_str = f"Mode: {getattr(time_config, 'NTPMode', 'N/A')} " \
                       f"Zone: {getattr(time_config, 'TimeZone', 'N/A')} " \
                       f"Servers: {getattr(time_config, 'NTPServer', 'N/A')}"
        else:
            time_str = 'N/A'

        # Performance history
        samples = get_safe_attr(info, 'proc', 'perfMonitor', 'samples', default=None)
        max_cpu = get_max_metric(samples, 'cpu')
        max_mem = get_max_metric(samples, 'memUsage')

        # DB size
        db_size = get_db_size(filer)

        # Write row
        with open(filename, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow([
                tenant, filer.name, sync_id, self_scan_interval, uploading,
                scanning, self_verification, metalogs_setting, audit_status,
                device_location, audit_path, metalog_size, metalog_files,
                firmware, license_info, eviction, volume, serial, mac, ip,
                dns1, dns2, ad_status, ad_mapping, alerts, time_str, uptime,
                f"CPU: {curr_cpu}% Mem: {curr_mem}%", max_cpu, max_mem, db_size
            ])

    session.logout()


def run_status(
    session: Any,
    filename: str,
    tenant: Optional[str] = None,
    all_tenants: bool = False
) -> None:
    """
    Run status report task.

    Args:
        session: Authenticated GlobalAdmin session
        filename: Output CSV filename
        tenant: Optional tenant name (leave blank for all tenants)
        all_tenants: If True, run on all tenants
    """
    logging.info('Starting status task')

    if os.path.exists(filename):
        logging.info('Appending to existing file.')
    else:
        logging.debug('File does not exist. Creating it.')
        write_header(filename)

    try:
        write_filer_status(session, filename, all_tenants, tenant)
    except Exception as e:
        logging.warning("An error occurred: %s", e)

    logging.info('Finished status task.')
