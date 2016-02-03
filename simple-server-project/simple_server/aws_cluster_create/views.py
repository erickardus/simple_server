from django.shortcuts import render
from aws_cluster_create.forms import CreateClusterStep0, CreateClusterStep1, CreateClusterStep2, CreateClusterStep3
import subprocess
import os
import boto3
import logging


log = logging.getLogger('simple_server')
BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")
myregion = ''


def aws_cluster_creator_step0(request):

    # AWS - Select a region to launch your servers
    form = CreateClusterStep0(request.POST or None)
    log.info('Generated form CreateClusterStep0')
    return render(request, 'aws_cluster_creator_step0.html', {'form': form})


def aws_cluster_creator_step1(request):

    # AWS - Select Name, Number, Flavor, User, Region, AMI and VPC options.
    if request.method == 'POST':
        old_form = CreateClusterStep0(request.POST)
        log.info('Obtained CreateClusterStep0 form data')
        if old_form.is_valid():
            global myregion
            region = old_form.cleaned_data['region']
            log.info('Old form value region: %s' % region)
            try:
                new_form = CreateClusterStep1(request.POST or None, myregion=region)
            except:
                log.fatal('Unable to render form CreateClusterStep1. %s' % sys.exc_info()[0])

            return render(request, 'aws_cluster_creator_step1.html', {'form': new_form, 'region': region})


def aws_cluster_creator_step2(request):

    # AWS - Select or Create a VPC
    if request.method == 'POST':
        old_form = CreateClusterStep1(request.POST, myregion=myregion)
        if old_form.is_valid():
            name = old_form.cleaned_data['name']
            instance_type = old_form.cleaned_data['instance_type']
            ami = old_form.cleaned_data['ami']
            vpc_selection = old_form.cleaned_data['vpc_selection']
            region = old_form.cleaned_data['region']
            number = old_form.cleaned_data['number']

            new_form = CreateClusterStep2(request.POST or None)

            vpc_choices, subnet_choices, sg_choices = getVPCinfo(region)

    return render(request, 'aws_cluster_creator_step2.html', {'form': new_form, 'name': name,
                                                              'instance_type': instance_type,
                                                              'ami': ami, 'region': region,
                                                              'number': number,
                                                              'vpc_selection': vpc_selection,
                                                              'myregion': region, 'vpc_choices': vpc_choices,
                                                              'subnet_choices': subnet_choices,
                                                              'sg_choices': sg_choices
                                                              })




def aws_cluster_creator_step3(request):

    # AWS - Select Roles and Runlist

    if request.method == 'POST':

        old_form = CreateClusterStep2(request.POST)
        if old_form.is_valid():
            new_form = CreateClusterStep3(request.POST or None)
            name = old_form.cleaned_data['name']
            instance_type = old_form.cleaned_data['instance_type']
            ami = old_form.cleaned_data['ami']
            #vpc = old_form.cleaned_data['vpc']
            region = old_form.cleaned_data['region']
            vpc_selection = old_form.cleaned_data['vpc_selection']
            number = old_form.cleaned_data['number']
            myvpc = request.POST.get('myvpc')
            mysubnet = request.POST.get('mysubnet')
            mysg = request.POST.get('mysg')

    return render(request, 'aws_cluster_creator_step3.html', {'form': new_form, 'name': name,
                                                              'instance_type': instance_type,
                                                              'ami': ami, 'region': region,
                                                              'myvpc': myvpc,
                                                              'mysubnet': mysubnet, 'mysg': mysg
                                                              }
                  )


def aws_cluster_creator_step4(request):

    if request.method == 'POST':
        form_past = CreateClusterStep3(request.POST or None)
        if form_past.is_valid():
            ami = form_past.cleaned_data['ami']
            #vpc = form_past.cleaned_data['vpc']
            instance_type = form_past.cleaned_data['instance_type']
            log.debug('from last form ami %s' % ami)
            name = form_past.cleaned_data['name']
            roles = form_past.cleaned_data['roles']
            runlist = form_past.cleaned_data['runlist']
            region = form_past.cleaned_data['region']
            number = form_past.cleaned_data['number']
            vpc_selection = form_past.cleaned_data['vpc_selection']
            myvpc = form_past.cleaned_data['myvpc']
            mysubnet = form_past.cleaned_data['mysubnet']
            mysg = form_past.cleaned_data['mysg']

            output = create_action(region, number, ami, instance_type, name, roles, runlist, vpc_selection, myvpc,
                                   mysubnet, mysg)
            output = output.decode('utf-8').split('\n')
            context = {
                "output": output,
                "ami": ami,
                "runlist": runlist,
                "instance_type": instance_type,
                "name": name,
                "roles": roles,
            }

            return render(request, 'aws_cluster_creator_step4.html', context)


def create_action(region, number, ami, instance_type, name, roles, runlist, vpc_selection, myvpc, mysubnet, mysg):

    try:

        return subprocess.check_output(["ruby", "aws_cluster_creator.rb", "-r", region, "-n", name, "-N", number,
                                        "-a", ami, "-t", instance_type, "--roles", roles,
                                        "--runlist", runlist, '--vpcselection', vpc_selection,
                                        "--vpc", myvpc, '--subnet_id', mysubnet, "--securitygroup_id", mysg],
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


