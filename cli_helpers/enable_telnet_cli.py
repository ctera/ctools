import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from unlock import enable_telnet

def print_help():
    print("\nEnable Telnet on an Edge Filer\n")
    print("Usage: ./ctools.exe enable_telnet [address] [username] [password] [device_name] [tenant] [verbose] [code]\n")
    print("Parameters:")
    print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
    print("  username: The global admin username of the CTERA Portal")
    print("  password: The global admin password of the CTERA Portal")
    print("  device_name: The device to enable telnet on")
    print("  tenant: The tenant to run the command on")
    print("  verbose: Enable debug logging for this tool - Ex: True")
    print("  code: The unlock code for the device\n")
    print("Ex: ./ctools.exe enable_telnet 192.168.80.200 admin password1! device1 tenant1 False\n")

def enable_telnet_cli(args):
    if len(args) < 3:
        print_help()

        sys.exit(0)
    elif len(args) < 8:
        print("\nError: Not enough arguments provided\n")
        print_help()

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
                    if len(args) < 9:
                        enable_telnet(ga, args[5], args[6])
                    elif len(args) == 9:
                        enable_telnet(ga, args[5], args[6], args[8])
                    else:
                        print("\nError: Too many arguments provided\n")
                        print_help()
                except Exception as e:
                    print(f"Failed to enable telnet: {e}")
                finally:
                    ga.logout()



        except Exception as e:
            print(f"An error occurred: {e}")

    sys.exit(0)
        