import boto3
import subprocess
import os
import logging


log = logging.getLogger('provisioning_tool')
BASE_DIR = os.path.join(os.path.dirname(__file__), "../")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-provisioning")


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


def aws_cluster_create(region, number, ami, instance_type, name, roles, runlist, vpc_selection,
                       vpc, subnet, security_group, ssh_username):
    try:
        process = subprocess.Popen(["ruby", "aws_cluster_creator.rb", "-r", region, "-n", name, "-N", number,
                                            "-a", ami, "-t", instance_type, "--roles", roles,
                                            "--runlist", runlist, '--vpcselection', vpc_selection,
                                            "--vpc", vpc, '--subnet_id', subnet, "--securitygroup_id", security_group,
                                            "--user", ssh_username], cwd=PROVISIONING_DIR)
        log.info('RubyCall AWS: ruby aws_cluster_creator.rb -r %s -n %s -N %s -a %s -t %s --roles %s --runlist %s --vpcselection %s --vpc %s --subnet_id %s --securitygroup_id %s --user %s ' %
                    (region, name, number, ami, instance_type, roles,runlist, vpc_selection, vpc, subnet,
                    security_group, ssh_username))
    except:
        pass

def handle_exception(ex):
    log.error('%s (%s)' % (ex.message, type(ex)))


def azure_cluster_create(location, number, image_id, vm_size, name, roles, runlist, tcp_endpoints):

    try:

        process = subprocess.Popen(["ruby", "azure_cluster_creator.rb", "-l", location, "-n", name, "-N", number,
                                        "-i", image_id, "-s", vm_size, "--roles", roles,
                                        "--runlist", runlist, "--cloud_service_name", name,
                                        "--storage_account_name", name,
                                        "tcp_endpoints", tcp_endpoints], cwd=PROVISIONING_DIR)
        log.info('RubyCall Azure: -l %s -n %s -N %s -i %s -s %s --roles %s --runlist %s --cloud_service_name %s --storage_account_name %s tcp_endpoints  %s' %
                (location, name, number, image_id, vm_size, roles, runlist, name, name, tcp_endpoints))
    except :
        pass


