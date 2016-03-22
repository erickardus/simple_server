from django.shortcuts import render
import logging

log = logging.getLogger('provisioning_tool')


def home(request):
    """Renders home.html.
    """

    return render(request, 'home.html')

