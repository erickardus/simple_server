import subprocess
from django.views.generic import TemplateView


class NodeList(TemplateView):
    template_name = "node_list.html"

    def nodes(self):
        cmd = "knife node list"
        result = subprocess.check_output(["ruby", "myknife.rb"], cwd='C:/Users/erick.ramirez/chef-hosted-repo')
        node_list = result.decode('utf-8').split()
        return node_list

    def get_context_data(self, **kwargs):
        context = super(NodeList, self).get_context_data(**kwargs)
        context['nodes'] = self.nodes()
        return context


