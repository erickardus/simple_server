require 'chef/provisioning'
require 'chef/provisioning/aws_driver'

with_driver "aws::us-east-1"

with_machine_options({
    ssh_username: "ec2-user",
    bootstrap_options: {
        image_id: "ami-0d4cfd66",
        instance_type: "t2.micro",
    },
})

with_chef_server "https://manage.chef.io/organizations/simple_server",
  :client_name => Chef::Config[:node_name],
  :signing_key_filename => Chef::Config[:client_key]


machine_batch "cluster" do
<<<<<<< HEAD
    1.upto(1) do |i|
<<<<<<< HEAD
        machine "server#{i}" do
=======
        machine "boombox#{i}" do
>>>>>>> 65da696e2d7ce42b86768d75219a7c7f55efebef
=======
    1.upto(2) do |i|
        machine "hello#{i}" do
>>>>>>> 1e9964cb6dc024555816a99dbb1be31a4352ffa0
            
            
                role 'webserver'
            
        end
    end
end

