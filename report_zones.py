import os
import logging
from datetime import datetime
import csv
from cterasdk import GlobalAdmin, settings, config, CTERAException, Object
from cterasdk.exceptions import ConsentException
from cterasdk.core import query

class FileNames:
    LogBaseName = 'Zones-'

def create(address, user, password, output, debug):
  output = output if output is not None else 'output'
  output = os.path.expandvars(output)
  if not os.path.exists(output):
    os.makedirs(output)
  if not os.path.isdir(output):
    logging.error('"%s" is not a folder' % os.path.basename(output))
  
  path = os.path.join(output, datetime.now().strftime('Portal-Reports-%Y_%m_%d') + '.csv')

  if password is None:
    logging.error('Password required')
    return
  
  FileNames.output = output if output is not None else FileNames.output
  FileNames.output = os.path.expandvars(FileNames.output)
  if not os.path.exists(FileNames.output):
    os.makedirs(FileNames.output)
  if not os.path.isdir(FileNames.output):
    logging.error('"%s" is not a folder' % os.path.basename(FileNames.output))

  path = os.path.join(FileNames.output, datetime.now().strftime(FileNames.LogBaseName + '%Y_%m_%d-%M_%S') + '.csv')

  with open(path, 'w', newline='\n', encoding='utf-8') as outputcsv:
    fieldnames = ['Portal','Zone','Cloud Folders','Devices','Total Size','Total Folders','Total Files']
    writer = csv.DictWriter(outputcsv, fieldnames=fieldnames)
    writer.writeheader()
    
    try:
      zonereport = gather_report(address,user,password,writer)
    except:
      logging.error(f'Login to portal {address} failed.')

def gather_report(address, user, password ,writer):
  """Disable SSL Verification"""
  settings.sessions.management.ssl = False
  settings.sessions.management.edge.services.ssl = False

  results = {}
  results['Portal']=address
  results['Error']="OK"

  try:
    admin = GlobalAdmin(address)
    admin = _login(admin, user, password)

    admin.portals.browse_global_admin()
    zonereport = {}

    tenants = admin.portals.list_tenants()
    for portal in tenants:
      tenant = portal.name

      if tenant is not None:
        admin.portals.browse(tenant)
        zones = admin.cloudfs.zones.all()

        for zone in zones:
          zonesummary = {}
          zonesummary['Portal'] = tenant
          zonesummary['Zone'] = zone.name

          if zone.name == 'All Folders':
            zonesummary['Cloud Folders'] = zone.name
          else:
            zonesummary['Cloud Folders'] = ','.join(getcloudfolders(admin, zone.zoneId))
          
          devices = []

          for device in zone.topDevices:
            devices.append(device.name)

          zonesummary['Devices'] = ','.join(devices)
          zonesummary['Total Size'] = zone.zoneStatistics.totalSize
          zonesummary['Total Folders'] = zone.zoneStatistics.totalFolders
          zonesummary['Total Files'] = zone.zoneStatistics.totalFiles
          zonereport[zone.name] = zonesummary

          logging.info(f'Entry for {zone.name} on portal: {tenant} completed.')
          writer.writerow(zonesummary)
      else:
        for portal in tenants:
          tenant = portal.name
          admin.portals.browse(tenant)
          zones = admin.cloudfs.zones.all()

          for zone in zones:
            zonereport[zone.name] = zone
    admin.logout()
    return zonereport
  except CTERAException as e:
    logging.error(f'Error: {e}')
    return None

def _login(host, user, secret):
  try:
    host.login(user, secret)
  except CTERAException as e:
    if e.response.code == 403:
      logging.error('Login failed. Invalid credentials')
  return host

def getcloudfolders(admin,zoneId):
    cloudfolders = []
    param = _zone_param(zoneId)
    response = admin.api.execute('/', 'getZoneFolders', param)
    for folder in response.objects:
        cloudfolders.append(folder.name)
    return cloudfolders

def _zone_param(zid=None):
    param = Object()
    builder = query.QueryParamBuilder().include_classname().startFrom(0).countLimit(100).orFilter(True)
    param.query = builder.build()
    param._classname = "ZoneQuery"
    param.delta = Object()
    param.delta._classname = 'ZoneDelta'
    param.delta.policyDelta = Object()
    param.delta.policyDelta = []
    param.zoneId = zid
    return param