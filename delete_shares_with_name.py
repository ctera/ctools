def get_filers(global_admin):
    """Return all connected Filers from each Tenant"""
    connected_filers = []
    for tenant in global_admin.portals.tenants():
        global_admin.portals.browse(tenant.name)
        all_filers = global_admin.devices.filers(include=[
                'deviceConnectionStatus.connected',
                'deviceReportedStatus.config.hostname'])
        for filer in all_filers:
            if filer.deviceConnectionStatus.connected:
                connected_filers.append(filer)
    return connected_filers