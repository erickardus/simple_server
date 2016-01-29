import subprocess
import json
import boto3
from django.views.generic import TemplateView
import os
import shutil

ec2 = boto3.resource('ec2')
instance = ec2.Instance(input())
response = instance.terminate()
