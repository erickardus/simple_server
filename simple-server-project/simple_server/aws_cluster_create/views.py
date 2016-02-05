from django.shortcuts import render
from aws_cluster_create.forms import CreateClusterStep0, CreateClusterStep1, CreateClusterStep2, CreateClusterStep3
import subprocess
import os
import boto3
import logging
import sys


log = logging.getLogger('simple_server')
BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")
myregion = ''


def aws_cluster_creator_step0(request):
    """Renders AWS cluster create step #0.
    It asks you to select a region to work with AWS EC2.
    """

    # This will create a form, as defined in forms.py (CreateCluster0)
    form = CreateClusterStep0(request.POST or None)
    log.info('Generated form CreateClusterStep0')

    try:
        # This will make use of the form defined above and render it using a template.
        return render(request, 'aws_cluster_creator_step0.html', {'form': form})

    except:
        log.error('Unable to process the request')
        return render(request, 'error.html')


def aws_cluster_creator_step1(request):
    """Renders AWS cluster create step #1.
    This will ask for different entries, including:
        - Name | Name of the instance/server. Any name should work (this is basically just a AWS tag, called 'Name')
        - Number | The number of instances you want to launch (it will be done in parallel)
        - Instance Type | Select instance size depending on your needs
        - VPC Options
            * automatic - it will create vpc, subnet and security group based on 'Name' parameter.
            * existing - Allows you to pick a previously defined VPC, subnet and security group.
        - AMI | Allows you to select an ami-ID based on your selected region and predefined choices. List will only
                include AMIs with OS that will work with our Chef cookbooks.
        - SSH Username | it will be self-populated based on the AMI selection, but you can change it if you know for a
                fact the proper SSH username your OS/AMI needs to authenticate.
    """

    if request.method == 'POST':
        old_form = CreateClusterStep0(request.POST)
        log.info('Obtained CreateClusterStep0 form data')
        if old_form.is_valid():
            global myregion
            region = old_form.cleaned_data['region']
            log.info('Old form value region: %s' % region)
            try:
                form = CreateClusterStep1(request.POST or None)
                ami_choices = getAMIs(region)
            except:
                log.fatal('Unable to render form CreateClusterStep1. %s' % sys.exc_info()[0])

            return render(request, 'aws_cluster_creator_step1.html', {'form': form, 'ami_choices': ami_choices})
    else:
        return render(request, 'error.html')


def aws_cluster_creator_step2(request):

    # AWS - Select or Create a VPC
    if request.method == 'POST':
        old_form = CreateClusterStep1(request.POST)
        if old_form.is_valid():
            region = old_form.cleaned_data['region']
            vpc_selection = old_form.cleaned_data['vpc_selection']

            if vpc_selection == "automatic":
                form = CreateClusterStep3(request.POST or None)
                return render(request, 'aws_cluster_creator_step3.html', {'form': form})

            if (vpc_selection == "existing") or (vpc_selection == "new"):

                form = CreateClusterStep2(request.POST or None)
                vpc_choices, subnet_choices, sg_choices = getVPCinfo(region)

                return render(request, 'aws_cluster_creator_step2.html', {'form': form, 'vpc_selection': vpc_selection,
                                                                          'vpc_choices': vpc_choices,
                                                                          'subnet_choices': subnet_choices,
                                                                          'sg_choices': sg_choices})


def aws_cluster_creator_step3(request):

    # AWS - Select Roles and Runlist

    if request.method == 'POST':

        old_form = CreateClusterStep2(request.POST)
        if old_form.is_valid():
            form = CreateClusterStep3(request.POST or None)

    return render(request, 'aws_cluster_creator_step3.html', {'form': form})


def aws_cluster_creator_step4(request):

    if request.method == 'POST':
        form_past = CreateClusterStep3(request.POST or None)
        if form_past.is_valid():
            ami = form_past.cleaned_data['ami']
            instance_type = form_past.cleaned_data['instance_type']
            name = form_past.cleaned_data['name']
            roles = form_past.cleaned_data['roles']
            runlist = form_past.cleaned_data['runlist']
            region = form_past.cleaned_data['region']
            number = form_past.cleaned_data['number']
            vpc_selection = form_past.cleaned_data['vpc_selection']
            vpc = form_past.cleaned_data['myvpc']
            subnet = form_past.cleaned_data['mysubnet']
            security_group = form_past.cleaned_data['mysg']
            ssh_username = form_past.cleaned_data['ssh_username']

            output = create_action(region, number, ami, instance_type, name, roles, runlist, vpc_selection, vpc,
                                   subnet, security_group, ssh_username)
            output = output.decode('utf-8').split('\n')
            context = {
                "output": output,
                "ami": ami,
                "instance_type": instance_type,
                "name": name,
                "roles": roles,
                "runlist": runlist,
                "region": region,
                "number": number,
                "vpc": vpc,
                "subnet": subnet,
                "security_group": security_group,
            }

            return render(request, 'aws_cluster_creator_step4.html', context)


def create_action(region, number, ami, instance_type, name, roles, runlist, vpc_selection,
                  vpc, subnet, security_group, ssh_username):

    try:

        return subprocess.check_output(["ruby", "aws_cluster_creator.rb", "-r", region, "-n", name, "-N", number,
                                        "-a", ami, "-t", instance_type, "--roles", roles,
                                        "--runlist", runlist, '--vpcselection', vpc_selection,
                                        "--vpc", vpc, '--subnet_id', subnet, "--securitygroup_id", security_group,
                                        "--user", ssh_username],
                                       cwd=PROVISIONING_DIR, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        return exc.output


def getVPCinfo(region):

    ec2 = boto3.client('ec2', region_name=region)
    data = ec2.describe_vpcs()
    vpcinfo = {}
    for vpc in data['Vpcs']:
        vpcinfo[vpc['VpcId']] = {}
        vpcinfo[vpc['VpcId']]['Subnets'] = {}
        vpcinfo[vpc['VpcId']]['SGs'] = {}
        subnets = ec2.describe_subnets(Filters=[{'Name':'vpc-id','Values':[vpc['VpcId'],]}])
        security_groups = ec2.describe_security_groups(Filters=[{'Name':'vpc-id','Values':[vpc['VpcId'],]}])

        for subnet in subnets['Subnets']:
            vpcinfo[vpc['VpcId']]['Subnets'][subnet['SubnetId']] = {'CidrBlock': subnet['CidrBlock'],
                                                                    'AvailabilityZone': subnet['AvailabilityZone']}
            if 'Tags' in subnet:
                name = ''
                for tag in subnet['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break
            else:
                name = 'default'

            vpcinfo[vpc['VpcId']]['Subnets'][subnet['SubnetId']]['Name'] = name

        for sg in security_groups['SecurityGroups']:
            vpcinfo[vpc['VpcId']]['SGs'][sg['GroupName']] = {'GroupId': sg['GroupId'],
                                                             'IpPermissions': sg['IpPermissions']}
        if 'Tags' in vpc:
            name =  ''
            for tag in vpc['Tags']:
                if tag['Key'] == 'Name':
                    name = tag['Value']
                    break
            vpcinfo[vpc['VpcId']]['Name'] = name
        else:
            vpcinfo[vpc['VpcId']]['Name'] = 'default'

    vpc_choices = []
    for key in vpcinfo.keys():
        mystr = vpcinfo[key]['Name'] + " - " + key
        #vpc_choices.append((vpcinfo[key]['Name'], mystr))
        vpc_choices.append((key, mystr))

    subnet_choices = []
    for key in vpcinfo.keys():
        for subnetkey in vpcinfo[key]['Subnets'].keys():
            mystr = key + " - " + vpcinfo[key]['Subnets'][subnetkey]['Name'] + \
                    " (" + vpcinfo[key]['Subnets'][subnetkey]['CidrBlock'] + ") [" + \
                    vpcinfo[key]['Subnets'][subnetkey]['AvailabilityZone'] + "]"
            subnet_choices.append((subnetkey,mystr))

    sg_choices = []
    for key in vpcinfo.keys():
        for sg in vpcinfo[key]['SGs'].keys():
            mystr = key + " - " + vpcinfo[key]['SGs'][sg]['GroupId'] + " " + sg
            sg_choices.append((vpcinfo[key]['SGs'][sg]['GroupId'], mystr))

    return vpc_choices, subnet_choices, sg_choices


def getAMIs(region):

    listOS = ['Amazon Linux AMI 2015*HVM*', 'Red Hat Enterprise Linux 6*HVM*',
              'SUSE Linux Enterprise Server 12*HVM*', 'Ubuntu Server 14.04*HVM*'
             ]

    try:
        ec2 = boto3.client('ec2', region_name=region)
        ami_choices = []
        data = ec2.describe_images(Filters=[{'Name': 'description', 'Values': listOS}])
        for image in data['Images']:
            ami_choices.append((image['ImageId'], image['Description']))

        return ami_choices

    except:
        pass

