import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from add_mapping import add_mapping

def print_help():
    print("\nAdd domain to advanced mapping under the UID/GID mappings.\n")
    print("Usage: ./ctools.exe add_mapping [address] [username] [password] [domain] [verbose] [tenant] [device_name]\n")
    print("Parameters:")
    print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
    print("  username: The global admin username of the CTERA Portal")
    print("  password: The global admin password of the CTERA Portal")
    print("  domain: The domain to add to the advanced mapping")
    print("  verbose: Enable debug logging for this tool - Ex: True")
    print("  tenant: The tenant to add the domain to (leave empty for all devices on all tenants)")
    print("  device_name: The name of the device to add the domain to (leave empty for multiple devices)\n")
    print("Ex: ./ctools.exe add_mapping 192.168.80.200 admin password1! domain.ctera.me False portal1 edge1\n")

def add_mapping_cli(args):
    if len(args) < 3:
        print_help()

        sys.exit(0)
    elif len(args) < 7:
        print("\nError: Not enough arguments provided\n")
        print_help()

        sys.exit(0)
    else:
        if args[6] == "True":
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()

        settings.sessions.management.ssl = False

        try:
            with GlobalAdmin(args[2]) as ga:
                ga.login(args[3], args[4])

                ga.portals.browse_global_admin()

                ga.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')
                ga.logout()
            
            
            if len(args) == 9:
                add_mapping(args[2], args[3], args[4], args[5], tenant=args[7], device_name=args[8])
            elif len(args) == 8:
                add_mapping(args[2], args[3], args[4], args[5], tenant=args[7])
                



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        