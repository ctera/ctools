import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from report_zones import create

def print_help():
    print("\nCreate zones report for details such as Devices, Total Size, Total Folders, and Total Files in the desired output location.\n")
    print("Usage: ./ctools.exe report_zones [address] [username] [password] [output_dir] [verbose]\n")
    print("Parameters:")
    print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
    print("  username: The global admin username of the CTERA Portal")
    print("  password: The global admin password of the CTERA Portal")
    print("  output_dir: The directory where the report will be saved")
    print("  verbose: Enable debug logging for this tool - Ex: True\n")
    print("Ex: ./ctools.exe reset_password 192.168.80.200 admin password1! C:\\Users\\user\\Desktop\\zones_report.csv\n")

def report_zones_cli(args):
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
            
            with GlobalAdmin(args[2]) as ga:
                ga.login(args[3], args[4])

                try:
                    create(ga, args[2], args[3], args[4], args[5])
                except Exception as e:
                    print(f"Failed to generate zones report {e}")
                finally:
                    ga.logout()



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        