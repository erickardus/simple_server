#!/usr/local/bin/python2.7

import subprocess
import json
import boto3

#Boto EC connection


### create nodes json fila
ec2 = boto3.resource('ec2')
final_list = []
nodes = subprocess.check_output(["knife", "node", "list"], cwd='/home/aterrazas/simple_server/chef-repo/.chef')
node_list = nodes.split()

for nodej in node_list:
    with open( "nodes/" + nodej + ".json" , 'w')  as jf:
        #cloud = output_json['normal']['chef_provisioning']['driver_url'] if output_json['normal']['chef_provisioning']['driver_url'] else output_json['normal']['chef_provisioning']['reference'][['driver_url']
        node_show = subprocess.call(["knife", "node", "show", nodej, "-F" ,"json" ], cwd='/home/aterrazas/simple_server/chef-repo/.chef', stdout=jf)    
        output_json = json.load(open('nodes/' + nodej + '.json'))
        insid = ''
        if output_json['normal']['chef_provisioning']['reference']['instance_id'] in output_json:
            insid = output_json['normal']['chef_provisioning']['reference']['instance_id']
        else: 
            insid = output_json['normal']['chef_provisioning']['reference']['vm_name']

        print insid

'''
        if aws in cloud
            instance = ec2.Instance(insid)
            final_list.append([nodej,insid,instance.state['Name'],instance.instance_type,instance.public_dns_name,instance.public_ip_address],) 
'''
