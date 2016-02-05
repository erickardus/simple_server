from django.shortcuts import render
import logging

log = logging.getLogger('simple_server')


def home(request):

    return render(request, 'home.html')

