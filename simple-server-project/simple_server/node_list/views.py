from django.shortcuts import render, redirect
import subprocess
import json
import boto3
import os
import logging

log = logging.getLogger('simple_server')

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")


#Boto EC connection
ec2 = boto3.resource('ec2')

def nodes(request):
### create nodes json fila
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
    return render(request, 'node_list.html', {"nodesList": nodesList})
       
def node_destroy(request):
    if request.method == 'POST':
        driver = request.POST.get('driver')
        nodename = request.POST.get('nodename')
        insid = request.POST.get('insid')   
        log.info( "Destroy node:",nodename, insid, driver )
    ### remove from CHEF
        os.chdir(PROVISIONING_DIR)
        subprocess.run(['knife','node','delete', nodename,'--y'], shell=True )
    ### remove from AWS
        instance = ec2.Instance(insid)
        response = instance.terminate()
    
    #return render(request, 'node_action.html', {"nodename": nodename,"insid": insid})
    return redirect('node_list')

