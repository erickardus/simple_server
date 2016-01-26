import subprocess
import json
import boto3
from django.views.generic import TemplateView

#Boto EC connection


class NodeList(TemplateView):
    template_name = "node_list.html"

    def nodes(self):
    ### create nodes json fila
        ec2 = boto3.resource('ec2')
        final_list = []
        nodes = subprocess.check_output(["knife", "node", "list"], cwd='/home/aterrazas/simple_server/chef-repo/.chef')
        node_list = nodes.split()
        for nodej in node_list:
            with open( "node_list/nodes/" + nodej + ".json" , 'w')  as jf:
                node_show = subprocess.call(["knife", "node", "show", nodej, "-F" ,"json" ], cwd='/home/aterrazas/simple_server/chef-repo/.chef', stdout=jf) 

                output_json = json.load(open('node_list/nodes/' + nodej + '.json'))
                insid = output_json['normal']['chef_provisioning']['reference']['instance_id']
                instance = ec2.Instance(insid)
                final_list.append([nodej,insid,instance.state['Name'],instance.instance_type,instance.public_dns_name,instance.public_ip_address],)

        return final_list

    def get_context_data(self, **kwargs):
        context = super(NodeList, self).get_context_data(**kwargs)
        context['nodes'] = self.nodes()
        return context
