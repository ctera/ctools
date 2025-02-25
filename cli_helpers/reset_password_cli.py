import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from reset_password import reset_filer_password

def print_help():
    print("\nReset the password of a local user on a device\n")
    print("Usage: ./ctools.exe reset_password [address] [username] [password] [device_name] [tenant] [user_username] [new_pass] [all_devices] [verbose]\n")
    print("Parameters:")
    print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
    print("  username: The global admin username of the CTERA Portal")
    print("  password: The global admin password of the CTERA Portal")
    print("  device_name: The device the user to reset the password for is on")
    print("  tenant: The tenant the device lies on")
    print("  user_username: The username of the local user to reset the password for")
    print("  new_pass: The new password for the local user")
    print("  all_devices: Whether to reset the password on all devices in the tenant - Ex: True\n")
    print("  verbose: Enable debug logging for this tool - Ex: True\n")
    print("Ex: ./ctools.exe reset_password 192.168.80.200 admin password1! device1 tenant1 user1 newPassword2! False False\n")

def reset_password_cli(args):
    if len(args) < 3:
        print_help()

        sys.exit(0)
    elif len(args) < 11:
        print("\nError: Not enough arguments provided\n")
        print_help()

        sys.exit(0)
    else:
        if args[10] == "True":
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
                    reset_filer_password(ga, args[5], args[6], args[7], args[8], args[9])
                except Exception as e:
                    print(f"Failed to reset password: {e}")
                finally:
                    ga.logout()



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        