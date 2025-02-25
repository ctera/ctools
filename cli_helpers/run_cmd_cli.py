import sys, logging

from log_setter import set_logging

from cterasdk import settings, GlobalAdmin

from run_cmd import run_cmd


def run_cmd_cli(args):
    if len(args) < 3:
        print("\nRun a CLI command on one device, all devices on a tenant, or all devices on all tenants\n")
        print("Usage: ./ctools.exe run_cmd [address] [username] [password] [command] [verbose] [tenant] [device_name]\n")
        print("Parameters:")
        print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
        print("  username: The global admin username of the CTERA Portal")
        print("  password: The global admin password of the CTERA Portal")
        print("  command: The CLI command to run on the devices - Ex: \"show status\"")
        print("  verbose: Enable debug logging for this tool - Ex: True")
        print("  tenant: The tenant to run the command on - Ex: tenant1")
        print("  device_name: The device to run the command on - Ex: device1\n")
        print("Ex: ./ctools.exe run_cmd 192.168.80.200 admin password1! \"dbg le\" False tenant1 device1\n")

        sys.exit(0)
    
    else:
        if args[6] == "True":
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()
        
        settings.sessions.management.ssl = False
        
        with GlobalAdmin(args[2]) as ga:
            try:
                ga.login(args[3], args[4])

                ga.portals.browse_global_admin()

                ga.api.put('/rolesSettings/readWriteAdminSettings/allowSSO', 'true')
                ga.logout()

                ga = GlobalAdmin(args[2])
                ga.login(args[3], args[4])

                if len(args) < 7:
                    print("\nError: Not enough arguments provided\n\n")
                    print("\nRun a CLI command on one device, all devices on a tenant, or all devices on all tenants\n")
                    print("Usage: ./ctools.exe run_cmd [address] [username] [password] [command] [verbose] [tenant] [device_name]\n")
                    print("Parameters:")
                    print("  address: The IP address of the CTERA Portal - Ex: 192.168.80.200")
                    print("  username: The global admin username of the CTERA Portal")
                    print("  password: The global admin password of the CTERA Portal")
                    print("  command: The CLI command to run on the devices - Ex: \"show status\"")
                    print("  verbose: Print the output of the command - Ex: True\n")
                    print("  tenant: The tenant to run the command on - Ex: tenant1")
                    print("  device_name: The device to run the command on - Ex: device1")
                    print("Ex: ./ctools.exe run_cmd 192.168.80.200 admin password1! \"dbg le\" tenant1 device1 False True\n")

                    sys.exit(0)
                elif len(args) < 8:
                    run_cmd(ga, args[5], all_tenants=True)
                elif len(args) < 9:
                    run_cmd(ga, args[5], tenant_name=args[7])
                else:
                    run_cmd(ga, args[5], tenant_name=args[7], all_tenants=False, device_name=args[8])

        
            except Exception as e:
                print(e)
            finally:
                ga.logout()
            
        sys.exit(0)