from django.shortcuts import render


def cluster_creator(request):
    """Starting point for cluster creation.
    Allows you to pick different cloud providers.
    """
    return render(request, 'cluster_create.html')
