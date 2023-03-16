# CTools

## Description

A toolbox of tasks to check and manage CTERA Edge Filers via CLI or GUI.

## Prerequisites

### Required Settings

1. Ensure necessary Remote Administration settings are enabled on the portal:

    Access the Global Administration view > Navigate to Settings > Control Panel > User Roles > Read/Write Administrator -> Ensure "Allow Single Sign On to Devices" is checked

[documentation](https://kb.ctera.com/v1/docs/en/portaladmin3-02-7?highlight=user%20roles%20portal)

## Please review this document to learn more about using each tool

## Development Requirements

- [CTERA Environment](https://www.ctera.com/)
- [CTERA SDK for Python](https://github.com/ctera/ctera-python-sdk)
- [Python](https://www.python.org/downloads/)
- [git](https://git-scm.com/)
- [Gooey](https://github.com/chriskiehl/Gooey)

## Setup

### Linux

General instructions. Actual commands will vary by distro and version.
```
git clone https://github.com/ctera/ctools.git
python -m pip install -r ctools/requirements.txt
```

### Windows

For a machine without Python and git already installed, you can use these steps to simplify setup.
Here we use [Chocolatey](https://chocolatey.org/) as a commmand line package manager for Windows.
Run PowerShell as an Administrator to setup. Close and re-open PowerShell
after to refresh the environment and enable tab completion of commands.

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
choco install python --yes
choco install git --yes
# Close and re-open your shell
git clone https://github.com/ctera/ctools.git
python -m pip install --upgrade pip
python -m pip install -r .\ctools\requirements.txt
cd ctools
```

## Run

```
# To launch the GUI, invoke ctools.py
python ctools.py
# To use on CLI, pass valid arguments to ctools.py
python ctools.py -h
```

## Instructions

### Task Usage

If desired, it's possible to add optional arguments to pre-populate fields for each task.
Each task has its own positional arguments, usually login info then any arguments required to complete the task.

**Use a Portal Global Administrator account to login.**
There is currently no support for tenant admins or direct logins to Filers. All requests are sent through the Portal to connected Filers.

Specify the task and run to see that task's required and optional arguments.
Any task can be run with `-h` or `--help` to see usage instructions.
Any task can be run with the optional flag `-v` or `--verbose` to enable debug logging.

```
Manage CTERA Edge Filers

positional arguments:
  {get_status,run_cmd,enable_telnet,enable_ssh,disable_ssh,suspend_sync,unsuspend_sync}
                        Task choices.
    get_status          Record current status of all connected Filers. Use --all to browse all Tenants
    run_cmd             Run a comand on each connected Filer.
    enable_telnet       Enable SSH on a Filer.
    enable_ssh          Enable SSH on a Filer.
    disable_ssh         Disable SSH on a Filer.
    suspend_sync        Suspend sync on a given Filer
    unsuspend_sync      Unsuspend sync on a given Filer
```

#### get_status

Record current status of connected Filers to a specified CSV output file.
Provide a portal URL, e.g. portal.ctera.me, to scan all connected Filers to that tenant and write various bits of
information to a specified CSV file.
If an IP address is provided, the Default Tenant Portal will be used.
Or you can use/check the `-a, --all` flag to scan all connected Filers across all Tenant Portals.
If the output filename already exists, the results will be appended to the existing file.

```
positional arguments:
  address        Portal IP, hostname, or FQDN
  username       Username for portal administrator
  password       Password. Enter ? to prompt in CLI
  filename       output filename

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Add verbose logging
  -a, --all      All Filers, All Tenants
```
#### run_cmd

Run a "hidden CLI command", i.e. execute a RESTful API request to each connected Filer.

```
usage: ctools.py run_cmd [-h] [-v] [-i] [-a] [-d DEVICE] address username password command

positional arguments:
  address               Portal IP, hostname, or FQDN
  username              Username for portal administrator
  password              Password. Enter ? to prompt in CLI
  command               Run a comand on one or more connected Filers.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Add verbose logging
  -i, --ignore_cert     Ignore cert warnings
  -a, --all             Run a command globally, on all Filers, on all Tenants.
  -d DEVICE, --device DEVICE
                        Device name to run command against. Overrides --all flag.
```
#### enable_telnet

Enable the telnet service on a given Filer. If no unlock code is provided, return the required MAC address
and firmware version to get an unlock code from CTERA Support.

```
usage: ctools.py enable_telnet [-h] [-v] [-i] [-c CODE] address username password device_name tenant_name

positional arguments:
  address               Portal IP, hostname, or FQDN
  username              Username for portal administrator
  password              Password. Enter ? to prompt in CLI
  device_name           Device Name
  tenant_name           Tenant Name

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Add verbose logging
  -i, --ignore_cert     Ignore cert warnings
  -c CODE, --code CODE  Required code to enable telnet
```

#### enable_ssh

Enable the ssh service on a given Filer and add the public key to the authorized_keys of the Filer.
If no public key is provided, a new keypair will generated and saved to the Downloads folder.

```
usage: ctools.py enable_ssh [-h] [-v] [-i] [-p PUBKEY] address username password device_name tenant_name

positional arguments:
  address               Portal IP, hostname, or FQDN
  username              Username for portal administrator
  password              Password. Enter ? to prompt in CLI
  device_name           Device Name
  tenant_name           Tenant Name

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Add verbose logging
  -i, --ignore_cert     Ignore cert warnings
  -p PUBKEY, --pubkey PUBKEY
                        Provide an SSH Public Key
```

#### suspend_sync / unsuspend_sync
Suspend or Unususpend Cloud Drive syncing on a Filer.

```
usage: ctools.py suspend_sync [-h] [-v] [-i] address username password device_name tenant_name

positional arguments:
  address            Portal IP, hostname, or FQDN
  username           Username for portal administrator
  password           Password. Enter ? to prompt in CLI
  device_name        Device Name
  tenant_name        Tenant Name

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Add verbose logging
  -i, --ignore_cert  Ignore cert warnings
```

#### reset_password
Reset a local user account password on a Filer.
```
usage: ctools.py reset_password [-h] [-v] [-i] address username password device_name tenant_name user_name filer_password

positional arguments:
  address            Portal IP, hostname, or FQDN
  username           Username for portal administrator
  password           Password. Enter ? to prompt in CLI
  device_name        Device Name
  tenant_name        Tenant Name
  user_name          User Name
  filer_password     New Filer Password. Enter ? to prompt in CLI

optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Add verbose logging
  -i, --ignore_cert  Ignore cert warnings
```

#### cloud_folders
Create folder_groups and cloud folders using a pre-populated CSV file - download template [here](./templates/cloud_folders.csv)
- Replace content in file above with desired folder_group and cloud_folder names

```
usage: ctools.py cloud_folders [-h] [-v] [-i] address username password /path/to/cloud_folders.csv

positional arguments:
  address            Portal IP, hostname, or FQDN
  username           Username for portal administrator
  password           Password. Enter ? to prompt in CLI
  cloud_folders.csv  Configured Template File
optional arguments:
  -h, --help         show this help message and exit
  -v, --verbose      Add verbose logging
  -i, --ignore_cert  Ignore cert warnings
```

## Examples

### GUI
To launch the GUI, simply invoke python and specify our main module, ctools.py, without specifying any flags.

```
PS C:\Users\ctera\git\ctools> python ctools.py
```
![ctools GUI screenshot](./images/screenshot-ctools-gui.png)

### CLI

Run ctools.py with any flags to run it from a CLI.

```
(ctools) PS C:\Users\ctera\git\ctools> python ctools.py run_cmd portal.ctera.me admin ? 'show /config/logging/log2File' --all --ignore_cert
2021-10-06 02:09:08,677 [INFO] Starting ctools
Password:
2021-10-06 02:09:11,683 [INFO] Logging into portal.ctera.me
2021-10-06 02:09:12,014 [INFO] User logged in. {'host': 'portal.ctera.me', 'user': 'admin'}
2021-10-06 02:09:12,202 [WARNING] Allow Single Sign On to Devices is not enabled.
Some tasks may fail or output may be incomplete
2021-10-06 02:09:12,203 [INFO] Starting run_cmd task
2021-10-06 02:09:12,272 [INFO] Getting all Filers since tenant is Administration
2021-10-06 02:09:12,986 [INFO] Running command on: vgw-1b6c
2021-10-06 02:09:12,988 [INFO] Executing CLI command. {'cli_command': 'show /config/logging/log2File'}
2021-10-06 02:09:13,047 [INFO] CLI command executed. {'cli_command': 'show /config/logging/log2File'}
2021-10-06 02:09:13,048 [INFO] No such attribute log2File
2021-10-06 02:09:13,049 [INFO] Finished command on: vgw-1b6c
2021-10-06 02:09:13,049 [INFO] Running command on: svtvgw
2021-10-06 02:09:13,050 [INFO] Executing CLI command. {'cli_command': 'show /config/logging/log2File'}
2021-10-06 02:09:13,113 [INFO] CLI command executed. {'cli_command': 'show /config/logging/log2File'}
2021-10-06 02:09:13,114 [INFO] {
   type: log2FileSetting
   maxFileSizeMB: "100"
   maxfiles: "70"
}
2021-10-06 02:09:13,116 [INFO] Finished command on: svtvgw
2021-10-06 02:09:13,116 [INFO] Running command on: team-vGateway1
2021-10-06 02:09:13,117 [INFO] Executing CLI command. {'cli_command': 'show /config/logging/log2File'}
2021-10-06 02:09:13,178 [INFO] CLI command executed. {'cli_command': 'show /config/logging/log2File'}
2021-10-06 02:09:13,179 [INFO] No such attribute log2File
2021-10-06 02:09:13,180 [INFO] Finished command on: team-vGateway1
2021-10-06 02:09:13,181 [INFO] Finished run_cmd task on all Tenants.
2021-10-06 02:09:13,243 [INFO] User logged out. {'host': 'portal.ctera.me', 'user': 'admin'}
2021-10-06 02:09:13,244 [INFO] Exiting ctools

```

