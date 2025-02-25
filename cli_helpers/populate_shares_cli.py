import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from populate import run_populate

def print_help():
    print("\nPopulate edge filer shares for every cloud folder in its portal (excluding My Files).\n")
    print("Usage: ./ctools.exe report_zones [address] [username] [password] [device_name] [verbose] [domain_name]\n")
    print("Parameters:")
    print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
    print("  username: The global admin username of the CTERA Portal")
    print("  password: The global admin password of the CTERA Portal")
    print("  device_name: The name of the edge filer to populate shares on")
    print("  verbose: Enable debug logging for this tool - Ex: True")
    print("  domain_name: The domain name of the edge filer. This is only needed if domain users are cloud folder owners\n")
    print("Ex: ./ctools.exe populate_shares 192.168.80.200 admin password1! edge1 True False domain.ctera.me\n")

def populate_shares_cli(args):
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
            

            if len(args) == 8:
                run_populate(args[2], args[3], args[4], args[5], args[7])
            elif len(args) == 7:
                run_populate(args[2], args[3], args[4], args[5])
            else:
                print("\nError: Wrong number of arguments provided\n")
                print_help()

                sys.exit(0)
                



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        