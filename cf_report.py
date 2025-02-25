import argparse
import csv
from cterasdk import GlobalAdmin, settings

# Generate report for all cloud folders and their statistics
def report(ip_addr, username, password, output_file='cloud_folders_report.csv'):
    settings.sessions.management.ssl = False

    # Open the CSV file for writing
    with open(output_file, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write the header row
        csv_writer.writerow(['Folder Name', 'Size (GB)'])

        with GlobalAdmin(ip_addr) as ga:
            ga.login(username, password)

            for element in ga.files.walk('Users/'):
                if element.scope == "InsideCloudFolder":
                    print("All Cloud Folders Read...")
                    print("Exiting...")
                    break
                
                if element.scope != "UsersFoldersContainer":
                    size_gb = element.size / (1024 ** 3)
                    print(element.name, ": ", f"{size_gb:.2f} GB")
                    # Write the folder data to the CSV file
                    csv_writer.writerow([element.name, f"{size_gb:.2f}"])

    print(f"Report successfully saved to {output_file}")

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate a report of cloud folders and their statistics.")
    parser.add_argument("ip_addr", help="IP address of the CTERA Portal")
    parser.add_argument("username", help="Admin Username for Portal")
    parser.add_argument("password", help="Admin Password for Portal")
    parser.add_argument("--output", default="cloud_folders_report.csv", help="Output CSV file name (default: cloud_folders_report.csv)")

    # Parse arguments
    args = parser.parse_args()

    # Run the report
    report(args.ip_addr, args.username, args.password, args.output)
