from cterasdk import *
from getpass import getpass
import logging, sys
import csv

def login():
    try:
        address = input("Portal (IP, Hostname or FQDN): ")
        username = input("Admin Username: ")
        password = getpass("Admin Password: ")
    except CTERAException as error:
        logging.error(error)
    
    try:
        logging.info("Logging into " + address)
        global_admin = GlobalAdmin(address)
        global_admin.login(username, password)
        logging.info("Successfully logged in to " + address)
        global_admin.portals.browse_global_admin()
        return global_admin
    except CTERAException as error:
        logging.warning(error)
        sys.exit("There was a problem logging in. Please try again.")


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

if __name__ == "__main__":
    try:
        global_admin = login()
        filers = get_filers(global_admin)

        word_to_delete = input('Please enter the word to delete shares:')

        # Create/open the CSV file and add headers if it's new
        with open('deleted_shares.csv', 'a+', newline='') as f:
            f.seek(0)  # Go to the start of the file to check if it's empty
            writer = csv.writer(f)
            if f.read() == '':  # If file is empty, write headers
                writer.writerow(['FilerName', 'ShareName', 'Status'])
        
        for filer in filers:
            shares_to_delete = []
            shares = filer.get('/config/fileservices/share')
            for share in shares:
                print(f"Share name: '{share.name}'")  # Add this line
                if isinstance(share.name, str) and word_to_delete in share.name:
                    shares_to_delete.append(share)

            if shares_to_delete:
                print(f"The following shares from filer {filer.name} will be deleted:")
                for share in shares_to_delete:
                    print(f"Share {share.name}")

                prompt = input('Do you want to proceed? Type Y to confirm:')
                if prompt.lower() == 'y':
                    with open('deleted_shares.csv', 'a', newline='') as f:
                        writer = csv.writer(f)
                        for share in shares_to_delete:
                            try:
                                filer.shares.delete(share.name)
                                print(f'Share {share.name} deleted')
                                writer.writerow([filer.name, share.name, 'Deleted'])
                            except CTERAException as error:
                                print(f"Failed to delete Share: {share.name} from Filer: {filer.name}")
                                writer.writerow([filer.name, share.name, 'NotDeleted'])

    except CTERAException as error:
        print(error)