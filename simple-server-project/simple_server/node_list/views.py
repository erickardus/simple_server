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
    #os.chdir(PROVISIONING_DIR)
    #for nodej in node_list:
    #chefcall = json.loads(subprocess.getoutput(['knife', "node", "show", str(nodej), "-F" ,"json" ]))
    awscall = json.loads(subprocess.getoutput(['aws', "ec2", "describe-instances"]))
    for nodeaws in awscall['Reservations']:
        insid = str(nodeaws['Instances'][0]['InstanceId']) 
        nodename = str(nodeaws['Instances'][0]['Tags'][0]['Value']) 
        instance = ec2.Instance(insid)
        nodesList.append(["AWS",nodename,insid,instance.placement['AvailabilityZone'],instance.state['Name'],instance.instance_type,instance.public_dns_name,instance.public_ip_address],)
<<<<<<< HEAD
    '''
    azurecall = json.loads(subprocess.getoutput(['aws', "ec2", "describe-instances"]))
    
    for nodeazure in azurecall:
            azurecall = json.loads(subprocess.getoutput(["azure", "vm", "show", insid , "--json" ]))
            insize = str(azurecall['InstanceSize']) if 'InstanceSize' in azurecall else ""
            nodesList.append([driver,nodej,insid,str(azurecall['Location']),str(azurecall['InstanceStatus']),insize,str(azurecall['DNSName']),str(azurecall['IPAddress'])],)
    '''
=======
    
    azurecall = json.loads(subprocess.getoutput(['azure', 'vm', 'list', '--json']))
    for nodeazure in azurecall:
            insize = str(azurecall[0]['InstanceSize']) if 'InstanceSize' in azurecall[0] else ""
            nodesList.append(["Azure",str(azurecall[0]['VMName']),insid,str(azurecall[0]['Location']),str(azurecall[0]['InstanceStatus']),insize,str(azurecall[0]['DNSName']),str(azurecall[0]['IPAddress'])],)
>>>>>>> ead42e20dc56eedf7c8621a0d93c8272da299d76
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
        
        if driver == "AWS" :
        ### remove from AWS
            instance = ec2.Instance(insid)
            response = instance.terminate()
        elif driver == "Azure" :
            subprocess.run(['azure', 'vm', 'delete', nodename,'-b', '-q' ], shell=True )  
            subprocess.run(['azure', 'storage', 'account', 'delete', nodename,'-q' ], shell=True )  
    
    #return render(request, 'node_action.html', {"nodename": nodename,"insid": insid})
    return redirect('node_list')

