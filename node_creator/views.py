from django.shortcuts import render
from node_creator.forms import Server, Software
import subprocess
from django.template import RequestContext


def creator_step1(request):
    form = Server(request.POST or None)

    return render(request, 'creator_step1.html', {'form': form})


def creator_step2(request):

    if request.method == 'POST':
        form_past = Server(request.POST)
        if form_past.is_valid():
            new_form = Software(request.POST or None)
            name = form_past.cleaned_data['name']
            flavor = form_past.cleaned_data['flavor']
            image = form_past.cleaned_data['image']
            #return render(request, 'creator_step2.html', {'form': new_form})
            return render(request, 'creator_step2.html', {'form': new_form, 'name': name, 'flavor': flavor, 'image': image})


def creator_step3(request):

    if request.method == 'POST':
        form = Software(request.POST or None)
        if form.is_valid():
            image = form.cleaned_data['image']
            flavor = form.cleaned_data['flavor']
            name = form.cleaned_data['name']
            runlist = form.cleaned_data['runlist']

            output = create_action(image, flavor, name, runlist)
            output = output.decode('utf-8').split('\n')
            context = {
                "output": output,
                "image": image,
                "runlist": runlist,
                "flavor": flavor,
                "name": name,
            }

            return render(request, 'creator_step3.html', context)


def create_action(image, flavor, name, runlist):
    #return subprocess.check_output(["ruby", "create_node.rb", "-I", image, "-f", flavor, "-N", name, "-r", runlist], cwd="C:/Users/erick.ramirez/chef-hosted-repo")
    try:
        return subprocess.check_output(["ruby", "create_node.rb", "-I", image, "-f", flavor, "-N", name, "-r", runlist], cwd="C:/Users/erick.ramirez/chef-hosted-repo", stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        return exc.output




