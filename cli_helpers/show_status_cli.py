import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from status import run_status

def show_status_cli(args):
    if len(args) < 3:
        print("\nGrab in depth stats about all devices in the CTERA Portal. Saved to same directory as this program is run from.\n")
        print("Usage: ./ctools.exe show_status [address] [username] [password] [file_name] [all_tenants] [verbose]\n")
        print("Parameters:")
        print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
        print("  username: The global admin username of the CTERA Portal")
        print("  password: The global admin password of the CTERA Portal")
        print("  file_name: The device to grab status on")
        print("  all_tenants: Grab status on all tenants - Ex: True")
        print("  verbose: Enable debug logging for this tool - Ex: True\n")
        print("Ex: ./ctools.exe show_status 192.168.80.200 admin password1! status_report.csv False\n")

        sys.exit(0)
    elif len(args) < 8:
        print("\nError: Not enough arguments provided\n")
        print("\nGrab in depth stats about all devices in the CTERA Portal. Saved to same directory as this program is run from.\n")
        print("Usage: ./ctools.exe show_status [address] [username] [password] [file_name] [all_tenants] [verbose]\n")
        print("Parameters:")
        print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
        print("  username: The global admin username of the CTERA Portal")
        print("  password: The global admin password of the CTERA Portal")
        print("  file_name: The device to grab status on")
        print("  verbose: Enable debug logging for this tool - Ex: True\n")
        print("Ex: ./ctools.exe show_status 192.168.80.200 admin password1! status_report.csv True False\n")

        sys.exit(0)

    else:
        if args[7] == "True":
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
            
            with GlobalAdmin(args[2]) as ga:
                ga.login(args[3], args[4])

                try:
                    run_status(ga, args[5], args[6]=="True")
                except Exception as e:
                    print(f"Failed to generate status report: {e}")
                finally:
                    ga.logout()
        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
    

    