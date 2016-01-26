from django.views.generic import TemplateView
import logging
log = logging.getLogger('simple_server')

log.debug('hello')

class Home(TemplateView):
    template_name = "home.html"






