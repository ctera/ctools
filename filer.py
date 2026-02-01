import logging
import re
from cterasdk import CTERAException


def safe_cli_command(filer, command):
    """
    Execute CLI command and ensure result is a string.
    Handles SDK 7.11+ changes where CLI output format may differ.

    :param filer: Filer object
    :param command: CLI command to execute
    :returns: String output or 'Not Applicable' on failure
    """
    try:
        result = filer.cli.run_command(command)

        # If result is already a string, return it
        if isinstance(result, str):
            return result

        # If result has a value or text attribute, extract it
        if hasattr(result, 'value'):
            return str(result.value)
        if hasattr(result, 'text'):
            return str(result.text)
        if hasattr(result, '__str__'):
            return str(result)

        # Last resort - convert to string
        return str(result) if result is not None else 'Not Applicable'
    except AttributeError:
        return 'Not Applicable'
    except Exception as e:
        logging.debug(f"CLI command failed: {command}, error: {e}")
        return 'Not Applicable'


def get_portal_name(filer):
    """
    Extract clean portal/tenant name from filer object.
    Handles SDK 7.11+ where filer.portal returns object reference paths.

    :param filer: Filer object
    :returns: Clean tenant/portal name string
    """
    try:
        portal = filer.portal

        # If it's already a clean name (no slashes), return it
        if isinstance(portal, str):
            # Handle format like "objs/9//TeamPortal/portal"
            # Extract the meaningful part (e.g., "TeamPortal")
            if '/' in portal:
                # Try to extract tenant name from path
                # Pattern: look for the part before "/portal" or between slashes
                match = re.search(r'/([^/]+)/portal$', portal)
                if match:
                    return match.group(1)

                # Alternative: get second-to-last segment
                parts = [p for p in portal.split('/') if p and p != 'objs' and p != 'portal']
                if parts:
                    # Filter out numeric-only parts
                    named_parts = [p for p in parts if not p.isdigit()]
                    if named_parts:
                        return named_parts[-1]

            return portal

        # If portal is an object, try common attributes
        if hasattr(portal, 'name'):
            return portal.name
        if hasattr(portal, 'tenant'):
            return portal.tenant

        return str(portal)
    except Exception as e:
        logging.debug(f"Failed to get portal name: {e}")
        return 'Unknown'


def get_current_tenant(portal_session):
    """Get current tenant from session, handling different SDK versions."""
    session = portal_session.users.session()

    # Try 7.11+ structure first
    if hasattr(session, 'tenant'):
        return session.tenant

    # Fall back to older structure
    if hasattr(session, 'user') and hasattr(session.user, 'tenant'):
        return session.user.tenant

    # Try other common patterns
    if hasattr(session, 'currentTenant'):
        return session.currentTenant

    # Last resort - log available attrs for debugging
    logging.warning(f"Could not determine tenant. Session attrs: {dir(session)}")
    return None


def get_filer(self, device=None, tenant=None):
    """Return Filer object if found"""
    try:
        filer = self.devices.device(device, tenant)
        return filer
    except CTERAException as error:
        logging.debug(error)
        logging.error("Device not found.")
        return None


def get_filers(self, all_tenants=False, tenant=None):
    try:
        """Return all connected Filers from Admin Portal or Tenant"""
        connected_filers = []
        if all_tenants is True:
            self.portals.browse_global_admin()

            #tenant = self.users.session().current_tenant()

            tenant = get_current_tenant(self)
            logging.info("Getting all Filers since tenant is %s", tenant)
            for tenant in self.portals.tenants():
                self.portals.browse(tenant.name)
                all_filers = self.devices.filers(include=[
                        'deviceConnectionStatus.connected',
                        'deviceReportedStatus.config.hostname'])
                connected_filers.extend([filer for filer in all_filers if filer.deviceConnectionStatus.connected])
        elif tenant is not None:
            logging.info("Getting Filers connected to %s", tenant)
            self.portals.browse(tenant)
            tenant_filers = self.devices.filers(include=[
                        'deviceConnectionStatus.connected',
                        'deviceReportedStatus.config.hostname'])
            connected_filers.extend([filer for filer in tenant_filers if filer.deviceConnectionStatus.connected])
        else:
            current_tenant = get_current_tenant(self)
            logging.info("Getting Filers connected to %s", current_tenant)
            tenant_filers = self.devices.filers(include=[
                        'deviceConnectionStatus.connected',
                        'deviceReportedStatus.config.hostname'])
            connected_filers.extend([filer for filer in tenant_filers if filer.deviceConnectionStatus.connected])
        return connected_filers
    except CTERAException as error:
        logging.debug(error)
        logging.error("Error getting Filers.")
        return None
