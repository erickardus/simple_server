import subprocess
import json
import boto3
from django.views.generic import TemplateView
import os

ec2 = boto3.resource('ec2')
nodesList = [] 

log = logging.getLogger('simple_server')
BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")

nodes = subprocess.check_output(["knife", "node", "list"], cwd=PROVISIONING_DIR)
node_list = nodes.split()
for nodej in node_list:
    chefcall = json.loads(subprocess.check_output(["knife", "node", "show", nodej, "-F" ,"json" ], cwd=PROVISIONING_DIR))
    driver = ''
    insid = ''
    if 'driver_url' in chefcall['normal']['chef_provisioning'] :
        driver = "AWS" 
        insid = str(chefcall['normal']['chef_provisioning']['reference']['instance_id'])
        instance = ec2.Instance(insid)
        nodesList.append([driver,nodej,insid,instance.state['Name'],instance.instance_type,instance.public_dns_name,instance.public_ip_address],)
    elif 'driver_url' in chefcall['normal']['chef_provisioning']['reference']:
        driver = "Azure" 
        insid = str(chefcall['normal']['chef_provisioning']['reference']['vm_name'])
        azurecall = json.loads(subprocess.check_output(["azure", "vm", "show", insid , "--json" ]))
        nodesList.append([driver,nodej,insid,str(azurecall['InstanceStatus']),str(azurecall['InstanceSize']),str(azurecall['DNSName']),str(azurecall['IPAddress'])],)

print 