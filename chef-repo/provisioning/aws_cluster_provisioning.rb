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
    1.upto(2) do |i|
        machine "hola#{i}" do
            
            
                role 'webserver'
            
        end
    end
end

