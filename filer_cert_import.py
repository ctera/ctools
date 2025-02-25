from cterasdk import Edge, CTERAException, settings
import logging

def import_test(address, username, password, private_key_file, *certificate_files):
  print("Address:", address)
  print("Username:", username)
  print("Password:", password)
  print("Private Key File:", private_key_file)
  print("Certificate Files:", certificate_files)
  print("End")

  settings.sessions.management.ssl = False
  with Edge(address) as edge:
    logging.info('Attempting login')
    edge.login(username, password)
    logging.info('Logged in successfully')
    logging.info('Logging Out')

def import_cert(address, username, password, private_key_file, *certificate_files):
  
  settings.sessions.management.ssl = False
  with Edge(address) as edge:
    logging.info('Attempting login')
    edge.login(username, password)
    logging.info('Logged in successfully')
    logging.info('Updating certificate')
    try:
      # Grab firmware version of Edge Filer to see which version of the API to use
      firmware_version = edge.api.get('/status/device/runningFirmware')

      # If firmware is 7.8 or higher, use the new API
      if is_firmware_newer_or_equal(firmware_version):
        edge.ssl.server.import_certificate(private_key_file, *certificate_files)
      else:
        edge.ssl.import_certificate(private_key_file, *certificate_files)
      

      # If firmware is 7.7 or lower, use the old API


      
    except Exception as e:
      logging.error(f'Error importing certificate: {e}')
      return
    logging.info('Certificate imported successfully')

def is_firmware_newer_or_equal(version, target_version="7.8"):
    # Split both version strings into a list of integers
    version_parts = list(map(int, version.split('.')))
    target_parts = list(map(int, target_version.split('.')))

    # Compare each part of the version
    return version_parts >= target_parts

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  import_cert('IP_ADDRESS', 'USERNAME', 'PASSWORD', 'private_key.pem', 'cert1.pem', 'cert2.pem')  # certificate files parameter accepts multiple files

