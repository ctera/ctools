# CTools

## Description

CTools is a toolbox to easily check, manage, run bulk operations, automate tasks across multiple CTERA Edge Filers and Portal via GUI or CLI.

### Getting Started

You do not need to build or compile the tool yourself.
Simply download the ready-to-use EXE file directly from the [Releases](https://github.com/ctera/ctools/releases) tab.

The EXE is digitally signed and ready to run immediately.

### Alternative (Python version)
If you prefer, you can run the tool from the Python source instead. This option requires Python and manual setup.

- #### Development Requirements
  - [CTERA Environment](https://www.ctera.com/)
  - [CTERA SDK for Python](https://github.com/ctera/ctera-python-sdk)
  - [Python](https://www.python.org/downloads/)
  - [git](https://git-scm.com/)
  - [PySide6](https://pypi.org/project/PySide6/)


## Requirements

1. **Use a Portal Global Administrator account to login.**

2. **Ensure necessary Remote Administration settings are enabled on the portal:** (Applies to portal versions older than 7.2)

    Access the Global Administration view > Navigate to Settings > Control Panel > User Roles > Read/Write Administrator -> Ensure "Allow Single Sign On to Devices" is checked

    - [documentation](https://kb.ctera.com/v1/docs/en/customizing-administrator-roles-1?highlight=Allow%20Single%20Sign%20On%20to%20Devices) 

## Please review this document to learn more about each tool

## Using CTools

When you launch **CTools**, two windows will open:

### 1. Main Window (GUI)
- Provides an interactive graphical interface for selecting and executing tasks.

### 2. Console Window
- This black window displays detailed logs, progress, and relevant runtime messages.
- **Important:** Keep this window open to view real-time operation status and debug information.

### Running Commands:
To see an explanation for what each tool does and how to use it, hover over the "i" button.

## Run CMD Tab

This tab allows you to run a command remotely across one or multiple CTERA Edge Filers. Below are explanations of each available field and checkbox:

| Field/Option                             | Description                                                                                                                                                                         |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                                                                                             |
| **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                                                                                   |
| **Password**                               | Password associated with the provided admin username.                                                                                                                              |
| **Command**                                | The command you want to execute on the filer(s). For example, to change the admin password for all the edge filers, please type `set /config/auth/users/admin/password "P@ssw0rd"` |
| **Tenant Name**                            | Specify the tenant name, if applicable, when running a command against specific tenants.                                                                                           |
| **Device Name (Overrides "All Tenants")**  | Specify an individual filer name to target; overrides running on all devices if provided.                                                                                          |
| **Run on all Tenants (No device name needed)** | Checkbox: Select to execute the command on all tenants connected to the specified portal.                                                                                          |
| **Verbose Logging**                        | Checkbox: Enable this option for detailed logging output in the console window.                                                                                                    |
| **Start**                                  | Initiates execution of the specified command.                                                                                                                                      |
| **Cancel**                                 | Cancels the current operation.                                                                                                                                                     |


#### Show Status
Grab in depth stats about all devices in the CTERA Portal. Saved to the same directory as the program is run from.

#### Suspend Sync / Unsuspend Sync
Suspend or Unsuspend Cloud Drive syncing on a Edge Filer.

#### Enable SSH / Disable SSH
Enable or Disable the ssh service on a given Edge Filer and add the public key to the authorized_keys of the Edge Filer.
If no public key is provided, a new keypair will generated and saved to the Downloads folder.

#### Enable Telnet
Enable the telnet service on a given Edge Filer. If no unlock code is provided, return the required MAC address
and firmware version to get an unlock code from CTERA Support.

#### Reset Password
Reset a local user account password on a Edge Filer.

#### CloudFS
Create folder groups and cloud folders using a pre-populated CSV file. Download the template here:
https://github.com/ctera/ctools/blob/main/templates/cloud_fs.csv

#### Delete Shares
Delete shares from all Gateway devices containing specified pattern

#### Copy Shares
Copy Shares from one specified Edge Filer to a different specified Edge Filer

#### Add/Remove Members
Add/remove domain users/groups to the Administrators group on all devices on all portals, all devices on specified portal tenant, or one device on specified portal tenant

#### Report Zones
Create zones report for details such as Devices, Total Size, Total Folders, and Total Files in the desired output location.

#### Populate Shares
Populate edge filer shares for every cloud folder in its portal (excluding My Files).

#### Add Domain to Advanced Mapping
Add domain to advanced mapping under the UID/GID mappings on all devices, or one specified device.

#### Shares Report
Export shares list for all edge filers (Detailed)

#### Import Certificate
Import a certificate to an Edge Filer.

## Adding Requests for new features/scripts
This toolset is always evolving and growing. If you have a request for Ctools, you can create an "issue" at this link:
https://github.com/ctera/ctools/issues

If you have a quick question, feel free to email lakep@ctera.com and mukeshj@ctera.com.
