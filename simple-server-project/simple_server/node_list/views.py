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
    nodesList = [] 
    awscall = json.loads(subprocess.getoutput(['aws', "ec2", "describe-instances"]))
    for nodeaws in awscall['Reservations']:
        insid = str(nodeaws['Instances'][0]['InstanceId']) 
        nodename = str(nodeaws['Instances'][0]['Tags'][0]['Value']) 
        instance = ec2.Instance(insid)
        nodesList.append(["AWS",nodename,insid,instance.placement['AvailabilityZone'],instance.state['Name'],instance.instance_type,instance.public_dns_name,instance.public_ip_address],)

    azurecall = json.loads(subprocess.getoutput(['azure', 'vm', 'list', '--json']))
    for nodeazure in azurecall:

            insize = str(nodeazure['InstanceSize']) if 'InstanceSize' in nodeazure else ""
            nodesList.append(["Azure",str(nodeazure['VMName']),str(nodeazure['VMName']),str(nodeazure['Location']),str(nodeazure['InstanceStatus']),insize,str(nodeazure['DNSName']),str(nodeazure['IPAddress'])],)
    
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
    
    return redirect('node_list')

