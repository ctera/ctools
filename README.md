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
python3 ctools/CTools.py
```

## Example

```
user@localhost:~$ python3 ctools/CTools.py
Tasks to run:
1. Get Details of all Connected Edge Filers to a specific Portal.
Enter a task number to execute: 1
Portal (IP, Hostname or FQDN): portal.example.com
Admin Username: admin
Admin Password:
Output filename. Make sure extension is csv: status.csv
2020-12-15 17:30:44,777    INFO [login.py:19] [login] - User logged in. {'host': 'portal.example.com', 'user': 'admin'}
Output file does not exist. Creating new file
2020-12-15 17:30:44,846    INFO [cli.py:16] [run_command] - Executing CLI command. {'cli_command': 'dbg le'}
2020-12-15 17:30:44,850    INFO [cli.py:20] [run_command] - CLI command executed. {'cli_command': 'dbg le'}
2020-12-15 17:30:44,882    INFO [login.py:26] [logout] - User logged out. {'host': 'portal.example.com'}
user@localhost:~$ cat status.csv
Gateway,CloudSync Status,selfScanIntervalInHours,FilesInUploadQueue,scanningFiles,selfVerificationscanningFiles,MetaLogsSetting,MetaLogMaxSize,MetaLogMaxFiles,CurrentFirmware,License,EvictionPercentage,CurrentVolumeStorage,IP Config,Alerts
my-vGateway,"['id"": ""Synced"",']",168,0,0,0,['0x00000404\tCurrent dbg level'],10,7,6.0.771.19,EV16,75,"{
     ""_classname"": ""StorageSummaryProc"",
     ""totalVolumeSpace"": 102400,
     ""usedVolumeSpace"": 79075,
     ""freeVolumeSpace"": 23325
}","['address"": null,']","{
     ""_classname"": ""AlertSettings"",
     ""SMTPServer"": null,
     ""auth"": null,
     ""emails"": [],
     ""from"": ""alert-no-reply@ctera.com"",
     ""logCodes"": [],
     ""minSeverity"": ""critical"",
     ""port"": 25,
     ""specificAlerts"": {
          ""_classname"": ""SpecificAlerts"",
          ""BackupFailAlert"": true,
          ""BackupFailDays"": 3,
          ""CloudConnectFailAlert"": true,
          ""CloudConnectFailHours"": 6,
          ""CloudSyncFailAlert"": true,
          ""CloudSyncFailHours"": 5,
          ""NotifyBackupSuccess"": false,
          ""NotifyDeviceStarted"": false,
          ""NotifyFirmwareUpgrade"": true,
          ""NotifyRedundantPSUFailure"": false,
          ""NotifySyncSuccess"": false,
          ""SyncFailAlert"": true,
          ""SyncFailDays"": 3,
          ""VolumeFullAlert"": true,
          ""VolumeFullPercent"": 95,
          ""VolumeQuotaFullAlert"": true,
          ""VolumeQuotaFullPercent"": 95
     },
     ""useAuth"": false,
     ""useCustomServer"": false,
     ""useTLS"": true
}"
```
