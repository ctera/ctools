from cterasdk import *
import urllib3
urllib3.disable_warnings()
import logging
from filer import get_filer, get_filers

def add_user_to_admin(self, add_or_remove, user, group, tenant_name=None, all_devices=False, device_name=None):
    try:
        config.http['SSL'] = 'Trust'

        logging.info("Tenant name: " + str(tenant_name) + " Device name: " + str(device_name) + " All devices: " + str(all_devices) + " User: " + str(user) + " Group: " + str(group) + " Add or remove: " + str(add_or_remove))

        if add_or_remove == "Add":
            if all_devices:
                filers = get_filers(self, all_tenants=True)

                if filers is None:
                    logging.error("No devices found")
                    return None
                
                for filer in filers:
                    if user is not None:
                        domain_user = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DU, user)
                        print("Domain user: ", domain_user)
                        filer.groups.add_members('Administrators', [domain_user])
                        logging.info("User \"" + str(domain_user) + "\" added to Administrators group on " + str(filer.name))
                    elif group is not None:
                        domain_group = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DG, group)
                        filer.groups.add_members('Administrators', [domain_group])
                        logging.info("Group \"" + str(domain_group) + "\" added to Administrators group on " + str(filer.name))
                    else:
                        logging.error("No user or group specified")
                        return None
            # one device one tenant
            elif not all_devices and device_name is not None:
                filer = get_filer(self, device_name, tenant_name)

                if filer is None:
                    logging.error("Device not found")
                    return None
                
                if user is not None:
                    domain_user = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DU, user)
                    print("Domain user: ", domain_user)
                    filer.groups.add_members('Administrators', [domain_user])
                    logging.info("User \"" + str(domain_user) + "\" added to Administrators group on " + str(filer.name))
                elif group is not None:
                    domain_group = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DG, group)
                    filer.groups.add_members('Administrators', [domain_group])
                    logging.info("Group \"" + str(domain_group) + "\" added to Administrators group on " + str(filer.name))
                else:
                    logging.error("No user or group specified")
                    return None
            # all devices one tenant
            elif not all_devices and device_name is None and tenant_name is not None:
                filers = get_filers(self, False, tenant=tenant_name)

                if filers is None:
                    logging.error("No devices found")
                    return None
                
                for filer in filers:
                    if user is not None:
                        domain_user = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DU, user)
                        print("Domain user: ", domain_user)
                        filer.groups.add_members('Administrators', [domain_user])
                        logging.info("User \"" + str(domain_user) + "\" added to Administrators group on " + str(filer.name))
                    elif group is not None:
                        domain_group = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DG, group)
                        filer.groups.add_members('Administrators', [domain_group])
                        logging.info("Group \"" + str(domain_group) + "\" added to Administrators group on " + str(filer.name))
                    else:
                        logging.error("No user or group specified")
                        return None

            else:
                logging.error("No device name or tenant name and Perform on all devices is not checked")
                return None
        elif add_or_remove == "Remove":
            #all devices all tenants
            if all_devices:
                filers = get_filers(self, all_tenants=True)

                if filers is None:
                    logging.error("No devices found")
                    return None
                
                for filer in filers:
                    if user is not None:
                        domain_user = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DU, user)
                        print("Domain user: ", domain_user)
                        filer.groups.remove_members('Administrators', [domain_user])
                        logging.info("User \"" + str(domain_user) + "\" removed from Administrators group on " + str(filer.name))
                    elif group is not None:
                        domain_group = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DG, group)
                        filer.groups.remove_members('Administrators', [domain_group])
                        logging.info("Group \"" + str(domain_group) + "\" removed from Administrators group on " + str(filer.name))
                    else:
                        logging.error("No user or group specified")
                        return None

                    logging.info("User removed to Administrators group on %s", filer.name)

            elif not all_devices and device_name is not None:
                filer = get_filer(self, device_name, tenant_name)

                if filer is None:
                    logging.error("Device not found")
                    return None
                
                if user is not None:
                    domain_user = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DU, user)
                    print("Domain user: ", domain_user)
                    filer.groups.remove_members('Administrators', [domain_user])
                    logging.info("User \"" + str(domain_user) + "\" removed from Administrators group on " + str(filer.name))
                elif group is not None:
                    domain_group = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DG, group)
                    filer.groups.remove_members('Administrators', [domain_group])
                    logging.info("Group \"" + str(domain_group) + "\" removed from Administrators group on " + str(filer.name))
                else:
                    logging.error("No user or group specified")
                    return None
            elif not all_devices and device_name is None and tenant_name is not None:
                filers = get_filers(self, False, tenant_name)

                if filers is None:
                    logging.error("No devices found")
                    return None
                
                for filer in filers:
                    if user is not None:
                        domain_user = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DU, user)
                        print("Domain user: ", domain_user)
                        filer.groups.remove_members('Administrators', [domain_user])
                        logging.info("User \"" + str(domain_user) + "\" removed from Administrators group on " + str(filer.name))
                    elif group is not None:
                        domain_group = gateway_types.UserGroupEntry(gateway_enum.PrincipalType.DG, group)
                        filer.groups.remove_members('Administrators', [domain_group])
                        logging.info("Group \"" + str(domain_group) + "\" removed from Administrators group on " + str(filer.name))
                    else:
                        logging.error("No user or group specified")
                        return None

            else:
                logging.error("No device name and Perform on all devices is not checked")
                return None
        else:
            logging.error("No add or remove specified")
            return None
        
    except CTERAException as error:
         logging.error(error)