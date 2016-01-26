require 'chef/provisioning'
require 'chef/provisioning/aws_driver'

with_driver "aws::us-west-1"

with_machine_options({
    ssh_username: "ec2-user",
    bootstrap_options: {
        image_id: "ami-353aff71",
        instance_type: "t2.micro",
    },
})

with_chef_server "https://manage.chef.io/organizations/simple_server",
  :client_name => Chef::Config[:node_name],
  :signing_key_filename => Chef::Config[:client_key]


machine_batch "cluster" do
    1.upto(1) do |i|
        machine "server#{i}" do
            
            
        end
    end
end

