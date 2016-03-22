from django.shortcuts import render
from azure_cluster_create.forms import CreateClusterStep1, CreateClusterStep2
from scripts.common import azure_cluster_create
import logging

log = logging.getLogger('provisioning_tool')


def azure_cluster_creator_step1(request):
    """Step 1. Selection of name, number, ImageId, VM size and location.
    """

    form = CreateClusterStep1
    log.info('Rendering CreateClusterStep1')
    return render(request, 'azure_cluster_creator_step1.html', {'form': form})


def azure_cluster_creator_step2(request):
    """Step 2. Selection of roles or runlist to configure in the target nodes.
    """

    if request.method == 'POST':
        form_past = CreateClusterStep1(request.POST)
        log.info('Successfully obtain data from POST request CreateClusterStep1')
        if form_past.is_valid():
            form = CreateClusterStep2(request.POST or None)
            log.info('Rendering CreateClusterStep2')
            return render(request, 'azure_cluster_creator_step2.html', {'form': form})


def azure_cluster_creator_step3(request):
    """Step 3. This screen will run the Chef provisioning script that provisions servers
    based on a ERB templated and parameters passed from this page.
    """

    if request.method == 'POST':
        form_past = CreateClusterStep2(request.POST or None)
        if form_past.is_valid():
            image_id = form_past.cleaned_data['image_id']
            vm_size = form_past.cleaned_data['vm_size']
            name = form_past.cleaned_data['name']
            roles = form_past.cleaned_data['roles']
            runlist = form_past.cleaned_data['runlist']
            location = form_past.cleaned_data['location']
            number = form_past.cleaned_data['number']
            tcp_endpoints = form_past.cleaned_data['tcp_endpoints']

            output = azure_cluster_create(location, number, image_id, vm_size, name, roles, runlist, tcp_endpoints)
            #output = output.decode('utf-8').split('\n')
            context = {
                "output": output,
                "image_id": image_id,
                "runlist": runlist,
                "vm_size": vm_size,
                "name": name,
                "roles": roles,
            }   

            return render(request, 'azure_cluster_creator_step3.html', context)

def seeazurelog(request):
    return render(request, 'azure_log_interactive.txt','')

def azurelogpage(request):
    return render(request, 'azure_log.html', '')





