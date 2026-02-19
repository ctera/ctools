"""Import certificate tool - Import SSL certificates to Edge Filers."""

import logging
from typing import List

from cterasdk import Edge, settings


def import_certificate(
    address: str,
    username: str,
    password: str,
    private_key_file: str,
    certificate_files: List[str]
) -> None:
    """
    Import SSL certificate to an Edge Filer.

    Args:
        address: Device IP address or hostname
        username: Device admin username
        password: Device admin password
        private_key_file: Path to private key file
        certificate_files: List of paths to certificate files
    """
    logging.info("Starting import certificate task.")
    logging.info("Device: %s", address)
    logging.info("Private key file: %s", private_key_file)
    logging.info("Certificate files: %s", certificate_files)

    settings.sessions.management.ssl = False

    try:
        with Edge(address) as edge:
            logging.info("Connecting to device: %s", address)
            edge.login(username, password)
            logging.info("Logged in successfully")

            logging.info("Importing certificate...")

            try:
                # Get firmware version to determine API to use
                firmware_version = edge.api.get('/status/device/runningFirmware')
                logging.info("Firmware version: %s", firmware_version)

                # Check if firmware is 7.8 or higher
                if _is_firmware_newer_or_equal(firmware_version, "7.8"):
                    # New API for 7.8+
                    edge.ssl.server.import_certificate(private_key_file, *certificate_files)
                else:
                    # Old API for 7.7 and below
                    edge.ssl.import_certificate(private_key_file, *certificate_files)

                logging.info("Certificate imported successfully")

            except Exception as e:
                logging.error("Error importing certificate: %s", e)
                raise

            logging.info("Logging out...")

        logging.info("Finished import certificate task.")

    except Exception as e:
        logging.error("Error in import certificate task: %s", e)
        raise


def _is_firmware_newer_or_equal(version: str, target_version: str = "7.8") -> bool:
    """
    Check if firmware version is newer than or equal to target version.

    Args:
        version: Current firmware version string
        target_version: Target version to compare against

    Returns:
        True if version >= target_version
    """
    try:
        version_parts = list(map(int, version.split('.')))
        target_parts = list(map(int, target_version.split('.')))
        return version_parts >= target_parts
    except (ValueError, AttributeError):
        logging.warning("Could not parse firmware version: %s", version)
        return True  # Default to new API
