# CTERA Portal WORM Settings Management Script

This script provides functionality to retrieve and update WORM (Write Once Read Many) settings for folders in CTERA Portal using the cterasdk Python library. WORM is a compliance feature that ensures data immutability by preventing modification or deletion of files after they are written.

## Features

- **Get WORM Settings**: Retrieve and display current WORM configuration for a specified folder
- **Set WORM Grace Period**: Update the grace period for WORM-protected folders (in days, hours, or minutes)
- **Date-Based Grace Period**: Calculate and set grace period automatically based on a target date
- Uses cterasdk API methods instead of direct curl calls
- Automatic session management with login/logout
- Detailed output showing all WORM settings including grace period, retention mode, and retention period

## Prerequisites

- Python 3.x
- `cterasdk` library

## Installation

1. Clone this repository or download the script file.
2. Install the required Python library:
   ```sh
   pip install cterasdk
   ```

## Usage

The script supports two main commands: `get` and `set`.

### Get WORM Settings

Retrieve and display WORM settings for a folder:

```sh
python main.py get --folder-id <folder_id> [--portal <address>] [--username <user>] [--password <pass>]
```

**Example:**
```sh
python main.py get --folder-id 69
```

### Set WORM Grace Period

Update the WORM grace period for a folder. You must specify one of: `--days`, `--hours`, `--minutes`, or `--date`:

```sh
python main.py set --folder-id <folder_id> (--days <n> | --hours <n> | --minutes <n> | --date <date>) [--portal <address>] [--username <user>] [--password <pass>]
```

**Examples:**
```sh
# Set grace period to 7 days
python main.py set --folder-id 69 --days 7

# Set grace period to 12 hours
python main.py set --folder-id 69 --hours 12

# Set grace period to 30 minutes
python main.py set --folder-id 69 --minutes 30

# Set grace period based on target date (calculates days automatically)
python main.py set --folder-id 69 --date "20 Feb 2026"
# If today is Feb 19, 2026: Sets grace period to 1 day
# If today is Feb 18, 2026: Sets grace period to 2 days
```

#### Date Format

The `--date` option accepts dates in multiple formats:
- `"20 Feb 2026"` or `"20 February 2026"` (DD MMM YYYY) - **Recommended, unambiguous**
- `"2026-02-20"` (YYYY-MM-DD) - **Recommended, unambiguous**
- `"20/02/2026"` (DD/MM/YYYY)
- `"02/20/2026"` (MM/DD/YYYY)
- `"20-02-2026"` (DD-MM-YYYY)

**Important Note on Slash Formats (DD/MM vs MM/DD):**

The script tries formats in order: DD/MM/YYYY first, then MM/DD/YYYY. This means:
- `"20/02/2026"` → Parsed as **February 20th** (DD/MM, because day 20 > 12, so MM/DD would be invalid)
- `"02/20/2026"` → Parsed as **February 20th** (MM/DD, because month 20 doesn't exist, so DD/MM fails)
- `"01/02/2026"` → Parsed as **February 1st** (DD/MM, because it's tried first and succeeds)

**To avoid ambiguity**, use formats with month names (e.g., `"20 Feb 2026"`) or ISO format (e.g., `"2026-02-20"`).

The script calculates the number of days from today to the target date and sets the grace period accordingly. **Note:** The target date must be in the future; past dates will result in an error.

### Command Line Arguments

#### Common Arguments (for both `get` and `set` commands):

- `--folder-id` (required): The folder ID to query or update
- `--portal` (optional): CTERA Portal address (default: `192.168.27.67`)
- `--username` (optional): Username for CTERA Portal login (default: `admin`)
- `--password` (optional): Password for CTERA Portal login (default: `Sooraj@123`)

#### Set Command Specific Arguments (mutually exclusive):

- `--days <n>`: Set grace period in days
- `--hours <n>`: Set grace period in hours
- `--minutes <n>`: Set grace period in minutes
- `--date <date>`: Set grace period based on target date. The script calculates the number of days from today to the target date and sets the grace period accordingly. Supports multiple date formats (e.g., "20 Feb 2026", "20/02/2026", "2026-02-20")

## Output

### Get Command Output

The script displays:
- **WORM Enabled**: Whether WORM is enabled for the folder
- **Grace Period**: The current grace period amount and type (Days/Hours/Minutes)
- **Retention Mode**: The retention mode (e.g., "Compliance")
- **Retention Period**: The retention period amount and type
- **Full WORM Settings Object**: Complete JSON representation of WORM settings

**Example Output:**
```
[INFO] Folder ID: 69
[INFO] WORM Enabled: True

[INFO] WORM Grace Period Settings:
  Amount: 7
  Type: Days

[INFO] Full WORM Settings Object:
  {
     "_classname": "WormSettings",
     "gracePeriod": {
          "_classname": "WormPeriod",
          "amount": 7,
          "type": "Days"
     },
     "retentionMode": "Compliance",
     "worm": true,
     "retentionPeriod": {
          "_classname": "WormPeriod",
          "amount": 1,
          "type": "Days"
     }
}
```

### Set Command Output

After successfully updating the grace period, the script:
1. If using `--date`, displays the target date and calculated number of days
2. Confirms the update was successful
3. Displays the new grace period settings
4. Automatically retrieves and displays the updated WORM settings

**Example Output (with --date option):**
```
[INFO] Target date: 20 Feb 2026
[INFO] Calculated days from today: 1
[INFO] Retrieving current folder settings for folder ID: 69...
[INFO] Updating WORM grace period to 1 Days...
[SUCCESS] WORM grace period updated successfully!
```

## How It Works

### Get WORM Settings

1. Establishes connection to CTERA Portal using GlobalAdmin
2. Uses `admin.api.get('objs/{folder_id}')` to retrieve the folder object
3. Extracts and displays WORM settings from the folder object

### Set WORM Grace Period

1. If using `--date` option:
   - Parses the target date string using multiple format attempts
   - Calculates the number of days from today to the target date
   - Validates that the target date is in the future
2. Retrieves the current folder object using `admin.api.get()`
3. Validates that WORM settings exist for the folder
4. Updates the `gracePeriod.amount` and `gracePeriod.type` attributes
5. Saves the updated object using `admin.api.put()`
6. Retrieves and displays the updated settings for verification

## Technical Details

- **API Methods Used**: 
  - `admin.api.get('objs/{folder_id}')` - Retrieve folder object
  - `admin.api.put('objs/{folder_id}', folder_obj)` - Update folder object
- **SSL Settings**: SSL verification is disabled by default for self-signed certificates
- **Error Handling**: Comprehensive error handling for CTERA API exceptions and general exceptions

## Important Notes

- The folder must already have WORM settings configured before you can update the grace period
- The script will create a grace period object if it doesn't exist, but WORM settings must be present
- Ensure you have the necessary permissions to modify folder settings in CTERA Portal
- The script disables SSL verification for the session. If your server requires SSL verification, you may need to modify the script accordingly
- Default credentials are hardcoded in the script. For production use, consider using environment variables or a configuration file

## Error Handling

The script handles the following error scenarios:
- Invalid folder ID
- Folder does not have WORM settings configured
- Authentication failures
- Network connectivity issues
- CTERA API errors
- Invalid date format (when using `--date` option)
- Past dates (when using `--date` option - target date must be in the future)

## Related Scripts

- `CoreWorm.sh` - Bash script version using curl for WORM management (located in repository root)

## License

This script is provided under the MIT License. See the LICENSE file for details.

---

For additional assistance or inquiries, please contact the CTERA support team or refer to the [CTERA documentation](https://www.ctera.com/docs/).
