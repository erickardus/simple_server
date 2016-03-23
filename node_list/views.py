from django.shortcuts import render, redirect
import subprocess
import json
import boto3
import os
import logging
import time

log = logging.getLogger('provisioning_tool')
BASE_DIR = os.path.join(os.path.dirname(__file__), "../")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-provisioning")


#Boto EC connection

def nodes(request):
    ec2 = boto3.client('ec2')
    nodesList = [] 
    awszones = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    for zone in awszones:
        log.info( "AWS zone: %s" % (zone))
        ec2 = boto3.client('ec2', region_name=zone)
        for reservation in ec2.describe_instances()['Reservations']:
            log.info( "Reservation: %s" % (reservation))
            for insaws in reservation['Instances']:
                insid = insaws['InstanceId']
                nodename = insaws['Tags'][0]['Value']
                ec2 = boto3.resource('ec2', region_name=zone)
                instance = ec2.Instance(insid)
                log.info( "Instance: %s" % (instance))
                nodesList.append(["AWS",nodename,insid,instance.placement['AvailabilityZone'],instance.state['Name'],instance.instance_type,instance.public_dns_name,instance.public_ip_address,zone],)
    
    azurecall = json.loads(subprocess.getoutput('azure vm list --json'))
    for nodeazure in azurecall:
            insize = str(nodeazure['InstanceSize']) if 'InstanceSize' in nodeazure else ""
            nodesList.append(["Azure",str(nodeazure['VMName']),str(nodeazure['VMName']),str(nodeazure['Location']),str(nodeazure['InstanceStatus']),insize,str(nodeazure['DNSName']),str(nodeazure['IPAddress'])],)
    
    return render(request, 'node_list.html', {"nodesList": nodesList})
       


def node_destroy(request):

    if request.method == 'POST':
        driver = request.POST.get('driver')
        region = request.POST.get('region')
        nodename = request.POST.get('nodename')
        insid = request.POST.get('insid')
        log.info( "Destroy node: %s %s %s %s" % (nodename, insid, driver, region))
        ### remove from CHEF
        os.chdir(PROVISIONING_DIR)
        subprocess.run(['knife','node','delete', nodename,'--y'], shell=True )

        if driver == "AWS" :
        ### remove from AWS
            ec2 = boto3.resource('ec2', region_name=region)
            instance = ec2.Instance(insid)
            response = instance.terminate()

        elif driver == "Azure" :
        ### remove from AWS
            subprocess.run(['azure', 'vm', 'delete', nodename,'-b', '-q' ], shell=True )
            time.sleep(120)
            subprocess.run(['azure', 'storage', 'account', 'delete', nodename,'-q' ], shell=True )

    return redirect('node_list')
