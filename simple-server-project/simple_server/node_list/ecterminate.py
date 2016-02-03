import subprocess
import json
import boto3
import os
import shutil

from django.views.generic import TemplateView
### remove from CHEF
BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")

os.chdir(PROVISIONING_DIR)
subprocess.run(['knife','node','delete',input(),'--y'], shell=True )

### remove from AWS
#ec2 = boto3.resource('ec2')
#instance = ec2.Instance(input())
#response = instance.terminate()

