import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from copyshares import copyshares

def print_help():
    print("\nCopy shares from source edge filer to another destination edge filer.\n")
    print("Usage: ./ctools.exe copy_shares [source_dev] [source_admin_usr] [source_admin_pass] [dest_dev] [dest_admin_usr] [dest_admin_pass] [verbose]\n")
    print("Parameters:")
    print("  source_dev: The IP address of the source edge filer")
    print("  source_admin_usr: The admin username of the source edge filer")
    print("  source_admin_pass: The admin password of the source edge filer")
    print("  dest_dev: The IP address of the destination edge filer")
    print("  dest_admin_usr: The admin username of the destination edge filer")
    print("  dest_admin_pass: The admin password of the destination edge filer")
    print("  verbose: Enable debug logging for this tool - Ex: True\n")
    print("Ex: ./ctools.exe copy_shares 192.168.80.200 admin password1! 192.168.80.201 admin newPassword2! False\n")

def copy_shares_cli(args):
    if len(args) < 3:
        print_help()

        sys.exit(0)
    elif len(args) < 9:
        print("\nError: Not enough arguments provided\n")
        print_help()

        sys.exit(0)
    else:
        if args[8] == "True":
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
                    copyshares(args[2], args[3], args[4], args[5], args[6], args[7])
                except Exception as e:
                    print(f"Failed to copy shares: {e}")
                finally:
                    ga.logout()



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        