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

Here we use Chocolatey as a commmand line package manager for Windows.
Run PowerShell as an Administrator to setup. Close and re-open PowerShell
after to refresh the environment and enable tab completion of commands.

```
Invoke-WebRequest https://chocolatey.org/install.ps1 -UseBasicParsing | Invoke-Expression
choco upgrade -y
choco install python --version=3.8.10 --yes
choco install git --yes
git clone https://github.com/ctera/ctools.git
python -m pip install -r .\ctools\requirements.txt
```

## Run

```
python ctools.py
```

## Example

```
[user@localhost ctools]$ ./ctools.py
2021-01-22 12:27:51,898    INFO [ctools.py:10] [<module>] - Starting ctools

    #################
       ctools menu
         v 1.5.1
    #################

    Available tasks:

    0. Quit
    1. Record status details of all connected Edge Filers.
    2. Enable telnet on one or more connected Edge Filers.
    3. Run a specified command on all connected Edge Filers.

Enter a task number to run: 3
2021-01-22 12:27:53,246    INFO [run_cmd.py:12] [run_cmd] - Starting run_cmd task
Portal (IP, Hostname or FQDN): portal.example.com
Admin Username: admin
Admin Password: password
2021-01-22 12:27:55,279    INFO [login.py:18] [login] - Logging into portal.example.com
2021-01-22 12:27:55,347    INFO [login.py:19] [login] - User logged in. {'host': 'portal.example.com', 'user': 'admin'}
2021-01-22 12:27:55,360    INFO [login.py:21] [login] - Successfully logged in to portal.example.com
Enter command to run: dbg level backup
You enetered:  dbg level backup
### Start command on: todd-vGateway
2021-01-22 12:28:00,655    INFO [cli.py:16] [run_command] - Executing CLI command. {'cli_command': 'dbg level backup'}
2021-01-22 12:28:00,782    INFO [cli.py:20] [run_command] - CLI command executed. {'cli_command': 'dbg level backup'}
Response:
 Setting debug level to 0x00000800
### End command on: todd-vGateway
### Start command on: vGateway-5439
2021-01-22 12:28:00,782    INFO [cli.py:16] [run_command] - Executing CLI command. {'cli_command': 'dbg level backup'}
2021-01-22 12:28:00,911    INFO [cli.py:20] [run_command] - CLI command executed. {'cli_command': 'dbg level backup'}
Response:
 Setting debug level to 0x00000800
### End command on: vGateway-5439
2021-01-22 12:28:00,911    INFO [run_cmd.py:26] [run_cmd] - Finished run_cmd task
Finished task. Returning to menu.

    #################
       ctools menu
         v 1.5.1
    #################

    Available tasks:

    0. Quit
    1. Record status details of all connected Edge Filers.
    2. Enable telnet on one or more connected Edge Filers.
    3. Run a specified command on all connected Edge Filers.

Enter a task number to run: 0
[user@localhost] ctools]$
```
