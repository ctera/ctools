# ctools

## Purpose

A tool to check the status of all CTERA filers and more coming soon.

## Development Requirements

- [Python 3.5+](https://www.python.org/)
- [git](https://git-scm.com/)
- [pip](https://pip.pypa.io/en/stable/user_guide/)
- [CTERA Environment](https://www.ctera.com/)

## Setup

```
git clone https://github.com/ctera/ctools.git
python3 -m pip install -r ctools/requirements.txt
```

## Run

```
python3 ctools.py
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
