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

![image](https://github.com/user-attachments/assets/4214fbe0-2f83-4942-a1c2-b5dec95c4a2d)

### Running Commands:
To see an explanation for what each tool does and how to use it, hover over the "i" button.

- **Run CMD**  
  This tab allows you to run a command remotely across one or multiple CTERA Edge Filers. This is useful in sitatuations when you have many filers and need to make a change across all of them without manually logging into each. Below are explanations of each available field and checkbox:

    | Field/Option                                  | Description                                                                                                                                                                         |
    | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | **Address (Portal IP, hostname, or FQDN)**    | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                                                                                             |
    | **Portal Admin Username**                     | Admin username used to login to Portal Admin UI.                                                                                                                                    |
    | **Password**                                  | Password associated with the provided admin username.                                                                                                                               |
    | **Command**                                   | The command you want to execute on the filer(s). For example, to change the admin password for all the edge filers, please type `set /config/auth/users/admin/password "P@ssw0rd"`  |
    | **Tenant Name**                               | Specify the portal tenant name, if the command doesn't need to be run on all devices and only on device in a specific tenant.                                                       |
    | **Device Name (Overrides "All Tenants")**     | Specify an individual filer name to target; overrides running on all devices if provided.                                                                                           |
    | **Run on all Tenants (No device name needed)**| Checkbox: Select to execute the command on all tenants connected to the specified portal.                                                                                           |
    | **Verbose Logging**                           | Checkbox: Enable this option for detailed logging output in the console window.                                                                                                     |
    | **Start**                                     | Initiates execution of the specified command.                                                                                                                                       |
    | **Cancel**                                    | Cancels the current operation.                                                                                                                                                      |

- **Show Status**  
  This tab helps in pulling detailed information from all Edge Filers connected to the portal, including memory, CPU, disk usage, log settings, Active Directory (AD) status, CloudSync queue status, and more. The output is saved in a `.csv` file format, which can be opened in Excel or any other compatible application.

  | Field/Option                                | Description                                                                                                          |
  | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
  | **Address (Portal IP, hostname, or FQDN)**  | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                              |
  | **Portal Admin Username**                   | Admin username used to login to Portal Admin UI.                                                                     |
  | **Password**                                | Password associated with the provided admin username.                                                                |
  | **File Name**                               | Specify the file name with a `.csv` extension to save the output.                                                    |
  | **Run on all Tenants**                      | Checkbox: Select to pull status information from all tenants connected to the specified portal.                      |
  | **Verbose Logging**                         | Checkbox: Enable this option for detailed logging output in the console window.                                      |
  | **Start**                                   | Initiates execution of the Show Status command.                                                                      |
  | **Cancel**                                  | Cancels the current operation.                                                                                       |

- **Suspend Sync / Unsuspend Sync**  
  These tabs help you remotely suspend or unsuspend sync operations on Edge Filers. This is particularly useful when the device UI is not reachable.

  | Field/Option                               | Description                                                                                                          |
  | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                              |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                     |
  | **Password**                               | Password associated with the provided admin username.                                                                |
  | **Device Name**                            | Specify the target filer device name.                                                                                |
  | **Tenant Name**                            | Specify the portal tenant name, where device exists                                                                  |
  | **Verbose Logging**                        | Checkbox: Enable this option for detailed logging output in the console window.                                      |
  | **Start**                                  | Initiates execution of the specified command (Suspend/Unsuspend).                                                    |
  | **Cancel**                                 | Cancels the current operation.                                                                                       |

- **Enable SSH / Disable SSH**  
  The **Enable SSH** tab allows you to remotely enable SSH access on Edge Filers.  
  The **Disable SSH** tab disables SSH access.

  | Field/Option                               | Description                                                                                                                   |
  | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                                       |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                              |
  | **Password**                               | Password associated with the provided admin username.                                                                         |
  | **Device Name**                            | Specify the target filer device name.                                                                                         |
  | **Tenant Name**                            | Specify the portal tenant name, where device exist.                                                                           |
  | **SSH Public Key**                         | Paste the SSH public key generated using PuTTYgen (or a similar key-generation tool) after creating a public/private key pair (see example below). |
  | **Verbose Logging**                        | Checkbox: Enable this option for detailed logging output in the console window.                                               |
  | **Start**                                  | Initiates execution of the specified command (Enable SSH / Disable SSH).                                                      |
  | **Cancel**                                 | Cancels the current operation.                                                                                                |

  **Example SSH Public Key format:**
  ```shell
  exec /config/device startSSHD publicKey "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEA0MUxI0nZ4jJPSoGnbFb/Qd4EbEipjjogIpOGVoOGeJx2DMJjZBF7MF/d/3Rt/SP5QDcnRvgIMA0e7o6wH6Zib7QvB9tXbeCnK68NQjx1KYabtKhrPlNC7VCOjeW8s9pC244nDnCsk8XLRNAUIOSAnQC/Iu+iqn0RV2D6qZzUJ4hkkcTh0G7wroDMkVmqQ3R+/2ibiRjux9C3HaHX7W+lVVJGF3MCK/+FRjb3MWQ+U2LYmwsvzq+xTJyikUwBS3Kng0WV4omzyaxjJ6vkkZh4wvlhdwfR6QEabW6Xk7wpEEXej6NaT9l+3CjXEWbrI8hD3mtICL+bdstPO2DeS7UcXw== rsa-key-20200821"

- **Enable Telnet**  
  This tab enables Telnet access on Edge Filers. The required activation code must be obtained from CTERA Support by providing them the Edge Filer's MAC address (available from the Edge Filer UI) and the installed version.

  | Field/Option                               | Description                                                                                                                    |
  | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                                        |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                               |
  | **Password**                               | Password associated with the provided admin username.                                                                          |
  | **Device Name**                            | Specify the target filer device name.                                                                                          |
  | **Tenant Name**                            | Specify the tenant name, if applicable, when enabling Telnet for specific tenants.                                             |
  | **Required Code for Telnet**               | Enter the activation code provided by CTERA Support after submitting the Edge Filer's MAC address and version information.      |
  | **Verbose Logging**                        | Checkbox: Enable this option for detailed logging output in the console window.                                                |
  | **Start**                                  | Initiates execution of the Enable Telnet command.                                                                              |
  | **Cancel**                                 | Cancels the current operation.                                                                                                 |

- **Reset Password**  
  This tab helps reset the admin or local user password for an Edge Filer when the current password has been lost or forgotten, but the device remains connected to the portal.

  | Field/Option                               | Description                                                                                                                    |
  | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                                        |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                               |
  | **Password**                               | Password associated with the provided admin username.                                                                          |
  | **Device Name**                            | Specify the target filer device name if it needs to be reset on only 1 filer                                                   |
  | **Tenant Name**                            | Specify the tenant name, where device exists.                                                                                  |
  | **Username for local user**                | Username of the local user whose password you want to reset (usually 'admin').                                                 |
  | **New filer password**                     | Enter the new password to set for the specified user.                                                                          |
  | **Run on all Devices (No device or tenant name needed)** | Checkbox: Select to reset the password on all devices connected to the specified portal.                         |
  | **Verbose Logging**                        | Checkbox: Enable this option for detailed logging output in the console window.                                                |
  | **Start**                                  | Initiates execution of the Reset Password command.                                                                             |
  | **Cancel**                                 | Cancels the current operation.                                                                                                 |

- **CloudFS**  
  This tab allows you to create multiple cloud folders on the portal using a CSV file. This is particularly useful when you have many cloud folders to create and prefer not to do so individually via the UI.

  | Field/Option                          | Description                                                                                                                    |
  | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
  | **Portal Address, hostname, or FQDN** | The IP address, hostname, or fully qualified domain name of your CTERA portal.                                                 |
  | **Username for portal admin**         | Admin username used to login to Portal Admin UI.                                                                               |
  | **Password**                          | Password associated with the provided admin username.                                                                          |
  | **CSV File**                          | Browse and select a CSV file with the list of cloud folders to be created.                                                     |
  | **Verbose**                           | Checkbox: Enable this option for detailed logging output in the console window.                                                |
  | **Start**                             | Initiates execution to create cloud folders as per the provided CSV file.                                                      |
  | **Cancel**                            | Cancels the current operation.                                                                                                 |

  **CSV Template:**  
  > You can download the CSV template [here](https://github.com/ctera/ctools/blob/main/templates/cloud_fs.csv).

- **Delete Shares**  
  This tab allows you to delete shares containing a specific keyword from all filers connected to the portal. For example, you can delete all shares containing the word "migration." After filling in the required fields and clicking **Start**, you'll be prompted to enter the keyword.

  | Field/Option                               | Description                                                                                                                    |
  | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal or filer.                                        |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                               |
  | **Password**                               | Password associated with the provided admin username.                                                                          |
  | **Start**                                  | Initiates execution and prompts for the keyword to identify shares to delete.                                                  |
  | **Cancel**                                 | Cancels the current operation.                                                                                                 |

- **Copy Shares**  
  This tab allows you to replicate share configurations from one Edge Filer (source) to another (destination). It creates all the share present on the source filer on the destination filer. Note that this operation does **not** copy the actual data—only the shares themselves are created.

  | Field/Option                          | Description                                                                                                   |
  | ------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
  | **Source Device IP/FQDN**             | IP address or fully qualified domain name of the source Edge Filer.                                            |
  | **Source Admin Username**             | Admin username used to log in to the source Edge Filer.                                                       |
  | **Source Admin Password**             | Password associated with the provided source admin username.                                                  |
  | **Destination Device IP/FQDN**        | IP address or fully qualified domain name of the destination Edge Filer.                                       |
  | **Destination Admin Username**        | Admin username used to log in to the destination Edge Filer.                                                   |
  | **Destination Admin Password**        | Password associated with the provided destination admin username.                                              |
  | **Verbose Logging**                   | Checkbox: Enable this option for detailed logging output in the console window.                               |
  | **Start**                             | Initiates execution to replicate share structures from the source to the destination filer.                   |
  | **Cancel**                            | Cancels the current operation.                                                                                |

- **Add/Remove Members to Admin Group**  
  This tab allows you to add or remove domain users or domain groups from the **Administrators** group on one or multiple Edge Filers. It’s particularly useful for efficiently managing administrative access across multiple devices.

  | Field/Option                            | Description                                                                                                                                                              |
  | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | **Portal Address, hostname, or FQDN**   | The IP address, hostname, or fully qualified domain name of your CTERA portal.                                                                                           |
  | **Username for portal admin**           | Admin username used to log in to Portal Admin UI.                                                                                                                        |
  | **Password**                            | Password associated with the provided admin username.                                                                                                                    |
  | **Add or Remove**                       | Select whether you want to **Add** or **Remove** members from the **Administrators** group. Selecting one option automatically updates the **Add** column accordingly.   |
  | **Add**                                 | Specify the member type (**Domain User** or **Domain Group**) to add or remove.                                                                                          |
  | **Perform on**                          | Select where to apply the changes: on **One Device**, **All Devices on One Tenant**, or **All Devices on All Tenants**.                                                  |
  | **Tenant Name**                         | Tenant name, required when performing on all devices within one tenant.                                                                                                 |
  | **Device Name**                         | Device name if performing the action on a single Edge Filer.                                                                                                             |
  | **User**                                | Domain user or group name to add or remove from the **Administrators** group.                                                                                            |
  | **Verbose Logging**                     | Checkbox: Enable this option for detailed logging output in the console window.                                                                                          |
  | **Start**                               | Initiates execution to add/remove members as configured.                                                                                                                 |
  | **Cancel**                              | Cancels the current operation.                                                                                                                                           |

- **Report Zones**  
  This tab pulls information about all zones and their details from connected portals and outputs them to a CSV file. The generated report includes:

  - **Portal Name**
  - **Zone Name**
  - **Cloud Folders**
  - **Devices**
  - **Total Size**
  - **Total Folders**
  - **Total Files**

  | Field/Option                               | Description                                                                                                           |
  | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal.                                        |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                      |
  | **Portal Admin Password**                  | Password associated with the provided admin username.                                                                 |
  | **Output Location**                        | Browse to select or specify the folder location to save the resulting CSV report file.                                |
  | **Start**                                  | Initiates the process and generates the Zones report.                                                                 |
  | **Cancel**                                 | Cancels the current operation.                                                                                        |

  **Note:**  
  The resulting CSV file can be opened in Excel or any other compatible application for further analysis.

- **Populate Shares**  
  This tab creates a share on an Edge Filer for each cloud folder (excluding "My Files"). It's especially useful when there are many cloud folders, and you need each one available as an individual share on the filer.

  | Field/Option                                 | Description                                                                                                                    |
  | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
  | **Address (Portal IP, hostname, or FQDN)**   | The IP address, hostname, or fully qualified domain name of your CTERA portal.                                                 |
  | **Portal Admin Username**                    | Admin username used to login to Portal Admin UI.                                                                               |
  | **Password**                                 | Password associated with the provided admin username.                                                                          |
  | **Device Name**                              | Specify the target Edge Filer device name where the shares should be populated.                                                |
  | **Domain Name**                              | Required only if domain users own cloud folders.                                                                               |
  | **Ignore cert warnings for login**           | Checkbox: Select this to bypass certificate warnings when connecting to the portal.                                            |
  | **Verbose Logging**                          | Checkbox: Enable this option for detailed logging output in the console window.                                                |
  | **Start**                                    | Initiates the creation of shares from existing cloud folders.                                                                  |
  | **Cancel**                                   | Cancels the current operation.                                                                                                 |

- **Add Domain to Advanced Mapping**  
  This tab adds additional Active Directory (AD) domains to Advanced Mappings on Edge Filers, enabling users from other AD domains to access shares.

  | Field/Option                               | Description                                                                                                                    |
  | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal.                                                 |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                               |
  | **Password**                               | Password associated with the provided admin username.                                                                          |
  | **Tenant (Empty if all devices on all tenants)** | Specify tenant name, leave blank if operation is for all tenants.                                                               |
  | **Device Name (Empty if multiple devices)** | Specify device name, leave blank if operation is for multiple devices.                                                          |
  | **Domain to be Added**                     | Name of the Active Directory domain to be added to Advanced Mappings.                                                          |
  | **Ignore cert warnings for login**         | Checkbox: Select this to bypass certificate warnings when connecting to the portal.                                            |
  | **Verbose Logging**                        | Checkbox: Enable this option for detailed logging output in the console window.                                                |
  | **Start**                                  | Initiates the process to add the specified domain to Advanced Mappings.                                                        |
  | **Cancel**                                 | Cancels the current operation.                                                                                                 |

- **Shares Report**  
  This tab generates a detailed CSV report of all shares configured across all connected Edge Filers. The resulting report includes the following information:

  - **Share Name**
  - **Share Path**
  - **Edge Filer Name**
  - **Edge Filer IP**

  | Field/Option                               | Description                                                                                                                       |
  | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
  | **Address (Portal IP, hostname, or FQDN)** | The IP address, hostname, or fully qualified domain name of your CTERA portal.                                                    |
  | **Portal Admin Username**                  | Admin username used to login to Portal Admin UI.                                                                                  |
  | **Password**                               | Password associated with the provided admin username.                                                                             |
  | **Tenant (Empty to run on all)**           | Specify tenant name if the report is specific to one tenant; leave blank to run for all tenants.                                  |
  | **Filename (.csv)**                        | Specify a filename with the `.csv` extension to save the generated report.                                                        |
  | **Ignore cert warnings for login**         | Checkbox: Select this to bypass certificate warnings when connecting to the portal.                                               |
  | **Verbose Logging**                        | Checkbox: Enable this option for detailed logging output in the console window.                                                   |
  | **Start**                                  | Initiates the process and generates the Shares report.                                                                            |
  | **Cancel**                                 | Cancels the current operation.                                                                                                    |

**Note:**  
The resulting CSV file can be opened in Excel or any other compatible application for further analysis.

- **Import Certificate**  
  This tab allows importing and updating the UI certificate on older Edge Filers where the direct certificate import option isn't available. To import the certificate, fill in the following fields:

  | Field/Option              | Description                                                                                               |
  | ------------------------- | --------------------------------------------------------------------------------------------------------- |
  | **Edge IP Address**       | IP address of the target Edge Filer.                                                                      |
  | **Admin Username**        | Admin username used to log in to the Edge Filer UI.                                                       |
  | **Admin Password**        | Password associated with the provided admin username.                                                     |
  | **Private Key File**      | Browse and select the private key file associated with the certificate.                                   |
  | **Certificate Files**     | Browse and select the certificate file(s) to import and update on the Edge Filer UI.                      |
  | **Verbose Logging**       | Checkbox: Enable this option for detailed logging output in the console window.                           |
  | **Start**                 | Initiates the import and update of the UI certificate.                                                    |
  | **Cancel**                | Cancels the current operation.                                                                            |

## Adding Requests for New Features or Scripts  

This toolset (**CTools**) is intended primarily for routine administrative tasks. If you have suggestions or feature requests related to simple administrative tasks, please either create an issue on our GitHub repository or open a support case:

- **GitHub Issues:** [https://github.com/ctera/ctools/issues](https://github.com/ctera/ctools/issues)  
- **CTERA Support:** [https://support.ctera.com](https://support.ctera.com)

