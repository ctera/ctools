import hashlib
import re

from login import global_admin_login
from filer import get_filer


def check_local_db(edge_filer):
    get_list = ['status', 'config']
    info = edge_filer.api.get_multi('/', get_list)

    edge_filer.telnet.enable(hashlib.sha1(
        (info.status.device.MacAddress + '-' + info.status.device.runningFirmware).encode('utf-8')).hexdigest()[:8])

    output =  edge_filer.shell.run_command('stat /var/volumes/vol1/.ctera/cloudSync/CloudSync.db')
    #print(output)
    size_bytes = int(re.search(r'(?<=Size:\ )[0-9]*', output).group())
    size_gb = round(size_bytes/2**30,2)

    edge_filer.telnet.disable()

    return size_gb


ga = global_admin_login("portal.ctera.me", "admin", "lap6056*")

edge_filer = get_filer(ga, "labgw")

print("Size: ", check_local_db(edge_filer))

ga.logout()