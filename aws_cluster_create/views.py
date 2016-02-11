from django.shortcuts import render
from aws_cluster_create.forms import CreateClusterStep0, CreateClusterStep1, CreateClusterStep2, CreateClusterStep3
from scripts.common import getVPCinfo, getAMIs, aws_cluster_create, handle_exception
import logging

log = logging.getLogger('simple_server')


def aws_cluster_creator_step0(request):
    """Renders AWS cluster create step #0.
    It asks you to select a region to work with AWS EC2.
    """

    # This will create a form, as defined in forms.py (CreateCluster0)
    form = CreateClusterStep0

    try:
        # This will make use of the form defined above and render it using a template.
        return render(request, 'aws_cluster_creator_step0.html', {'form': form})

    except Exception as e:
        handle_exception(e)
        return render(request, 'error.html')


def aws_cluster_creator_step1(request):
    """Renders AWS cluster create step #1.
    It asks you to select name, number, ami, instance type and more.
    """

    if request.method == 'POST':
        old_form = CreateClusterStep0(request.POST)
        log.info('Obtained CreateClusterStep0 form data')
        if old_form.is_valid():
            region = old_form.cleaned_data['region']
            log.info('Old form value region: %s' % region)
            try:
                form = CreateClusterStep1(request.POST or None)
                ami_choices = getAMIs(region)
            except Exception as e:
                handle_exception(e)

            return render(request, 'aws_cluster_creator_step1.html', {'form': form, 'ami_choices': ami_choices})
    else:
        return render(request, 'error.html')


def aws_cluster_creator_step2(request):
    """This function is about VPC, subnet and security group selection.
    Based on previous entry vpc_selection, you will be redirected to a page
    to pick one of the available VPC, subnet and SG options or just create one
    automatically based on the name of the server.
    """

    if request.method == 'POST':
        old_form = CreateClusterStep1(request.POST)
        log.info('Obtained CreateClusterStep1 form data')
        if old_form.is_valid():
            region = old_form.cleaned_data['region']
            vpc_selection = old_form.cleaned_data['vpc_selection']
            log.debug('region= %s' % region)
            log.debug('vpc_selection= %s' % vpc_selection)

            if vpc_selection == "automatic":
                log.debug('Rendering aws_cluster_creator_step3.html using CreateClusterStep3 form.')
                form = CreateClusterStep3(request.POST or None)
                return render(request, 'aws_cluster_creator_step3.html', {'form': form})

            if (vpc_selection == "existing") or (vpc_selection == "new"):
                log.debug('Rendering aws_cluster_creator_step2.html using CreateClusterStep2 form')
                form = CreateClusterStep2(request.POST or None)
                try:
                    vpc_choices, subnet_choices, sg_choices = getVPCinfo(region)
                except Exception as ex:
                    handle_exception(ex)

                return render(request, 'aws_cluster_creator_step2.html', {'form': form, 'vpc_selection': vpc_selection,
                                                                          'vpc_choices': vpc_choices,
                                                                          'subnet_choices': subnet_choices,
                                                                          'sg_choices': sg_choices})


def aws_cluster_creator_step3(request):
    """This is the last screen to select options. It will be used to decide
    on which cookbooks or roles you want your cluster to be configured with.
    """

    if request.method == 'POST':
        old_form = CreateClusterStep2(request.POST)
        if old_form.is_valid():
            form = CreateClusterStep3(request.POST or None)

    return render(request, 'aws_cluster_creator_step3.html', {'form': form})


def aws_cluster_creator_step4(request):
    """This function gathers all data selected by the user and uses it
    to call a function that will create an RB file out of a template
    resulting in a Chef provisioning script, and then executes it to
    retrieve the output which is printed in screen.
    """

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
            vpc = form_past.cleaned_data['vpc']
            subnet = form_past.cleaned_data['subnet']
            security_group = form_past.cleaned_data['sg']
            ssh_username = form_past.cleaned_data['ssh_username']

            # Calls a function that obtains the result of the Chef provisioning script. This takes a few minutes
            # to complete, so be patient.
            try:
                output = aws_cluster_create(region, number, ami, instance_type, name, roles, runlist, vpc_selection,
                                            vpc, subnet, security_group, ssh_username)
                output = output.decode('utf-8').split('\n')
            except Exception as ex:
                handle_exception(ex)
                return render(request, 'error.html')

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
