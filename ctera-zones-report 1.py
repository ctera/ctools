#!/usr/bin/python3
#v1.0.0 - Report


import os
import click
import logging
import urllib3
from datetime import datetime
from getpass import getpass
from cterasdk import GlobalAdmin, config, CTERAException, Object
from cterasdk.exceptions import ConsentException
from cterasdk.core import query
import cterasdk.settings  # unnecessary if you use: (from cterasdk import *)
from datetime import timedelta
import csv
import _thread

class FileNames:
    LogBaseName = 'Zones-'

@click.command(help="CTERA Portal Zone Report")
@click.option("-h", "--hostlist", required=True, help="file containing list of portal fqdns")
@click.option("-u", "--user", required=True, help="administrator user name")
@click.option("-p", "--password", required=False, help="administrator password")
@click.option("-o", "--output", required=False, help="output directory, defaults to downloads directory")
@click.option("--debug", is_flag=True, help="debug")
def create(hostlist, user, password, output, debug):

    #Create Output File
    output = output if output is not None else 'output'
    output = os.path.expandvars(output)
    if not os.path.exists(output):
        os.makedirs(output)
        #raise click.BadParameter('The system cannot find the folder specified', param=output, param_hint='-o')
    if not os.path.isdir(output):
        raise click.BadParameter('"%s" is not a folder' % os.path.basename(output), param=output, param_hint='-o')

    path = os.path.join(output, datetime.now().strftime('Portal-Reports-%Y_%m_%d') + '.csv')

    #Set Log Level
    config.Logging.get().setLevel(logging.INFO)
    if debug:
        config.Logging.get().setLevel(logging.DEBUG)

    #Get password
    if password is None:
        password = click.prompt('Password (%s)' % user, hide_input=True)

    #Read List of Portals
    try:
        with open(hostlist, encoding="utf8") as hosts:
            lines=hosts.read().splitlines()
    except:
        # Report error if the hosts file can't be opened.
        with open(ErrorFileName, "w+") as f:
            logging.getLogger().error('Hosts file does not exist')
            f.write('Hosts file does not exist')
            f.close()
            quit()

    #portal_list = ['cteraportal.ctera.me']
    #Create Output File
    FileNames.output = output if output is not None else FileNames.output
    FileNames.output = os.path.expandvars(FileNames.output)
    if not os.path.exists(FileNames.output):
        os.makedirs(FileNames.output)
    if not os.path.isdir(FileNames.output):
        raise click.BadParameter('"%s" is not a folder' % os.path.basename(FileNames.output), param=FileNames.output, param_hint='-o')

    path = os.path.join(FileNames.output, datetime.now().strftime(FileNames.LogBaseName + '%Y_%m_%d-%M_%S') + '.csv')

    with open(path, 'w', newline='\n', encoding='utf-8') as outputcsv:
        fieldnames = ['Portal','Zone','Cloud Folders','Devices','Total Size','Total Folders','Total Files']
        writer = csv.DictWriter(outputcsv, fieldnames=fieldnames)
        writer.writeheader()
        #Generate Reports for each Portal
        for host in lines:
            #print(host)
            try:
                zonereport = portal_login(host,user,password,writer)
            except:
                logging.getLogger().error(f'Login to portal {host} failed.')
                quit()


def portal_login(host,user,password,writer):
    """Disable SSL Verification"""
    cterasdk.settings.sessions.management.ssl = False
    cterasdk.settings.sessions.management.edge.services.ssl = False

    #Login to the portal and generate each report as needed.
    results = {}
    results['Portal']=host
    results['Error']="OK"
    try:

        admin = GlobalAdmin(host)
        admin = _login(admin, user, password)

        admin.portals.browse_global_admin()
        zonereport = {}
        # Browse default tenant as needed for folders and folder groups report.
        tenants = admin.portals.list_tenants()
        for portal in tenants:
            tenant = portal.name
        
            if tenant is not None:
                admin.portals.browse(tenant)
                zones = admin.cloudfs.zones.all()
                for zone in zones:
                    zonesummary = {}
                    zonesummary['Portal']=tenant
                    zonesummary['Zone']=zone.name
                    if zone.name == "All Folders":
                        zonesummary['Cloud Folders']=zone.name
                    else:
                        zonesummary['Cloud Folders']=','.join(getcloudfolders(admin,zone.zoneId))
                    devices = []
                    for device in zone.topDevices:
                        devices.append(device.name)
                    zonesummary['Devices']=','.join(devices)
                    zonesummary['Total Size']=zone.zoneStatistics.totalSize
                    zonesummary['Total Folders']=zone.zoneStatistics.totalFolders
                    zonesummary['Total Files']=zone.zoneStatistics.totalFiles
                    zonereport[zone.name]=zonesummary
                    logging.getLogger().error(f'Entry for {zone.name} on portal: {tenant} completed.')
                    writer.writerow(zonesummary)

            else:
                for portal in tenants:
                    tenant = portal.name
                    admin.portals.browse(tenant)
                    zones = admin.cloudfs.zones.all()
                    for zone in zones:
                        zonereport[zone.name]=zone

        admin.logout()
        return zonereport

    except CTERAException as error:
        raise click.ClickException(str(error))

def _login(host, user, secret):
    try:
        host.login(user, secret)
    except CTERAException as error:
        if error.response.code == 403:
            raise click.ClickException('Invalid username or password')
    return host

def from_console(prompt):
    user_input = None

    while not user_input:
        try:
            user_input = getpass(prompt)
        except EOFError:
            raise ConsentException()

    return user_input

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

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
if __name__ == '__main__':
    create()
