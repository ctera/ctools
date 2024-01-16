import logging
from filer import get_filer

def share_audit(self, device_name):
    """
    Returns a list of shares with all users that have access to the shares.

    Args:
        self: The instance of the class.
        device_name (str): The name of the device.
    Returns:
        str: The result of the share audit.

    """
    tenant = self.users.session().user.tenant
    filer = get_filer(self, device_name, tenant)
    
    if filer is None:
        logging.error("Device not found")
        return None
    
    shares = filer.shares.get()

    result = ""

    for share in shares:
        share_name = share.name
        acl = share.acl
        result += "ACL Entries for share [" + str(share_name) + "]:" + "\n"
        for entry in acl:
            result += "\tAccess Entity Type: " + str(entry.principal2._classname) + "\n"
            if entry.principal2.displayName is None:
                result += "\tAccess Entity Name: Everyone" + "\n"
            else:
                result += "\tAccess Entity Name: " + str(entry.principal2.displayName) + "\n"
            result += "\tAccess Permissions: " + str(entry.permissions.allowedFileAccess) + "\n"
            result += "\n"

    logging.info(result)