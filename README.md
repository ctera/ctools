# ctools

## Purpose

A toolbox of sorts to check and manage CTERA Edge Filers and more coming soon.

## Development Requirements

- [Python 3.8.x](https://www.python.org/downloads/release/python-3810/)
- [git](https://git-scm.com/)
- [CTERA SDK for Python](https://github.com/ctera/ctera-python-sdk)
- [Gooey](https://github.com/chriskiehl/Gooey)
- [CTERA Environment](https://www.ctera.com/)

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
# To launch the GUI
python ctools.py
# To use on CLI
python ctools.py -h
```

## Examples

### GUI
To launch the GUI, simply invoke python and specify our main module, ctools.py, without specifying any flags.

```
PS C:\Users\ctera\git\ctools> python ctools.py
```
![ctools GUI screenshot](./images/screenshot-ctools-gui.png)

### CLI

Running the CLI from PowerShell
The (ctools) in the prompt is PyEnv which is not required but helpful.
Run ctools.py with any flags to run it from CLI
The first, required, positional argument is the Task choice.
Specify the task and run to see that task's required and optional arguments.
Any task can be run with `-h` or `--help` to see usage instructions.
Any task can be run with the optional flag `-v` or `--verbose` to enable debug logging.

```
(ctools) PS C:\Users\ctera\git\ctools> python ctools.py -h
usage: ctools.py [-h] {get_status,run_cmd,enable_telnet,enable_ssh,disable_ssh,suspend_sync,unsuspend_sync} ...

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

(ctools) PS C:\Users\ctera\git\ctools> python ctools.py get_status
usage: ctools.py get_status [-h] [-v] [-a] address username password filename
ctools.py get_status: error: the following arguments are required: address, username, password, filename

optional arguments:
  -h, --help            show this help message and exit

(ctools) PS C:\Users\ctera\git\ctools> python ctools.py get_status -h
usage: ctools.py get_status [-h] [-v] [-a] address username password filename

positional arguments:
  address        Portal IP, hostname, or FQDN
  username       Username for portal administrator
  password       Password. Enter ? to prompt in CLI
  filename       output filename

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Add verbose logging
  -a, --all      All Filers, All Tenants

(ctools) PS C:\Users\ctera\git\ctools> python ctools.py get_status portal.ctera.me admin ? report.csv --all
2021-09-23 17:21:17,257 [INFO] Starting ctools
Password:
2021-09-23 17:21:20,109 [INFO] Logging into portal.ctera.me
2021-09-23 17:21:20,226 [INFO] User logged in. {'host': 'portal.ctera.me', 'user': 'admin'}
2021-09-23 17:21:20,262 [WARNING] Allow Single Sign On to Devices is not enabled. Some tasks may fail or output may be incomplete
2021-09-23 17:21:20,262 [INFO] Starting status task
2021-09-23 17:21:20,287 [INFO] Getting all Filers since tenant is Administration
2021-09-23 17:21:21,585 [INFO] Executing CLI command. {'cli_command': 'dbg level'}
2021-09-23 17:21:21,597 [INFO] CLI command executed. {'cli_command': 'dbg level'}
2021-09-23 17:21:23,237 [INFO] Executing CLI command. {'cli_command': 'dbg level'}
2021-09-23 17:21:23,247 [INFO] CLI command executed. {'cli_command': 'dbg level'}
2021-09-23 17:21:24,109 [INFO] Executing CLI command. {'cli_command': 'dbg level'}
2021-09-23 17:21:24,121 [INFO] CLI command executed. {'cli_command': 'dbg level'}
2021-09-23 17:21:25,209 [INFO] Executing CLI command. {'cli_command': 'dbg level'}
2021-09-23 17:21:25,221 [INFO] CLI command executed. {'cli_command': 'dbg level'}
2021-09-23 17:21:25,246 [INFO] User logged out. {'host': 'portal.ctera.me', 'user': 'admin'}
2021-09-23 17:21:25,249 [INFO] Finished status task.
```
