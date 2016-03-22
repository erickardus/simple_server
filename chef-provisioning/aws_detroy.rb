require 'chef/provisioning'
require 'chef/provisioning/aws_driver'

with_driver "aws::us-east-1"

with_chef_server "https://manage.chef.io/organizations/provisioning_tool",
  :client_name => Chef::Config[:node_name],
  :signing_key_filename => Chef::Config[:client_key]


machine "practicaws2" do
    action :destroy
end

