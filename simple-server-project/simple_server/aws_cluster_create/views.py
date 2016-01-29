from django.shortcuts import render
from aws_cluster_create.forms import CreateClusterStep0, CreateClusterStep1, CreateClusterStep2
import subprocess
import os
import logging


log = logging.getLogger('simple_server')
BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")
myregion = ''


def aws_cluster_creator_step0(request):

    # AWS - Select a region
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
            user = old_form.cleaned_data['user']

            new_form = CreateClusterStep2(request.POST or None, vpc_selection=vpc_selection, myregion=region)

    return render(request, 'aws_cluster_creator_step2.html', {'form': new_form, 'name': name,
                                                              'instance_type': instance_type,
                                                              'ami': ami, 'region': region,
                                                              'number': number, 'user': user,
                                                              'vpc_selection': vpc_selection,
                                                              'myregion': region

                                                              })




def aws_cluster_creator_step3(request):

    # AWS - Select Roles and Runlist

    if request.method == 'POST':

        old_form = CreateClusterStep2(request.POST, myregion=myregion)
        if old_form.is_valid():
            new_form = CreateClusterStep3(request.POST or None)
            name = old_form.cleaned_data['name']
            instance_type = old_form.cleaned_data['instance_type']
            ami = old_form.cleaned_data['ami']
            vpc = old_form.cleaned_data['vpc']
            region = old_form.cleaned_data['region']
            number = old_form.cleaned_data['number']
            user = old_form.cleaned_data['user']
            vpc_name = old_form.cleaned_data['vpc_name']

    return render(request, 'aws_cluster_creator_step3.html', {'form': new_form, 'name': name,
                                                                      'instance_type': instance_type,
                                                                      'ami': ami, 'region': region,
                                                                      'number': number, 'user': user,
                                                                      'vpc': vpc, 'vpc_name': vpc_name
                                                                      }
                          )



def aws_cluster_creator_step4(request):

    if request.method == 'POST':
        form_past = CreateClusterStep3(request.POST or None)
        if form_past.is_valid():
            ami = form_past.cleaned_data['ami']
            vpc = form_past.cleaned_data['vpc']
            instance_type = form_past.cleaned_data['instance_type']
            log.debug('from last form ami %s' % ami)
            name = form_past.cleaned_data['name']
            roles = form_past.cleaned_data['roles']
            runlist = form_past.cleaned_data['runlist']
            region = form_past.cleaned_data['region']
            number = form_past.cleaned_data['number']
            user = form_past.cleaned_data['user']

            output = create_action(region, number, user, ami, instance_type, name, roles, runlist)
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


def create_action(region, number, user, ami, instance_type, name, roles, runlist):

    try:

        return subprocess.check_output(["ruby", "aws_cluster_creator.rb", "-r", region, "-n", name, "-N", number,
                                        "-u", user, "-a", ami, "-t", instance_type, "--roles", roles,
                                        "--runlist", runlist], cwd=PROVISIONING_DIR, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        return exc.output




