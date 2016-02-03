#!/usr/local/bin/python3.5

import subprocess
import json
import boto3
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")


ec2 = boto3.resource('ec2')
os.chdir(PROVISIONING_DIR)
#insid = input("InsID: ")
nodename = input("NodeName: ")
#instance = ec2.Instance(insid)
#response = instance.terminate()
print(os.getcwd())
chefdestroy = subprocess.run(['knife', 'node', 'delete', nodename], shell=True)
print(chefdestroy)