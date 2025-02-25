import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from sharereport import share_report

def print_help():
    print("\nExport shares list for all edge filers (Detailed)\n")
    print("Usage: ./ctools.exe shares_report [address] [username] [password] [filename] [verbose] [tenant]\n")
    print("Parameters:")
    print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
    print("  username: The global admin username of the CTERA Portal")
    print("  password: The global admin password of the CTERA Portal")
    print("  filename: The name of the report file")
    print("  verbose: Enable debug logging for this tool - Ex: True")
    print("  tenant: The tenant to generate the report for (leave empty for all tenants)\n")
    print("Ex: ./ctools.exe shares_report 192.168.80.200 admin password1! shares_report.csv False portal1\n")

def shares_report_cli(args):
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
                    if len(args) == 8:
                        share_report(ga, args[5], tenant=args[7])
                    elif len(args) == 7:
                        share_report(ga, args[5])
                    else:
                        print("\nError: Wrong number of arguments provided\n")
                        print_help()
                except Exception as e:
                    print(f"Failed to generate shares report {e}")
                finally:
                    ga.logout()



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        