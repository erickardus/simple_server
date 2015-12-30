from django.shortcuts import render
from azure_cluster_create.forms import CreateClusterStep1, CreateClusterStep2
import subprocess
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../..")
PROVISIONING_DIR = os.path.join(BASE_DIR, "chef-repo/provisioning")


def azure_cluster_creator_step1(request):

    form = CreateClusterStep1(request.POST or None)
    return render(request, 'azure_cluster_creator_step1.html', {'form': form})


def azure_cluster_creator_step2(request):

    if request.method == 'POST':
        form_past = CreateClusterStep1(request.POST)
        if form_past.is_valid():
            new_form = CreateClusterStep2(request.POST or None)
            name = form_past.cleaned_data['name']
            vm_size = form_past.cleaned_data['vm_size']
            image_id = form_past.cleaned_data['image_id']
            location = form_past.cleaned_data['location']
            number = form_past.cleaned_data['number']
            password = form_past.cleaned_data['password']
            cloud_service_name = form_past.cleaned_data['cloud_service_name']
            storage_account_name = form_past.cleaned_data['storage_account_name']
            tcp_endpoints = form_past.cleaned_data['tcp_endpoints']
            return render(request, 'azure_cluster_creator_step2.html', {'form': new_form, 'name': name,
                                                                        'vm_size': vm_size,
                                                                        'image_id': image_id, 'location': location,
                                                                        'number': number, 'password': password,
                                                                        'cloud_service_name': cloud_service_name,
                                                                        'storage_account_name': storage_account_name,
                                                                        'tcp_endpoints': tcp_endpoints})


def azure_cluster_creator_step3(request):

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
            password = form_past.cleaned_data['password']
            cloud_service_name = form_past.cleaned_data['cloud_service_name']
            storage_account_name = form_past.cleaned_data['storage_account_name']
            tcp_endpoints = form_past.cleaned_data['tcp_endpoints']

            output = create_action(location, number, password, image_id,
                                   vm_size, name, roles, runlist,
                                   cloud_service_name, storage_account_name,
                                   tcp_endpoints
                                   )
            output = output.decode('utf-8').split('\n')
            context = {
                "output": output,
                "image_id": image_id,
                "runlist": runlist,
                "vm_size": vm_size,
                "name": name,
                "roles": roles,
            }

            return render(request, 'azure_cluster_creator_step3.html', context)


def create_action(region, number, user, ami, instance_type, name, roles, runlist,
                  cloud_service_name, storage_account_name, tcp_endpoints):

    try:

        return subprocess.check_output(["ruby", "azure_cluster_creator.rb", "-r", region, "-n", name, "-N", number, "-u", user,
                                        "-a", ami, "-t", instance_type, "--roles", roles,
                                        "--runlist", runlist, "--cloud_service_name", cloud_service_name,
                                        "--storage_account_name", storage_account_name,
                                        "tcp_endpoints", tcp_endpoints], cwd=PROVISIONING_DIR, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        return exc.output




