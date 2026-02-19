"""Generate zones report for CTERA portal."""

import csv
import logging
import os
from datetime import datetime
from typing import Any, Optional

from cterasdk import CTERAException, Object
from cterasdk.core import query


def report_zones(
    session: Any,
    filename: str,
    tenant: Optional[str] = None,
    all_tenants: bool = True
) -> None:
    """
    Generate zones report.

    Args:
        session: Authenticated GlobalAdmin session
        filename: Output CSV filename or directory
        tenant: Optional specific tenant name
        all_tenants: If True, report on all tenants
    """
    logging.info("Starting zones report task.")

    # Handle output path
    output_path = os.path.expandvars(filename)
    if os.path.isdir(output_path):
        timestamp = datetime.now().strftime('Zones-%Y_%m_%d-%H_%M_%S')
        output_path = os.path.join(output_path, f"{timestamp}.csv")

    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Portal', 'Zone', 'Cloud Folders', 'Devices',
                'Total Size', 'Total Folders', 'Total Files'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            _gather_zones_report(session, writer, tenant, all_tenants)

        logging.info("Zones report saved to %s", output_path)
    except Exception as e:
        logging.error("Error generating zones report: %s", e)

    logging.info("Finished zones report task.")


def _gather_zones_report(
    session: Any,
    writer: csv.DictWriter,
    tenant: Optional[str],
    all_tenants: bool
) -> None:
    """Gather zone data and write to CSV."""
    try:
        session.portals.browse_global_admin()

        if tenant:
            tenants = [type('Tenant', (), {'name': tenant})()]
        else:
            tenants = session.portals.list_tenants()

        for portal in tenants:
            tenant_name = portal.name
            session.portals.browse(tenant_name)

            try:
                zones = session.cloudfs.zones.all()
            except Exception as e:
                logging.warning("Error getting zones for %s: %s", tenant_name, e)
                continue

            for zone in zones:
                zone_data = {
                    'Portal': tenant_name,
                    'Zone': zone.name,
                    'Cloud Folders': _get_cloud_folders(session, zone),
                    'Devices': _get_zone_devices(zone),
                    'Total Size': getattr(zone.zoneStatistics, 'totalSize', 'N/A'),
                    'Total Folders': getattr(zone.zoneStatistics, 'totalFolders', 'N/A'),
                    'Total Files': getattr(zone.zoneStatistics, 'totalFiles', 'N/A'),
                }

                writer.writerow(zone_data)
                logging.info("Wrote entry for zone %s on %s", zone.name, tenant_name)

    except CTERAException as e:
        logging.error("Error gathering zones report: %s", e)


def _get_cloud_folders(session: Any, zone: Any) -> str:
    """Get cloud folders for a zone."""
    if zone.name == 'All Folders':
        return zone.name

    try:
        param = _zone_query_param(zone.zoneId)
        response = session.api.execute('/', 'getZoneFolders', param)
        folders = [folder.name for folder in response.objects]
        return ','.join(folders)
    except Exception as e:
        logging.debug("Error getting cloud folders: %s", e)
        return 'N/A'


def _get_zone_devices(zone: Any) -> str:
    """Get devices for a zone."""
    try:
        devices = [device.name for device in zone.topDevices]
        return ','.join(devices)
    except Exception:
        return 'N/A'


def _zone_query_param(zone_id: Any) -> Object:
    """Create query parameter for zone folders."""
    param = Object()
    builder = query.QueryParamBuilder().include_classname().startFrom(0).countLimit(100).orFilter(True)
    param.query = builder.build()
    param._classname = "ZoneQuery"
    param.delta = Object()
    param.delta._classname = 'ZoneDelta'
    param.delta.policyDelta = []
    param.zoneId = zone_id
    return param
