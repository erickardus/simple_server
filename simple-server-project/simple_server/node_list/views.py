import subprocess
import json
import boto3
from django.views.generic import TemplateView
import os
import shutil

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")


#Boto EC connection


class NodeList(TemplateView):
    template_name = "node_list.html"

    def nodes(self):
    ### create nodes json fila
        ec2 = boto3.resource('ec2')
        nodesList = [] 
        os.chdir(PROVISIONING_DIR)
        nodes = subprocess.getoutput(['knife', "node", "list"])
        node_list = nodes.split()
        for nodej in node_list:
            chefcall = json.loads(subprocess.getoutput(['knife', "node", "show", str(nodej), "-F" ,"json" ]))
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
                azurecall = json.loads(subprocess.getoutput(["azure", "vm", "show", insid , "--json" ]))
                insize = str(azurecall['InstanceSize']) if 'InstanceSize' in azurecall else ""
                nodesList.append([driver,nodej,insid,str(azurecall['InstanceStatus']),insize,str(azurecall['DNSName']),str(azurecall['IPAddress'])],)

        return nodesList

    def get_context_data(self, **kwargs):
        context = super(NodeList, self).get_context_data(**kwargs)
        context['nodes'] = self.nodes()
        return context
