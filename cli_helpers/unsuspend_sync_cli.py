import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from unsuspend_sync import unsuspend_filer_sync

def unsuspend_sync_cli(args):
    print(args)
    if len(args) < 3:
        print("\nUnsuspend sync on a device\n")
        print("Usage: ./ctools.exe unsuspend_sync [address] [username] [password] [device_name] [tenant] [verbose]\n")
        print("Parameters:")
        print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
        print("  username: The global admin username of the CTERA Portal")
        print("  password: The global admin password of the CTERA Portal")
        print("  device_name: The device to unsuspend sync on")
        print("  tenant: The tenant to run the command on\n")
        print("Ex: ./ctools.exe unsuspend_sync 192.168.80.200 admin password1! device1 tenant1 False\n")

        sys.exit(0)
    elif len(args) < 8:
        print("\nError: Not enough arguments provided\n")
        print("\nUnsuspend sync on a device\n")
        print("Usage: ./ctools.exe unsuspend_sync [address] [username] [password] [device_name] [tenant] [verbose]\n")
        print("Parameters:")
        print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
        print("  username: The global admin username of the CTERA Portal")
        print("  password: The global admin password of the CTERA Portal")
        print("  device_name: The device to unsuspend sync on")
        print("  tenant: The tenant to run the command on\n")
        print("Ex: ./ctools.exe unsuspend_sync 192.168.80.200 admin password1! device1 tenant1 False\n")

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
                    unsuspend_filer_sync(ga, args[5], args[6])
                except Exception as e:
                    print(f"Failed to unsuspend sync: {e}")
                finally:
                    ga.logout()



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        