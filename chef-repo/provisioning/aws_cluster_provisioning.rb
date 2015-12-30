require 'chef/provisioning'
require 'chef/provisioning/aws_driver'

with_driver "aws::us-east-1"

with_machine_options({
    ssh_username: "ec2-user",
    bootstrap_options: {
        image_id: "ami-60b6c60a",
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

ruby_block "print out public IPs" do
    block do
        nodes = search(:node, "name:server*")
        for node in nodes
            Chef::Log.info("Application can be accessed at http://#{node['ec2']['public_ipv4']}:3001")
        end
    end
end